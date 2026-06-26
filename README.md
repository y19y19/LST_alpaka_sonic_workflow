# LST Alpaka SONIC Workflow

This document explains how to set up a Triton server that loads the LST Alpaka algorithm, how to use `perf_analyzer` to benchmark LST algorithm performance on the Triton server, and how to set up the SONIC client in CMSSW.

---

## Client in CMSSW

### Step 1: Set up CMSSW

```bash
cmsrel CMSSW_16_1_0_pre4
cd CMSSW_16_1_0_pre4/src
cmsenv
```

### Step 2: Merge CMSSW changes for SONIC support

```bash
git cms-merge-topic y19y19:CMSSW_16_1_0_pre4_LST_alpaka_SONIC
scram b -j 10  # compile
```

### Step 3: Clone this repository

```bash
git clone -b CMSSW_16_1_0_pre4 git@github.com:y19y19/LST_alpaka_sonic_workflow.git sonic-workflow
cd sonic-workflow
```

> **Note:** Complete the remaining client steps after setting up the server below.

---

## Server Setup

Start from a clean environment — this can be a terminal separate from the client.

### Step 1: Compile LST Standalone

Follow the build instructions at:
https://github.com/y19y19/LST_alpaka_standalone_SONIC/tree/CMSSW_16_1_0_pre4#build-lst_cudaso-and-lst_cpuso

### Step 2: Set up and compile the LST backend

Follow the instructions at:
https://github.com/y19y19/LST_alpaka_backend/tree/CMSSW_16_1_0_pre4_backend#triton-inference-server-lst-alpaka-backend

### Step 3: Set up the `models` folder

The `models` folder can be placed in a separate location, but it must be mounted into the container when launching the server (see Step 5).

```bash
mkdir models
cd models
mkdir LST
cd LST
cp <path_to_sonic-workflow>/config.pbtxt .
mkdir 1/
cd 1/
cp -r <path_to>/lst_standalone/RecoTracker/LSTCore .
cp <path_to>/LST_alpaka_backend/build/libtriton_LST.so .
```

### Step 4: Pull the Triton server container

Skip this step if you already have the container.

```bash
singularity pull --disable-cache docker://y19y19/tritonserver:rhel8.9_v4_gcc13
```

### Step 5: Launch the server

Before launching the server on a node, run `hostname -i` to get the node's IP address — you will need it when connecting the client.

```bash
singularity run --nv -e --no-home \
  -B <path_to>/models/:/models/ \
  -B /cvmfs/:/cvmfs/ \
  <path_to>/tritonserver_rhel8.9_v4_gcc13.sif
```

Inside the container, set the required environment variables and launch the server:

```bash
export CMSSW_RELEASE_BASE=/cvmfs/cms.cern.ch/el8_amd64_gcc13/
export CMSSW_SEARCH_PATH=/cvmfs/cms.cern.ch/el8_amd64_gcc13/cms/cmssw/CMSSW_16_1_0_pre4/external/el8_amd64_gcc13/data
export GCCDIR=$CMSSW_RELEASE_BASE/external/gcc/13.4.0-6908cfdf803923e783448096ca4f0923
export TBBDIR=$CMSSW_RELEASE_BASE/external/tbb/v2022.3.0-88eb7be4ee320d604a798a914aea6359/
export OPENBLASDIR=$CMSSW_RELEASE_BASE/external/OpenBLAS/0.3.27-da4a3c2bb8ae43f3913a4a44acdb1b50/
export PATH=$GCCDIR/bin:$PATH
export LD_LIBRARY_PATH=$GCCDIR/lib64:$GCCDIR/lib:$TBBDIR/lib:$OPENBLASDIR/lib:$LD_LIBRARY_PATH
export LD_PRELOAD=/models/LST/1/LSTCore/standalone/code/rooutil/librooutil.so:/models/LST/1/LSTCore/standalone/LST/liblst_cuda.so:/models/LST/1/LSTCore/standalone/LST/liblst_cpu.so

# Launch the server
tritonserver \
  --model-repository=/models \
  --http-port=8010 \
  --grpc-port=8011 \
  --metrics-port=8012 \
  --allow-metrics=True \
  --allow-gpu-metrics=True \
  --allow-cpu-metrics=True
```

Once the server launches successfully, leave the process running — it is a persistent service. The startup logs will indicate whether the model instance is loaded on CPU or GPU, which should match what is defined in `config.pbtxt`. To change the device placement, update the instance configuration in `config.pbtxt` and relaunch the server.

---

## Client in CMSSW (continued)

### Step 4: Run the RelVal workflow

Original instructions for RelVal workflow are here:
https://github.com/y19y19/cmssw/tree/CMSSW_16_1_0_pre4_LST_alpaka_SONIC/RecoTracker/LSTCore/standalone#run-the-lst-reconstruction-in-cmssw-read-to-the-end-before-running

```bash
cd <path_to>/CMSSW_16_1_0_pre4/src
cmsenv
cmsRun TTbar_14TeV_TuneCP5_cfi_GEN_SIM.py  # generates 10 events
```

Before running the next config file (`step2_DIGI_L1TrackTrigger_L1_L1P2GT_DIGI2RAW_HLT_PU.py`), download a pileup mix file locally to avoid slow remote reads during the step. You will need a valid VOMS proxy (`voms-proxy-init`) before downloading.

```bash
xrdcp root://cmsxrootd.fnal.gov//store/relval/CMSSW_16_0_0_pre2/RelValMinBias_14TeV/GEN-SIM/150X_mcRun4_realistic_v1_STD_RegeneratedGS_Run4D121_noPU-v1/2580000/0ec3ba02-2c03-42b7-b429-ec39db7dce06.root <local_path_to_pileup_mix>
```

Open `step2_DIGI_L1TrackTrigger_L1_L1P2GT_DIGI2RAW_HLT_PU.py` and replace line 120 with the local path to the downloaded pileup mix file, then run:

```bash
cmsRun step2_DIGI_L1TrackTrigger_L1_L1P2GT_DIGI2RAW_HLT_PU.py
```

Step 3 runs the LST algorithm, which can be executed locally or through SONIC.

**Local workflow:**
```bash
cmsRun step3_RAW2DIGI_RECO_VALIDATION_DQM_PU.py
```

> To specify the accelerator for the local workflow, change line 44 in `step3_RAW2DIGI_RECO_VALIDATION_DQM_PU.py` to `'cpu'` or `'gpu-nvidia'` before running. `FastTimerService` and `ThroughputService` are included to generate a `time.json` file for event timing pie charts. See https://github.com/y19y19/circles for instructions on drawing the pie charts.

**SONIC workflow:**
```bash
cmsRun run.py --address <node_address> --port <grpc_port> --threads 1 --maxEvents 10
```

Step 4 (Optional): Harvest plots

This step was part of the original RelVal workflow and produces a ROOT file containing LST algorithm track performance plots.

```bash
cmsRun step4_HARVESTING_PU.py
```
