"""
Fetch official Yandex Market geo regions and build lr_code -> region_name map.

This script does NOT guess or hardcode anything. It must be run to generate
backend/data/region_lr_map.csv, which is the only allowed mapping source.
"""

import csv
import sys
from pathlib import Path

OUT_PATH = Path(__file__).resolve().parents[1] / "data" / "region_lr_map.csv"


def build_map():
    """
    No automatic source available in this environment.
    Provide region_lr_map.csv manually from official Yandex geo export.
    """
    raise RuntimeError(
        "No deterministic lr_code source available. Please provide backend/data/region_lr_map.csv "
        "exported from official Yandex Market geo regions. No hardcoded mapping is allowed."
    )


if __name__ == "__main__":
    try:
        build_map()
    except Exception as exc:
        sys.stderr.write(f"Failed to build region_lr_map.csv: {exc}\n")
        sys.exit(1)
