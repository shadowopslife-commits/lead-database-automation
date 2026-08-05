import re, time, sys
from pathlib import Path

BASE = Path(r"C:\ShadowOps_CANONICAL\03_STATE_BUILD")
IN_FILE = BASE / "UNKNOWN_REMAINING.txt"

STATE_FILES = {
    "CA": BASE / "CA.txt",
    "TX": BASE / "TX.txt",
    "FL": BASE / "FL.txt",
    "AZ": BASE / "AZ.txt",
    "NV": BASE / "NV.txt",
}

OUT_UNKNOWN = BASE / "UNKNOWN_POST_NUMERIC.txt"
HOLD_NO_ZIP = BASE / "HOLD_NO_ZIP.txt"
HOLD_NO_PHONE = BASE / "HOLD_NO_PHONE.txt"
HOLD_NO_AC = BASE / "HOLD_NO_AREA_CODE.txt"

PROGRESS_EVERY = 5_000_000

re_zip = re.compile(r'(?<!\d)(\d{5})(?:-\d{4})?(?!\d)')
re_phone = re.compile(r'(?<!\d)(?:1)?(\d{10})(?!\d)')

def zip_to_state(zip5):
    z = int(zip5)
    if 90000 <= z <= 96699: return "CA"
    if 75000 <= z <= 79999 or 88500 <= z <= 88599: return "TX"
    if 32000 <= z <= 34999: return "FL"
    if 85000 <= z <= 86599: return "AZ"
    if 88900 <= z <= 89899: return "NV"
    return None

def extract_zip(line):
    m = re_zip.search(line)
    return m.group(1) if m else None

def extract_phone(line):
    m = re_phone.search(line)
    if not m:
        return None
    p = m.group(1)
    if len(set(p)) == 1:
        return None
    return p

def area_code(phone):
    return phone[:3] if phone else None

def main():
    start = time.time()
    processed = moved = no_zip = no_phone = no_ac = 0

    handles = {s: open(p, "a", encoding="utf-8", errors="ignore") for s, p in STATE_FILES.items()}
    unk = open(OUT_UNKNOWN, "w", encoding="utf-8", errors="ignore")
    hz = open(HOLD_NO_ZIP, "w", encoding="utf-8", errors="ignore")
    hp = open(HOLD_NO_PHONE, "w", encoding="utf-8", errors="ignore")
    ha = open(HOLD_NO_AC, "w", encoding="utf-8", errors="ignore")

    with open(IN_FILE, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            processed += 1

            zip5 = extract_zip(line)
            phone = extract_phone(line)
            ac = area_code(phone)

            if not zip5:
                hz.write(line)
                no_zip += 1
            elif not phone:
                hp.write(line)
                no_phone += 1
            elif not ac:
                ha.write(line)
                no_ac += 1
            else:
                state = zip_to_state(zip5)
                if state and state in handles:
                    handles[state].write(line)
                    moved += 1
                else:
                    unk.write(line)

            if processed % PROGRESS_EVERY == 0:
                print(f"Processed {processed:,} | Moved {moved:,} | NoZIP {no_zip:,} | NoPhone {no_phone:,} | NoAC {no_ac:,}", flush=True)

    for h in handles.values():
        h.close()
    unk.close()
    hz.close()
    hp.close()
    ha.close()

    print("\n=== DOUBLE-CONFIRM NUMERIC PASS COMPLETE ===")
    print(f"Processed: {processed:,}")
    print(f"Moved: {moved:,}")
    print(f"No ZIP: {no_zip:,}")
    print(f"No Phone: {no_phone:,}")
    print(f"No Area Code: {no_ac:,}")
    print(f"Minutes: {(time.time()-start)/60:.2f}")

if __name__ == "__main__":
    main()
