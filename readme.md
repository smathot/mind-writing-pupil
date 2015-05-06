# The mind-writing pupil

Experimental resources for:

Mathôt, S., Melmi, J-B., Van der Linden, L., & Van der Stigchel, S. (in prep.) *The Mind-Writing Pupil: A Human-Computer Interface Based on Pupillometry and Decoding of Covert Visual Attention [working title]*.

## Preregistration

The training program was preregistered on the Open-Science Framework prior to data collection. See:

- <https://osf.io/s9j8z/>

## Data

The raw data in can be found in the folder `data`.

- Format: EyeLink `.edf`
- The following blocks are missing:
	- `data/PP11/Phase 3/PP110307.edf`
	- `data/PP03/Phase 1/PP030111.edf`
- The following subjects dropped out voluntarily and were replaced:
	- PP01
	- PP05
- During data analysis, participant numbers are remapped to restore contiguous numbering:
	- PP11 -> PP01 [tested as -> appears in analysis as]
	- PP12 -> PP05
	- PP10 -> PP08
	- PP08 -> PP10

## Analysis

- Scripts for the analysis of Phase 1 - 3 are in the folder `analysis`.
- Scripts for the analysis of Phase 4 are in the folder `analysis4`.

## Experiment

The experiment script can be found in the folder `experiment`.
