# Output Validation for the CMSSW Workflow

## Setup

Uncomment the lines starting at
[`LSTOutputConverter.cc#L189`](https://github.com/y19y19/cmssw/blob/8165fab7c9dd228316f29617727d6b74e2bfe811/RecoTracker/LST/plugins/LSTOutputConverter.cc#L189)
to enable writing the per-event output to a JSON file named `LST_output.json` when running the CMSSW workflow. 

Do `scram b` to recompile LST package in cmssw.

Both the local workflow and the SONIC workflow can generate this JSON file.

## Running the Validation

Validate the output by running:

```bash
python output_validation.py
```

`output_validation.py` expects input files named in the format:

```
LST_output_<local|SONIC>_<CPU|GPU>_run<1-5>.json
```

It compares 5 trials for each of the 4 workflows (local CPU, local GPU, SONIC CPU, SONIC GPU) and produces a validation plot.
