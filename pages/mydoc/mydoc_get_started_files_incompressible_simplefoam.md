---
title: Example of simplified files_Incompressible
keywords: new case, faq
summary:
sidebar: mydoc_sidebar
permalink: mydoc_get_started_files_incompressible_simplefoam.html
folder: mydoc
---

Here is an example of simplified files_Incompressible to speed up the DAFoam repo compilation speed, assuming we want to test a new change for DASimpleFoam with the SA turbulence model and force objective.

<pre>
DAUtility/DAUtility.C

DACheckMesh/DACheckMesh.C
DACheckMesh/checkGeometry.C
DACheckMesh/checkTools.C

DAOption/DAOption.C

DARegDb/DARegDbSinglePhaseTransportModel.C
DARegDb/DARegDbTurbulenceModelIncompressible.C

DAModel/DATurbulenceModel/DATurbulenceModel.C
DAModel/DATurbulenceModel/DASpalartAllmaras.C

DAModel/DARadiationModel/DARadiationModel.C
DAModel/DARadiationModel/DAP1.C

DAModel/DAModel.C

DAStateInfo/DAStateInfo.C
DAStateInfo/DAStateInfoSimpleFoam.C

DAMotion/DAMotion.C
DAMotion/DAMotionDummy.C

DAIndex/DAIndex.C

DAField/DAField.C

DAObjFunc/DAObjFunc.C
DAObjFunc/DAObjFuncForce.C

DAFvSource/DAFvSource.C
DAFvSource/DAFvSourceActuatorDisk.C

DAResidual/DAResidual.C
DAResidual/DAResidualDummy.C
DAResidual/DAResidualSimpleFoam.C

DAColoring/DAColoring.C

DAJacCon/DAJacCon.C
DAJacCon/DAJacCondRdW.C
DAJacCon/DAJacCondFdW.C
DAJacCon/DAJacConDummy.C

DAPartDeriv/DAPartDeriv.C
DAPartDeriv/DAPartDerivdRdW.C
DAPartDeriv/DAPartDerivdFdW.C

DALinearEqn/DALinearEqn.C

DASolver/DASolver.C
DASolver/DASimpleFoam/DASimpleFoam.C

models/dummyTurbulenceModel/makeDummyTurbulenceModelIncompressible.C
models/meshWaveFrozen/meshWaveFrozenPatchDistMethod.C
models/MRFDF/MRFZoneDF.C
models/MRFDF/MRFZoneListDF.C
models/MRFDF/IOMRFZoneListDF.C

LIB = $(DAFOAM_ROOT_PATH)/OpenFOAM/sharedLibs/libDAFoamIncompressible$(DF_LIB_SUFFIX)

</pre>

{% include links.html %}
