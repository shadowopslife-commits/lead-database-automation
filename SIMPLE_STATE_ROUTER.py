import os

BASE = r"C:\ShadowOps_CANONICAL\03_STATE_BUILD"
INPUT = os.path.join(BASE, "UNKNOWN_REMAINING.txt")
OUTPUT_UNKNOWN = os.path.join(BASE, "UNKNOWN_FINAL.txt")

STATES = ["CA","TX","FL","AZ","NV","OR","UT","ID","VA","WA","NY","NJ","PA","IL","OH","GA","NC","SC","CO"]

state_files = {st: open(os.path.join(BASE, f"{st}.txt"), "a", encoding="utf-8", errors="ignore")
               for st in STATES}

unknown_out = open(OUTPUT_UNKNOWN, "w", encoding="utf-8", errors="ignore")

processed = 0
routed = 0

print("=== SIMPLE STATE ROUTER STARTED ===", flush=True)
print(f"Input: {INPUT}", flush=True)

with open(INPUT, "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        processed += 1
        line_upper = line.upper()
        matched = False

        for st in STATES:
            token = f",{st},"
            if token in line_upper:
                state_files[st].write(line)
                routed += 1
                matched = True
                break

        if not matched:
            unknown_out.write(line)

        if processed % 1_000_000 == 0:
            print(f"Processed {processed:,} | Routed {routed:,}", flush=True)

for fh in state_files.values():
    fh.close()
unknown_out.close()

print("=== SIMPLE ROUTE COMPLETE ===", flush=True)
print(f"Processed total: {processed:,}", flush=True)
print(f"Routed total: {routed:,}", flush=True)
print(f"Remaining UNKNOWN written to: {OUTPUT_UNKNOWN}", flush=True)
