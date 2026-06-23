# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: step4 -s HARVESTING:@trackingOnlyValidation+@trackingOnlyDQM --conditions auto:phase2_realistic_T35 --mc --geometry ExtendedRun4D121 --scenario pp --filetype DQM --era Phase2C22I13M9 --procModifiers trackingIters01,trackingLST -n 10 --pileup AVE_200_BX_25ns --pileup_input das:/RelValMinBias_14TeV/CMSSW_16_0_0_pre2-150X_mcRun4_realistic_v1_STD_RegeneratedGS_Run4D121_noPU-v1/GEN-SIM
import FWCore.ParameterSet.Config as cms

from Configuration.Eras.Era_Phase2C22I13M9_cff import Phase2C22I13M9
from Configuration.ProcessModifiers.trackingIters01_cff import trackingIters01
from Configuration.ProcessModifiers.trackingLST_cff import trackingLST

process = cms.Process('HARVESTING',Phase2C22I13M9,trackingIters01,trackingLST)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mix_POISSON_average_cfi')
process.load('Configuration.Geometry.GeometryExtendedRun4D121Reco_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.DQMSaverAtRunEnd_cff')
process.load('Configuration.StandardSequences.Harvesting_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(10),
    output = cms.optional.untracked.allowed(cms.int32,cms.PSet)
)

# Input source
process.source = cms.Source("DQMRootSource",
    fileNames = cms.untracked.vstring('file:step3_RAW2DIGI_RECO_VALIDATION_DQM_PU_inDQM.root')
)

process.options = cms.untracked.PSet(
    IgnoreCompletely = cms.untracked.vstring(),
    Rethrow = cms.untracked.vstring('ProductNotFound'),
    TryToContinue = cms.untracked.vstring(),
    accelerators = cms.untracked.vstring('*'),
    allowUnscheduled = cms.obsolete.untracked.bool,
    canDeleteEarly = cms.untracked.vstring(),
    deleteNonConsumedUnscheduledModules = cms.untracked.bool(True),
    dumpOptions = cms.untracked.bool(False),
    emptyRunLumiMode = cms.obsolete.untracked.string,
    eventSetup = cms.untracked.PSet(
        forceNumberOfConcurrentIOVs = cms.untracked.PSet(
            allowAnyLabel_=cms.required.untracked.uint32
        ),
        numberOfConcurrentIOVs = cms.untracked.uint32(0)
    ),
    fileMode = cms.untracked.string('FULLMERGE'),
    forceEventSetupCacheClearOnNewRun = cms.untracked.bool(False),
    holdsReferencesToDeleteEarly = cms.untracked.VPSet(),
    makeTriggerResults = cms.obsolete.untracked.bool,
    modulesToCallForTryToContinue = cms.untracked.vstring(),
    modulesToIgnoreForDeleteEarly = cms.untracked.vstring(),
    numberOfConcurrentLuminosityBlocks = cms.untracked.uint32(0),
    numberOfConcurrentRuns = cms.untracked.uint32(1),
    numberOfStreams = cms.untracked.uint32(0),
    numberOfThreads = cms.untracked.uint32(1),
    printDependencies = cms.untracked.bool(False),
    sizeOfStackForThreadsInKB = cms.optional.untracked.uint32,
    throwIfIllegalParameter = cms.untracked.bool(True),
    wantSummary = cms.untracked.bool(False)
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('step4 nevts:10'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

# Additional output definition

# Other statements
process.mix.input.nbPileupEvents.averageNumber = cms.double(200.000000)
process.mix.bunchspace = cms.int32(25)
process.mix.minBunch = cms.int32(-3)
process.mix.maxBunch = cms.int32(3)
process.mix.input.fileNames = cms.untracked.vstring(['/store/relval/CMSSW_16_0_0_pre2/RelValMinBias_14TeV/GEN-SIM/150X_mcRun4_realistic_v1_STD_RegeneratedGS_Run4D121_noPU-v1/2580000/0ec3ba02-2c03-42b7-b429-ec39db7dce06.root', '/store/relval/CMSSW_16_0_0_pre2/RelValMinBias_14TeV/GEN-SIM/150X_mcRun4_realistic_v1_STD_RegeneratedGS_Run4D121_noPU-v1/2580000/1228fe59-9833-4fd7-829c-15a2edfd9d93.root', '/store/relval/CMSSW_16_0_0_pre2/RelValMinBias_14TeV/GEN-SIM/150X_mcRun4_realistic_v1_STD_RegeneratedGS_Run4D121_noPU-v1/2580000/2c90ab5a-7ce3-49bf-8eac-2d2131afed9d.root', '/store/relval/CMSSW_16_0_0_pre2/RelValMinBias_14TeV/GEN-SIM/150X_mcRun4_realistic_v1_STD_RegeneratedGS_Run4D121_noPU-v1/2580000/5ec70cd3-b366-4283-b648-b4b38811aede.root', '/store/relval/CMSSW_16_0_0_pre2/RelValMinBias_14TeV/GEN-SIM/150X_mcRun4_realistic_v1_STD_RegeneratedGS_Run4D121_noPU-v1/2580000/762324d1-30be-4515-ad0d-08f4b45b21d2.root', '/store/relval/CMSSW_16_0_0_pre2/RelValMinBias_14TeV/GEN-SIM/150X_mcRun4_realistic_v1_STD_RegeneratedGS_Run4D121_noPU-v1/2580000/7f3bd434-8375-4dca-b851-4bf76b7438a4.root', '/store/relval/CMSSW_16_0_0_pre2/RelValMinBias_14TeV/GEN-SIM/150X_mcRun4_realistic_v1_STD_RegeneratedGS_Run4D121_noPU-v1/2580000/8b0e2219-3b73-46ad-a67e-20fc3f8231f8.root', '/store/relval/CMSSW_16_0_0_pre2/RelValMinBias_14TeV/GEN-SIM/150X_mcRun4_realistic_v1_STD_RegeneratedGS_Run4D121_noPU-v1/2580000/b034d0ba-c283-43d2-9724-1ce77072ba5e.root', '/store/relval/CMSSW_16_0_0_pre2/RelValMinBias_14TeV/GEN-SIM/150X_mcRun4_realistic_v1_STD_RegeneratedGS_Run4D121_noPU-v1/2580000/d9090beb-e176-45eb-9a13-29cfa7e1b479.root', '/store/relval/CMSSW_16_0_0_pre2/RelValMinBias_14TeV/GEN-SIM/150X_mcRun4_realistic_v1_STD_RegeneratedGS_Run4D121_noPU-v1/2580000/ddecc010-3486-43a2-a483-60fe9b957efb.root', '/store/relval/CMSSW_16_0_0_pre2/RelValMinBias_14TeV/GEN-SIM/150X_mcRun4_realistic_v1_STD_RegeneratedGS_Run4D121_noPU-v1/2580000/e2ad0add-b051-4f54-8fa0-332c35e03166.root'])
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase2_realistic_T35', '')

# Path and EndPath definitions
process.alcaHarvesting = cms.Path()
process.dqmHarvesting = cms.Path(process.DQMOffline_SecondStep+process.DQMOffline_Certification)
process.dqmHarvestingExpress = cms.Path(process.DQMOffline_SecondStep_Express)
process.dqmHarvestingExtraHLT = cms.Path(process.DQMOffline_SecondStep_ExtraHLT+process.DQMOffline_Certification)
process.dqmHarvestingFakeHLT = cms.Path(process.DQMOffline_SecondStep_FakeHLT+process.DQMOffline_Certification)
process.dqmHarvestingPOGMC = cms.Path(process.DQMOffline_SecondStep_PrePOGMC)
process.genHarvesting = cms.Path(process.postValidation_gen)
process.validationHarvesting = cms.Path(process.hltpostvalidation)
process.validationHarvestingFS = cms.Path(process.recoMuonPostProcessors+process.postValidationTracking+process.MuIsoValPostProcessor+process.calotowersPostProcessor+process.hcalSimHitsPostProcessor+process.hcaldigisPostProcessor+process.hcalrechitsPostProcessor+process.electronPostValidationSequence+process.photonPostProcessor+process.pfJetClient+process.pfMETClient+process.pfJetResClient+process.pfElectronClient+process.rpcRecHitPostValidation_step+process.makeBetterPlots+process.bTagCollectorSequenceMCbcl+process.METPostProcessor+process.L1GenPostProcessor+process.bdHadronTrackPostProcessor+process.MuonCSCDigisPostProcessors+process.MuonGEMHitsPostProcessors+process.MuonGEMDigisPostProcessors+process.MuonGEMRecHitsPostProcessors+process.hgcalPostProcessor+process.trackerphase2ValidationHarvesting+process.postValidation_gen)
process.validationHarvestingHI = cms.Path(process.postValidationHI)
process.validationHarvestingMiniAOD = cms.Path(process.JetPostProcessorHarvesting+process.METPostProcessorHarvesting+process.bTagMiniValidationHarvesting+process.postValidationMiniAOD)
process.validationHarvestingNoHLT = cms.Path(process.postValidation+process.postValidation_gen)
process.validationHarvestingPhase2 = cms.Path(process.hltpostvalidation)
process.validationpreprodHarvesting = cms.Path(process.postValidation_preprod+process.hltpostvalidation_preprod+process.postValidation_gen)
process.validationpreprodHarvestingNoHLT = cms.Path(process.postValidation_preprod+process.postValidation_gen)
process.validationprodHarvesting = cms.Path(process.hltpostvalidation_prod+process.postValidation_gen)
process.postValidation_trackingOnly_step = cms.Path(process.postValidation_trackingOnly)
process.DQMHarvestTracking_step = cms.Path(process.DQMHarvestTracking)
process.dqmsave_step = cms.Path(process.DQMSaver)

# Schedule definition
process.schedule = cms.Schedule(process.postValidation_trackingOnly_step,process.DQMHarvestTracking_step,process.dqmsave_step)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)



# Customisation from command line

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
