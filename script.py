import os
import glob

def load_properties(filepath):
    props = {}
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            props[key.strip()] = value.strip()
    return props

def check_keys(baseline_file, other_files):
    baseline = load_properties(baseline_file)
    baseline_keys = set(baseline.keys())

    table = []
    for fname in other_files:
        d = load_properties(fname)
        missing = baseline_keys - set(d.keys())
        shortname = os.path.splitext(os.path.basename(fname))[0]
        status = "✅  All keys" if not missing else f"⚠️ \t{len(missing)} missing"
        table.append([shortname, len(baseline_keys), len(d.keys()), len(missing), status])

    # Print table header
    print(f"{'File':<20} {'Baseline Keys':<15} {'File Keys':<10} {'Missing':<10} {'Status'}")
    print("-"*70)
    for row in table:
        print(f"{row[0]:<20} {row[1]:<15} {row[2]:<10} {row[3]:<10} {row[4]}")

if __name__ == "__main__":
    # Use relative paths from current directory
    baseline_file = "./themes/src/main/resources/theme/base/admin/messages/messages_en.properties"
    other_files = glob.glob(
        "./themes/src/main/resources-community/theme/base/admin/messages/messages_*.properties"
    )

    if not os.path.exists(baseline_file):
        print("Baseline file not found!")
    elif not other_files:
        print("No other properties files found!")
    else:
        check_keys(baseline_file, other_files)