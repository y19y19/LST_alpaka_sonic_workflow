# CMS Event Process Timing Pie Chart

## Overview

To visualize how long each process takes per event, you need the `time.json` file generated when running the CMS config `step3_RAW2DIGI_RECO_VALIDATION_DQM_PU.py`.

Download the JSON files locally for each workflow before plotting.

## Workflows

Six workflows have been tested:

| Workflow | Description |
|---|---|
| `local_cpu` | No SONIC; accelerator set to CPU |
| `local_gpu` | No SONIC; accelerator set to GPU (nvidia) |
| `local_cpu_sonic` | SONIC enabled; Triton server hosts the LST model on CPU, running on the **same** interactive job as the CMS config |
| `local_gpu_sonic` | SONIC enabled; Triton server hosts the LST model on GPU, running on the **same** interactive job as the CMS config |
| `remote_cpu_sonic` | SONIC enabled; Triton server hosts the LST model on CPU, running on a **different** interactive job from the CMS config |
| `remote_gpu_sonic` | SONIC enabled; Triton server hosts the LST model on GPU, running on a **different** interactive job from the CMS config |

> **Note:** Running inside a scheduled interactive job limits the number of CPU cores and the amount of memory available to the job.

## Plotting the Pie Chart

Use the [`hlt_sonic`](https://github.com/y19y19/circles/tree/hlt_sonic) branch of the `circles` repository to view the pie chart locally. A browser and PHP are required.

```bash
cd /path/to/circles
php -S localhost:8080
```

Then open `http://localhost:8080` in a browser and:

1. Load the `time.json` file for the workflow you want to inspect.
2. Select **`hlt_sonic`** from the `Groups` dropdown.
3. Select **`Tracking`** for a zoomed-in view of tracking-related processes.

In the Tracking view, `lstProducer` (non-SONIC workflows) or `lstSONICProducer` (SONIC workflows) will appear depending on the selected workflow.
