---
title:
 "Decoding of visual attention with pupillometry (Preregistered training program)"
author:
  Sebastiaan Mathôt^1^, Jean-Baptiste Melmi^1^, Lotje van der Linden^1^, and Stefan Van der Stigchel^2^
affiliation:
 - ^1^Aix-Marseille University, CNRS, LPC UMR 7290, Marseille, France
 - ^2^Dept. of Experimental Psychology, Helmholtz Institute, Utrecht University, The Netherlands
correspondence: |
 Address for correspondence: <s.mathot@cogsci.nl>
---

Recent studies have shown that the pupillary light response is modulated by covert visual attention [@Binda2013Bright;@Mathôt2013Plos;@Naber2013Osc;@Mathôt2014Exo]: When you covertly attend to (without looking at) a bright stimulus, your pupils constrict relative to when you attend to a dark stimulus. Here, we will use this phenomenon to decode the focus of attention on single trials, thus testing the feasibility of a human-computer interface based on pupillometry and decoding of attention.

Participants will be trained to select one of several stimuli by covertly paying attention to it. We predict that all participants will reach a selection accuracy of more than 80% during the final block of each training phase (Phase 1-3). Furthermore, using an extension of this technique, we predict that participants will be able to correctly write a short sentence of their choosing (Phase 4).

The aim of this document is to preregister a detailed description of the training program and predictions. No data has been collected yet.

## Participants

Ten naive participants from the community of Aix-Marseille université will be trained. Participants will have normal, uncorrected vision (no glasses or lenses) and be 18 - 40 years old. Participants will receive €60 for their participation. Participants will provide written informed consent prior to training. The study will be conducted with approval of the ethics committee of Aix-Marseille Université (Ref.: 2014-12-03-09).

## Exclusion criteria

Participants will be excluded when any of the following criteria is met: the participant frequently looks away from the central fixation dot; the participant blinks excessively; there are technical issues that prevent high-quality recording; the participant decides not to finish the experiment. Because it is difficult to evaluate all of these criteria automatically, exclusion will be based on evaluation by the experimenters (JBM and SM). When a participant is excluded, data collection will be stopped, and another participant will be recruited to replace the excluded participant. Participants may only be excluded based on experimenter evaluation during Phase 1 of the training program, but participants can choose to stop the experiment at any moment.

## Software and apparatus

Eye position and pupil size will be recorded monocularly with an EyeLink 1000 (SR Research, Mississauga, ON, Canada), a video-based eye tracker sampling at 1000 Hz. We will record the right eye, unless the left eye provides a better signal. Stimuli will be presented on a 21" ViewSonic p227f CRT monitor (1280x1024, 85 Hz) running Ubuntu Linux 14.04. Testing will take place in a dimly lit room.

The experiment is implemented with OpenSesame [@MathôtSchreij2012] using the PsychoPy back-end [@Peirce2007] for display control and PyGaze [@Dalmaijer2014] for eye tracking. The version of the experimental script that will be used is hosted on <http://bitbucket.org> in the `p0015-plr-bci` repository at commit [`#6638427`](https://bitbucket.org/smathot/p0015-plr-bci/commits/6638427732a60f053a8c68ad8f5a3638a100f512) in the `training` branch.

## General stimuli and procedure

Before each block, a nine-point eye-tracker calibration is performed. At the start of each trial, an automatic single-point recalibration ("drift correction") is performed. The display consists of a green central fixation dot (r = 0.2°) on a gray background. Items are presented in a circular configuration at an eccentricity of 9.2° (see %FigParadigm). Items consist of colored letters against a dark or bright background (r = 6.2°). When only two items are presented, each item is accompanied by a mirror-symmetric placeholder (see %FigParadigm::a; this configuration is chosen because pilot experiments showed it to be the most effective of several tested configurations). Participants are instructed to attend covertly to the target stimulus, while keeping gaze fixed on the central fixation dot. The target is either indicated by a cue (Phase 1-3), or chosen by the participant (Phase 4). The cue is both visual (e.g., the letter 'A' shown on the display) and auditory (e.g., a synthesized French voice saying *Sélectionnez A*). The participant can replay the auditory cue at any moment by pressing the space bar. If fixation is lost (gaze deviates more than 2.6° from the display center for more than 10 ms), the experiment is paused until fixation is re-established. If fixation is lost due to loss of calibration, the entire block is aborted and restarted. The trial ends when a selection has been made (%FigParadigm::b, see Selection algorithm).

%--
figure:
 id: FigParadigm
 source: FigParadigm.svg
 caption: |
  a) Participants select one of two (Phase 1), four (Phase 2), or eight (Phase 3) simultaneously presented stimuli. b) The target stimulus is indicated by a cue. This is an example of a correct selection, because the selected stimulus matches the cue.
--%

## Selection algorithm

Items are divided into two groups based on the brightness of their background. Each group has a likelihood `l` that the attended stimulus belongs to that group. Initially, `l` is 1 for both groups. After each cycle, a proportional pupil-size change is determined (see Pupil-size measurement). For the group that has changed from bright to dark, `l` is multiplied by the proportional pupil-size change. For the group that has changed from dark to bright, `l` is divided by the proportional pupil-size change. Cycling continues until the proportional difference between the `l`s for both groups exceeds a threshold, after which the group with the highest `l` is designated as the winner. If groups consist of more than one stimulus, the losing group is discarded, and the winning group is subdivided into two new groups. The selection process then starts anew. This continues until the winning group contains only a singly item, after which a final selection is made. (See %FigSelection.) The analysis is performed on-line, while the participant is performing the task.

%--
figure:
 id: FigSelection
 source: FigSelection.svg
 caption: |
  A schematic example of the selection procedure in the case of eight stimuli. Stimuli are grouped by the brightness of their background. One group is eliminated on each selection, after which the remaining group is subdivided a new. This procedure repeats until only a single stimulus remains.
--%


## Pupil-size measurement

The proportional pupil-size difference (`ppsd`) on cycle `i` is defined as:

	ppsd(i) = ps(i) / ps(i-1)

Here, `ps(i)` is the median pupil size on cycle `i` during the last 250 ms before the onset of the polarity change (see %FigPupilSize). The first 500 ms of each cycle is used as an adaptation period. No other filtering or preprocessing is performed.

%--
figure:
 id: FigPupilSize
 source: FigPupilSize.svg
 caption: |
  Each cycle (1250 ms) consists of an adaptation (500 ms), measurement (250 ms), and polarity-change (500 ms) period. We use the median pupil size during the measurement period.
--%

## Training program

The training program consists of four phases. During Phase 1-3 the participant will be trained to make progressively more complicated selections. During Phase 4, the participant will write a short self-selected sentence using an extension of the technique trained during Phase 1-3. Training will take place across multiple days, with a maximum of one week between consecutive sessions.

### Phase 1: Two stimuli

During Phase 1, the participant is trained to select one of two simultaneously presented stimuli. Blocks consist of 16 selections. Participants complete at least 6 blocks, and at most 12 blocks. When a participant finishes a block with 100% accuracy, after having completed at least 6 blocks, the training part of the phase is finished, and we will continue with a single block in gaze-stabilization mode, as described below.

If, after the maximum number of training blocks have been completed, accuracy on the last block is less than 80%, the phase will be restarted with a more conservative threshold of 1.5 (default threshold = 1.375). This threshold will be kept for the remainder of the training. If accuracy on the last block is less than 80% and the threshold has already been raised to 1.5, the experiment is aborted and training is considered unsuccessful.

After the training blocks have been completed, the participant will be tested on 1 block with gaze-stabilization mode enabled. In this mode of the experiment, the stimulus display is centered on gaze position using a continuous gaze-contingent algorithm. This causes the display to appear jittery, which is why gaze stabilization is not enabled during the training blocks. However, running one block in gaze-stabilization mode will allow us to verify that selection is really driven by covert visual attention, rather than by biases in gaze position.

### Phase 2: Four stimuli

Phase 2 is identical to Phase 1, except that four stimuli are presented simultaneously.

### Phase 3: Eight stimuli

Phase 2 is identical to Phase 1, except that eight stimuli are presented simultaneously.

### Phase 4: Free writing

During Phase 4, participants will be trained to write text by selecting letters and control characters (backspace, space, and return). Participants initially select a group of four letters out of eight groups. This group subsequently 'unfolds' after which the participant selects one letter. Structurally, selecting a letter is therefore identical to a one-of-eight selection (Phase 3) followed by a one-of-four selection (Phase 2).

%--
figure:
 id: FigFreeWriting
 source: FigFreeWriting.svg
 caption: |
  The progressive selection procedure used for free writing.
--%

First, participants will be given the chance to familiarize themselves with the layout of the 'virtual keyboard'. Next, they will practice by writing the French word "ecrire" (without accent). Practice is completed when the word has been successfully written, or after three tries. Next, participants choose a short sentence of 10 to 15 characters. This sentence may not contain accents or punctuation. Participants are given two opportunities to write this sentence. Writing is considered correct when the final sentence matches the specified sentence. The use of backspace to correct mistakes during text input is permitted. Writing is considered incorrect when an incorrect sentence is accepted by the participant by entering the return control character, or when the participant enters more than 20 characters.
