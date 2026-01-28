#!/usr/bin/env python3
"""
Parse lcov.info and print coverage summary table.
Exit with code 1 if line coverage < threshold.
"""

import sys
import re
from collections import defaultdict

def parse_lcov(lcov_path):
    file_data = defaultdict(lambda: {"total_lines": 0, "covered_lines": 0})
    current_file = None

    with open(lcov_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith("SF:"):
                # SF:/path/to/file.rs
                current_file = line[3:].strip()
                # Normalize path: remove leading dirs if needed
                # Keep only relative path from project root
                if "src/" in current_file:
                    current_file = current_file.split("src/", 1)[-1]
                elif "tests/" in current_file:
                    current_file = current_file.split("tests/", 1)[-1]
                else:
                    # Keep as-is if not in src/ or tests/
                    pass
            elif line.startswith("DA:") and current_file:
                # DA:line_number,hit_count
                parts = line[3:].split(",")
                if len(parts) == 2:
                    hit_count = int(parts[1])
                    file_data[current_file]["total_lines"] += 1
                    if hit_count > 0:
                        file_data[current_file]["covered_lines"] += 1

    return dict(file_data)

def calculate_coverage(data):
    total_covered = sum(v["covered_lines"] for v in data.values())
    total_lines = sum(v["total_lines"] for v in data.values())
    overall_pct = (total_covered / total_lines * 100) if total_lines > 0 else 0.0

    file_coverage = {}
    for file, stats in data.items():
        if stats["total_lines"] > 0:
            pct = stats["covered_lines"] / stats["total_lines"] * 100
        else:
            pct = 0.0
        file_coverage[file] = {
            "covered": stats["covered_lines"],
            "total": stats["total_lines"],
            "pct": pct
        }

    return file_coverage, total_covered, total_lines, overall_pct

def print_table(file_coverage, total_covered, total_lines, overall_pct, threshold=30.0):
    print("\n📊 Coverage Report")
    print("-" * 60)
    print(f"{'File':<30} | {'Lines':>8} | {'Covered':>8} | {'%':>6}")
    print("-" * 60)

    for file in sorted(file_coverage.keys()):
        stats = file_coverage[file]
        print(f"{file:<30} | {stats['total']:>8} | {stats['covered']:>8} | {stats['pct']:>5.1f}%")

    print("-" * 60)
    print(f"{'TOTAL':<30} | {total_lines:>8} | {total_covered:>8} | {overall_pct:>5.1f}%")
    print("-" * 60)

    if overall_pct < threshold:
        print(f"\n❌ FAIL: Coverage ({overall_pct:.1f}%) is below threshold ({threshold}%)")
        sys.exit(1)
    else:
        print(f"\n✅ PASS: Coverage ({overall_pct:.1f}%) meets threshold ({threshold}%)")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 check_coverage.py <lcov_file> [threshold]")
        sys.exit(1)

    lcov_path = sys.argv[1]
    threshold = float(sys.argv[2]) if len(sys.argv) > 2 else 30.0

    try:
        data = parse_lcov(lcov_path)
        if not data:
            print("⚠️ No coverage data found in LCOV file.")
            sys.exit(1)

        file_cov, total_cov, total_lines, overall_pct = calculate_coverage(data)
        print_table(file_cov, total_cov, total_lines, overall_pct, threshold)

    except FileNotFoundError:
        print(f"❌ Error: File '{lcov_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error parsing LCOV: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()