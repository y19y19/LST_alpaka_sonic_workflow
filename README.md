# LST_alpaka_sonic_workflow

FIXME: the workflow input/output root file name does not match. 
FIXME: needs instructions of getting some PU mix files. 
```
$ cmsrel CMSSW_16_1_0_pre4
$ cd CMSSW_16_1_0_pre4/src
$ cmsenv
$ git cms-merge-topic y19y19:CMSSW_16_1_0_pre4_LST_alpaka_SONIC
$ scram b -j 10
$ git clone <this repo> sonic-workflow
$ cd sonic-workflow
$ cmsRun TTbar_14TeV_TuneCP5_cfi_GEN_SIM.py # generate root file needed by next cmsRun
$ cmsRun step2_DIGI_L1TrackTrigger_L1_L1P2GT_DIGI2RAW_HLT_PU.py # generate root file needed by next cmsRun

# Now it is the LST step that can be modified by SONIC
# Local CPU -> modify the accelerator as 'cpu' in step3
# Local CUDA ->  modify the accelerator as 'gpu-nvidia'
$ cmsRun step3_RAW2DIGI_RECO_VALIDATION_DQM_PU.py
# If you want to run it through SONIC, use run.py after the server has been set up. Get the server side address and port number
$ cmsRun run.py --address 128.211.142.16 --port 8011 --threads 1 --maxEvents 10 
# or without SONIC
$ cmsRun run.py --noSonic --maxEvents=10

# Run step 4 to see plots for LST algorithm
$ cmsRun step4_HARVESTING_PU.py
