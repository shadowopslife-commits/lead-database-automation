# -*- coding: utf-8 -*-

import time
import re
import os

INPUT_FILE = r"C:\ShadowOps_WORKING_CORE\OTHER_RAW.txt"
OUT_DIR = r"C:\ShadowOps_WORKING_CORE"

STATE_PATTERNS = {
    "CA": r"\b(CA|CALIFORNIA)\b",
    "TX": r"\b(TX|TEXAS)\b",
    "FL": r"\b(FL|FLORIDA)\b",
    "AZ": r"\b(AZ|ARIZONA)\b",
    "NV": r"\b(NV|NEVADA)\b",
}

compiled = {
    k: re.compile(v, re.IGNORECASE)
    for k, v in STATE_PATTERNS.items()
}

os.makedirs(OUT_DIR, exist_ok=True)

out_files = {
    k: open(os.path.join(OUT_DIR, f"OTHER_TO_{k}.txt"), "w", encoding="utf-8", errors="ignore")
    for k in STATE_PATTERNS
}

still_other = open(
    os.path.join(OUT_DIR, "STILL_OTHER.txt"),
    "w",
    encoding="utf-8",
    errors="ignore"
)

counts = {k: 0 for k in STATE_PATTERNS}
counts["STILL_OTHER"] = 0

start = time.time()
total = 0

print("BEGIN OTHER RECLASSIFICATION")
print("SOURCE:", INPUT_FILE)

with open(INPUT_FILE, "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        total += 1
        matched = False

        for state, pat in compiled.items():
            if pat.search(line):
                out_files[state].write(line)
                counts[state] += 1
                matched = True
                break

        if not matched:
            still_other.write(line)
            counts["STILL_OTHER"] += 1

        if total % 500_000 == 0:
            mins = (time.time() - start) / 60
            print(f"Processed {total:,} lines | {mins:.1f} min")

for fh in out_files.values():
    fh.close()

still_other.close()

mins = (time.time() - start) / 60

print("\nDONE — OTHER RECLASSIFIED")
print(f"TOTAL OTHER ROWS : {total:,}")
for k in ["CA", "TX", "FL", "AZ", "NV", "STILL_OTHER"]:
    print(f"{k:12} : {counts[k]:,}")
print(f"Minutes        : {mins:.1f}")
