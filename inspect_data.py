#!/usr/bin/env python
"""
Inspect the actual structure of NeurIPS 2025 data.
"""

import sys
from pathlib import Path
import json

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from neurips_abstracts.downloader import download_neurips_data


def main():
    print("Inspecting NeurIPS 2025 Data Structure")
    print("=" * 80)

    try:
        # Download the data
        print("\nDownloading data...")
        data = download_neurips_data(year=2025)

        print(f"\nTop-level structure:")
        print(f"  Type: {type(data)}")
        print(f"  Keys: {list(data.keys())}")

        # Inspect each key
        for key in data.keys():
            value = data[key]
            print(f"\n'{key}':")
            print(f"  Type: {type(value)}")

            if isinstance(value, list):
                print(f"  Length: {len(value)}")
                if value:
                    print(f"  First item type: {type(value[0])}")
                    if isinstance(value[0], dict):
                        print(f"  First item keys: {list(value[0].keys())}")
                        # Show first item
                        print(f"\n  Sample item:")
                        for k, v in list(value[0].items())[:10]:
                            if isinstance(v, str) and len(v) > 80:
                                print(f"    {k}: {v[:80]}...")
                            elif isinstance(v, list) and len(v) > 3:
                                print(f"    {k}: [list of {len(v)} items]")
                            else:
                                print(f"    {k}: {v}")
            elif isinstance(value, dict):
                print(f"  Dict keys: {list(value.keys())}")
            else:
                print(f"  Value: {value}")

        # If 'results' exists, show more detail
        if "results" in data:
            results = data["results"]
            print(f"\n{'=' * 80}")
            print(f"\nDetailed 'results' analysis:")
            print(f"  Total items: {len(results)}")

            if results and isinstance(results[0], dict):
                # Show all keys from first item
                print(f"\n  All keys in first result:")
                for key in results[0].keys():
                    value = results[0][key]
                    if isinstance(value, str):
                        preview = value[:60] + "..." if len(value) > 60 else value
                        print(f"    - {key}: '{preview}'")
                    elif isinstance(value, list):
                        print(f"    - {key}: [list with {len(value)} items]")
                        if value and isinstance(value[0], dict):
                            print(f"        First item keys: {list(value[0].keys())}")
                    elif isinstance(value, dict):
                        print(f"    - {key}: {{dict with keys: {list(value.keys())}}}")
                    else:
                        print(f"    - {key}: {value}")

        print("\n" + "=" * 80)
        print("Inspection complete!")

    except Exception as e:
        print(f"\nError: {type(e).__name__}: {e}")
        import traceback

        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
