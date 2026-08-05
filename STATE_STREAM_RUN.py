import os
import csv

OUTPUT_ROOT = r"C:\ShadowOps_CANONICAL\03_STATE_BUILD"
COUNT_FILE = os.path.join(OUTPUT_ROOT, "STATE_COUNTS.csv")

SOURCE_FILES = [
    r"D:\ShadowOps_RAW\merge_parts\MASTER_PART_001.txt",
    r"D:\ShadowOps_RAW\chunks\chunk_0023.txt",
    r"C:\ShadowOps_CANONICAL\02_CORE\ShadowOps_WORKING_CORE\CORE_001.txt",
    r"C:\ShadowOps_CANONICAL\02_CORE\ShadowOps_WORKING_CORE\CORE_002.txt",
    r"C:\ShadowOps_CANONICAL\02_CORE\ShadowOps_WORKING_CORE\CORE_003.txt",
]

STATES = {
    "CA": ["california", "los angeles", "orange", "san diego", "707", "760"],
    "TX": ["texas", "houston", "dallas", "214", "713", "832"],
    "FL": ["florida", "miami", "305"],
    "AZ": ["arizona", "phoenix"],
    "NV": ["nevada", "las vegas"],
}

os.makedirs(OUTPUT_ROOT, exist_ok=True)

state_files = {}
state_counts = {}

for state in STATES:
    path = os.path.join(OUTPUT_ROOT, f"{state}.txt")
    state_files[state] = open(path, "a", encoding="utf-8", errors="ignore")
    state_counts[state] = 0

unknown_path = os.path.join(OUTPUT_ROOT, "UNKNOWN.txt")
unknown_file = open(unknown_path, "a", encoding="utf-8", errors="ignore")
state_counts["UNKNOWN"] = 0

def classify(line):
    l = line.lower()
    for state, signals in STATES.items():
        if f",{state}," in l or l.endswith(f",{state}") or f" {state} " in l:
            return state
        for s in signals:
            if s in l:
                return state
    return "UNKNOWN"

processed = 0

for src in SOURCE_FILES:
    if not os.path.exists(src):
        continue

    print(f"[START] {src}")

    with open(src, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            processed += 1
            state = classify(line)
            if state in state_files:
                state_files[state].write(line)
            else:
                unknown_file.write(line)
            state_counts[state] += 1

            if processed % 5_000_000 == 0:
                print(f"Processed {processed:,} lines")

for f in state_files.values():
    f.close()
unknown_file.close()

with open(COUNT_FILE, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["State", "RowCount"])
    for k, v in sorted(state_counts.items()):
        writer.writerow([k, v])

print("=== STATE STREAM COMPLETE ===")
print(f"Total lines processed: {processed:,}")
print(f"Counts written to: {COUNT_FILE}")
