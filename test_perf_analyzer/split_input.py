#!/usr/bin/env python3
"""Split a multi-event Triton perf_analyzer JSON into per-event JSON files
and generate corresponding perf_analyzer shell scripts.

Usage:
    python split_input.py <input_json> [config_pbtxt]

  input_json   -- multi-event JSON produced by LSTSONICProducer
  config_pbtxt -- optional path to the model's config.pbtxt; used to determine
                  which fields are FP32 (defaults to the hardcoded list below)

Each generated shell script accepts one argument at runtime:
    ./perf_analyzer_command_event<N>.sh <output_name>
  where output_name is the base name for the CSV (e.g. "remote_gpu_async"),
  and the script writes to /workspace/<output_name>_event<N>.csv.

Output files are written to the same directory as input_json:
  LST_input_event<N>.json
  perf_analyzer_command_event<N>.sh
"""

import json
import os
import re
import stat
import sys

# ── Triton server / perf_analyzer settings ───────────────────────────────────
TRITON_URL  = "128.211.142.16:8011"
METRICS_URL = "128.211.142.16:8012/metrics"
MODEL_NAME  = "LST"

# ── Default FP32 fields (from config.pbtxt TYPE_FP32 entries) ────────────────
DEFAULT_FP32_FIELDS = {
    "see_px", "see_py", "see_pz",
    "see_dxy", "see_dz",
    "see_ptErr", "see_etaErr",
    "see_stateTrajGlbX", "see_stateTrajGlbY", "see_stateTrajGlbZ",
    "see_stateTrajGlbPx", "see_stateTrajGlbPy", "see_stateTrajGlbPz",
    "ph2_x", "ph2_y", "ph2_z",
    "ptCut",
}


def parse_fp32_fields(config_path):
    """Return the set of field names declared as TYPE_FP32 in config.pbtxt."""
    fp32_fields = set()
    current_name = None
    with open(config_path) as f:
        for line in f:
            m = re.search(r'name:\s*"([^"]+)"', line)
            if m:
                current_name = m.group(1)
            if "TYPE_FP32" in line and current_name:
                fp32_fields.add(current_name)
                current_name = None
    return fp32_fields


def ensure_floats(event, fp32_fields):
    """Cast all values in FP32 fields to Python float so json.dump writes
    decimal points even for whole-number values (e.g. 35 -> 35.0).
    perf_analyzer rejects bare integers in FP32 fields."""
    for field in fp32_fields:
        if field not in event:
            continue
        v = event[field]
        if isinstance(v, list):
            event[field] = [float(x) for x in v]
        else:
            event[field] = float(v)
    return event


def field_length(value):
    return len(value) if isinstance(value, list) else 1


def write_event_json(path, event):
    with open(path, "w") as f:
        json.dump({"data": [event]}, f)


def write_perf_script(path, event_id, json_filename, event):
    shape_flags = " \\\n    ".join(
        f"--shape {name}:{field_length(value)}"
        for name, value in event.items()
    )
    script = (
        f"#!/bin/bash\n"
        f"# Usage: $0 <output_name>\n"
        f"# Writes results to /workspace/<output_name>_event{event_id}.csv\n"
        f'OUTPUT_NAME=${{1:?\"Usage: $0 <output_name>\"}}\n'
        f"\n"
        f"perf_analyzer -v -m {MODEL_NAME} -x 1 --async"
        f" -u {TRITON_URL} \\\n"
        f"    --metrics-url {METRICS_URL} \\\n"
        f"    --measurement-interval 100000 --percentile=95 --collect-metric \\\n"
        f"    --concurrency-range 1:5:1 \\\n"
        f"    -i grpc --input-data {json_filename} \\\n"
        f"    -f /workspace/${{OUTPUT_NAME}}_event{event_id}.csv --verbose-csv \\\n"
        f"    {shape_flags}\n"
    )
    with open(path, "w") as f:
        f.write(script)
    os.chmod(path, os.stat(path).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    input_json   = sys.argv[1]
    config_pbtxt = sys.argv[2] if len(sys.argv) > 2 else None

    out_dir = os.path.dirname(os.path.abspath(input_json))

    fp32_fields = parse_fp32_fields(config_pbtxt) if config_pbtxt else DEFAULT_FP32_FIELDS
    if config_pbtxt:
        print(f"FP32 fields from {config_pbtxt}: {sorted(fp32_fields)}")

    with open(input_json) as f:
        data = json.load(f)

    events = data["data"]
    print(f"Found {len(events)} event(s) in {input_json}")

    for i, event in enumerate(events):
        event_id = i + 1
        ensure_floats(event, fp32_fields)

        json_filename = f"LST_input_event{event_id}.json"
        json_path = os.path.join(out_dir, json_filename)
        write_event_json(json_path, event)

        sh_path = os.path.join(out_dir, f"perf_analyzer_command_event{event_id}.sh")
        write_perf_script(sh_path, event_id, json_filename, event)

        print(f"  event {event_id:>2}: {json_filename}  +  perf_analyzer_command_event{event_id}.sh")

    print("Done.")


if __name__ == "__main__":
    main()
