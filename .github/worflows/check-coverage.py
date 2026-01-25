import json
import sys

THRESHOLD = 33.0  # процент

with open("coverage.json") as f:
    data = json.load(f)

total = data["summary"]

metrics = {
    "Function Coverage": total["functions"]["percent"],
    "Line Coverage": total["lines"]["percent"],
    "Region Coverage": total["regions"]["percent"],
    "Branch Coverage": total["branches"]["percent"],
}

all_passed = True
for name, value in metrics.items():
    if value < THRESHOLD:
        print(f"❌ {name}: {value:.2f}% < {THRESHOLD}%")
        all_passed = False
    else:
        print(f"✅ {name}: {value:.2f}%")

if not all_passed:
    print(f"\n⚠️  Coverage below {THRESHOLD}% in one or more categories!")
    sys.exit(1)
else:
    print(f"\n🎉 All coverage metrics ≥ {THRESHOLD}%")