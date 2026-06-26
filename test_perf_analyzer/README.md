# Performance Analyzer Testing for the SONIC Workflow

## Setup

Uncomment the code starting at
[`LSTSONICProducer.cc#L350`](https://github.com/y19y19/cmssw/blob/8165fab7c9dd228316f29617727d6b74e2bfe811/RecoTracker/LST/plugins/LSTSONICProducer.cc#L350)
to enable the SONIC workflow to write all input events to `LST_input.json`.

> **Note:** Input files can be very large. Limit the run to fewer than 10 events.

## Splitting Inputs

Use `split_input.py` to split the inputs into one JSON file per event and to generate the `perf_analyzer` commands for testing.

Before running the script, edit the `TRITON_URL` (the node address hosting the Triton server and its gRPC port) and `METRICS_URL` variables inside `split_input.py`.

```bash
python split_input.py LST_input.json [config_pbtxt]
```

`perf_analyzer` requires shape information for each input feature and a `config.pbtxt` file to parse the input JSON correctly. The script generates both.

## Running the Performance Analyzer

```bash
source perf_analyzer_command_event1.sh <workflow>  # e.g. remote_gpu_async
```

Four workflows are supported: `local_cpu_async`, `local_gpu_async`, `remote_cpu_async`, and `remote_gpu_async`. The appropriate workflow depends on:
- whether the Triton server is running on the same node as `perf_analyzer` (local) or a different node (remote), and
- whether the server is configured as a CPU or GPU model instance.

## Plotting Results

After benchmarking all four workflows, generate the comparison plot:

```bash
python plot_perf.py
```

This script reads the CSV files produced by `perf_analyzer` and plots each metric column, comparing all four workflows side by side.
