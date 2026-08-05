import re
from pathlib import Path

INPUT = Path(r"D:\ShadowOps_CANONICAL\UNKNOWN_SHRINK_STEP1\OTHER_ZIP_REMAINING_NO_CA_AZ.txt")
OUT_DIR = Path(r"D:\ShadowOps_CANONICAL\MISC_HOLD")
OUT_MISC = OUT_DIR / "UNROUTABLE_LEADS.txt"
OUT_JUNK = INPUT.with_name("OTHER_ZIP_PURE_JUNK.txt")

OUT_DIR.mkdir(parents=True, exist_ok=True)

PHONE_RE = re.compile(r'(^|[^0-9])([2-9][0-9]{2})([2-9][0-9]{6})([^0-9]|$)')
STREET_RE = re.compile(r'\b\d{1,6}\s+\w+')
STATE_RE = re.compile(r'\b(AL|AK|AZ|AR|CA|CO|CT|DE|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VT|VA|WA|WV|WI|WY)\b', re.I)

processed = misc = junk = 0

with INPUT.open("r", errors="ignore") as fin, \
     OUT_MISC.open("a", encoding="utf-8") as fout_misc, \
     OUT_JUNK.open("w", encoding="utf-8") as fout_junk:

    for line in fin:
        processed += 1
        low = line.lower()

        has_phone = PHONE_RE.search(low)
        has_street = STREET_RE.search(low)
        has_state = STATE_RE.search(low)

        if has_phone and has_street and not has_state:
            fout_misc.write(line)
            misc += 1
        else:
            fout_junk.write(line)
            junk += 1

        if processed % 25000 == 0:
            print(f"Processed {processed:,} | Misc {misc:,} | Junk {junk:,}")

print("=== UNROUTABLE LEAD ISOLATION COMPLETE ===")
print(f"Processed: {processed:,}")
print(f"Moved to MISC: {misc:,}")
print(f"Junk left: {junk:,}")
print(f"MISC file: {OUT_MISC}")
print(f"Junk file: {OUT_JUNK}")
