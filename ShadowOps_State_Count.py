import os, re, time, csv
from collections import defaultdict

CORE_DIRS = [
    r"C:\ShadowOps_WORKING_CORE",
    r"D:\ShadowOps_WORKING_CORE",
    r"E:\ShadowOps_WORKING_CORE"
]

REPORT_DIR = r"D:\ShadowOps_REPORTS"
os.makedirs(REPORT_DIR, exist_ok=True)

REPORT_CSV = os.path.join(REPORT_DIR, "STATE_BASELINE_COUNTS.csv")

STATES = {
    "CA": ["CA", "CALIFORNIA"],
    "TX": ["TX", "TEXAS"],
    "FL": ["FL", "FLORIDA"],
    "AZ": ["AZ", "ARIZONA"],
    "NV": ["NV", "NEVADA"]
}

ZIP_RANGES = {
    "CA": ("90", "96"),
    "TX": ("75", "79"),
    "FL": ("32", "34"),
    "AZ": ("85", "86"),
    "NV": ("89", "89")
}

def detect_state(line):
    u = line.upper()
    for st, keys in STATES.items():
        for k in keys:
            if f",{k}," in u or u.endswith(f",{k}") or f" {k} " in u:
                return st
    for z in re.findall(r"\b\d{5}\b", u):
        for st,(lo,hi) in ZIP_RANGES.items():
            if lo <= z[:2] <= hi:
                return st
    return "OTHER"

counts = defaultdict(int)
total = 0
start = time.time()

print("SCANNING CORE FILES...")

for d in CORE_DIRS:
    if not os.path.exists(d): 
        continue
    for f in os.listdir(d):
        if not f.startswith("CORE_") or not f.endswith(".txt"):
            continue
        p = os.path.join(d,f)
        print("Scanning", p)
        with open(p, "r", errors="ignore") as fh:
            for line in fh:
                total += 1
                counts[detect_state(line)] += 1
                if total % 5_000_000 == 0:
                    print(f"Processed {total:,} | {(time.time()-start)/60:.1f} min")

with open(REPORT_CSV, "w", newline="") as c:
    w = csv.writer(c)
    w.writerow(["STATE","COUNT"])
    for k in ["CA","TX","FL","AZ","NV","OTHER"]:
        w.writerow([k, counts[k]])

print("DONE")
print("TOTAL:", total)
for k in ["CA","TX","FL","AZ","NV","OTHER"]:
    print(k, counts[k])
