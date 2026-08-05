import os, csv, time
from collections import Counter, defaultdict

CORE_FILES = [
    r"C:\ShadowOps_WORKING_CORE\CORE_001.txt",
    r"C:\ShadowOps_WORKING_CORE\CORE_002.txt",
    r"C:\ShadowOps_WORKING_CORE\CORE_003.txt"
]

OUT_DIR = r"D:\ShadowOps_OTHER_PREVIEW"
if not os.path.exists(OUT_DIR):
    OUT_DIR = r"C:\ShadowOps_OTHER_PREVIEW"
os.makedirs(OUT_DIR, exist_ok=True)

SAMPLE_OUT = os.path.join(OUT_DIR, "OTHER_PREVIEW_SAMPLE.csv")
SUMMARY_OUT = os.path.join(OUT_DIR, "OTHER_STATE_SIGNAL_SUMMARY.csv")
COLUMN_OUT  = os.path.join(OUT_DIR, "OTHER_COLUMN_STATE_HITS.csv")

STATE_ABBR = {"CA","TX","FL","AZ","NV"}
STATE_FULL = {"CALIFORNIA","TEXAS","FLORIDA","ARIZONA","NEVADA"}
ZIP_RANGES = {
    "CA": range(90000,97000),
    "TX": range(75000,80000),
    "FL": range(32000,35000),
    "AZ": range(85000,87000),
    "NV": range(89000,90000)
}

def detect_state(token):
    t = token.strip().upper()
    if t in STATE_ABBR: return t
    if t in STATE_FULL: return t[:2]
    if t.isdigit() and len(t)==5:
        z = int(t)
        for s,r in ZIP_RANGES.items():
            if z in r: return s
    return None

sample = []
state_counts = Counter()
column_hits = defaultdict(Counter)

start = time.time()
processed = 0

for file in CORE_FILES:
    if not os.path.exists(file):
        continue
    print(f"Scanning {file}")
    with open(file, encoding="utf-8", errors="ignore") as f:
        for line in f:
            processed += 1
            cols = line.rstrip().split(",")
            found = set()

            for i,c in enumerate(cols):
                s = detect_state(c)
                if s:
                    found.add(s)
                    column_hits[i][s] += 1

            if not found:
                state_counts["OTHER"] += 1
                if len(sample) < 1000:
                    sample.append(cols)
            else:
                for s in found:
                    state_counts[s] += 1

            if processed % 5_000_000 == 0:
                mins = round((time.time()-start)/60,1)
                print(f"Processed {processed:,} | OTHER {state_counts['OTHER']:,} | {mins} min")

with open(SAMPLE_OUT,"w",newline="",encoding="utf-8") as f:
    csv.writer(f).writerows(sample)

with open(SUMMARY_OUT,"w",newline="",encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["STATE","COUNT"])
    for k,v in state_counts.items():
        w.writerow([k,v])

with open(COLUMN_OUT,"w",newline="",encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["COLUMN","STATE","HITS"])
    for col,states in column_hits.items():
        for s,c in states.items():
            w.writerow([col,s,c])

print("\\n=== OTHER ANALYSIS COMPLETE ===")
print("Output folder:", OUT_DIR)
