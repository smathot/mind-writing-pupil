## Preregistration

This experiment was preregistered on Jan 21, 2015 (<https://osf.io/yvaqs/>). All deviations from the plan are indicated below.

## Materials and availability

Participant data, experimental software, and analysis scripts are available from: TODO. This repository also includes a ready-to-use package for using our HCI on supported systems.

## Participants

Ten naive participants from the community of Aix-Marseille université were recruited (normal or uncorrected vision; age range: TODO). Participants received €90 for their participation (deviation from preregistration: We originally planned to pay €60). The experiment took approximately 10 h, divided over multiple days. Participants provided written informed consent prior to the experiment. The study was conducted with approval of the ethics committee of Aix-Marseille Université (Ref.: 2014-12-03-09), and was in accordance with the Declaration of Helsinki (7^th^ rev.).

## Software and apparatus

Eye position and pupil size were recorded monocularly with an EyeLink 1000 (SR Research, Mississauga, ON, Canada), a video-based eye tracker sampling at 1000 Hz. The right eye was recorded, unless the left eye provided a better signal. Stimuli were be presented on a 21" ViewSonic p227f CRT monitor (1280 x 1024 px, 85 Hz) running Ubuntu Linux 14.04. Testing took place in a dimly lit room. The experiment was implemented with OpenSesame [@MathôtSchreij2012] using the PsychoPy back-end [@Peirce2007] for display control and PyGaze [@Dalmaijer2014Pygaze] for eye tracking.

## General stimuli and procedure

Before each block, a nine-point eye-tracker calibration was performed. At the start of each trial, an automatic single-point recalibration ("drift correction") was performed. The display consisted of a green central fixation dot (r = 0.2°) on a gray background (TODO cd/m2). Items were presented in a circular configuration at an eccentricity of 9.2° (%FigParadigm). Items consisted of colored letters against a circular background (r = 6.2°). When only two items were presented, each item was accompanied by a mirror-symmetric placeholder (see %FigParadigm::a; this configuration was chosen because pilot experiments showed it to be the most effective of several tested configurations). The backgrounds alternated between brightness (TODO cd/m2) and darkness (TODO cd/m2) in cycles of 1.25 s (0.8 Hz). Each cycle consisted of a smooth brightness transition of 0.5 s, followed by 0.75 s of constant brightness (%FigParadigm::c).

The participant attended covertly to the target stimulus, while keeping gaze on the central fixation dot. The target was either indicated by a cue (Phase 1-3), or chosen by the participant (Phase 4). The cue was both visual (e.g., the letter 'A' shown on the display) and auditory (e.g., a synthesized French voice saying *Sélectionnez A*). The participant could replay the auditory cue at any moment by pressing the space bar. The trial ended when a selection was made (%FigParadigm::b, see Selection algorithm).

%--
figure:
 id: FigParadigm
 source: FigParadigm.svg
 caption: |
  a) Participants selected one of two (Phase 1), four (Phase 2), or eight (Phase 3) simultaneously presented stimuli. b) The target stimulus was indicated by a cue. This example shows a correct selection, because the selected stimulus ('a') matches the cue. c) During each cycle, the brightness of the stimulus gradually changed in 0.5 s, and then remained constant for 0.75.
--%

## Control for eye position

In each but the final block of each phase, the experiment was paused when fixation was lost (gaze deviated more than 2.6° from the display center for more than 10 ms), and continued when fixation was re-established. In the final block of each phase, the entire display was locked to gaze position (from now on: gaze-stabilization mode): When the eyes drifted slightly to the left, all stimuli except the central fixation dot would shift slightly to the left as well. This ascertained that selection was not driven by small eye movements in the direction of the attended stimulus [cf. @Mathôt2014JVis;@Mathôt2013Plos].

## Selection algorithm

Items are divided into two groups: bright and dark backgrounds. Each group has a parameter `l` that reflects how likely it is that the attended stimulus is part of that group. Initially, `l` is 1 for both groups. After each cycle, a proportional pupil-size difference (`ppsd`) is determined (see Pupil-size measurement). For the stimulus group that has changed from bright to dark, `l` is multiplied by the proportional pupil-size change. For the stimulus group that has changed from dark to bright, `l` is divided by the proportional pupil-size change. Cycling continues until the proportional difference between the `l`s for both groups exceeds a threshold `t`, after which the group with the highest `l` is designated as the winner. If groups consist of more than one stimulus, the losing group is discarded, and the winning group is subdivided into two new bright/ dark groups (See %FigSelection). The selection process then starts anew. This continues until the winning group contains only a single item, after which the final selection is made. The analysis is performed on-line, while the participant performs the task.

A crucial property of this algorithm is that it continues until there is sufficient evidence for reliable stimulus selection. Selection can be made faster but less accurate by reducing the threshold `t`, and slower but more accurate by increasing it.

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

Here, `ps(i)` is the median pupil size during the last 250 ms of cycle `i` (see %FigParadigm::c).

## Training program

The training program consisted of four phases. In Phases 1-3, participants were trained to make progressively more complicated selections. In Phase 4, participants wrote a short self-selected sentence using an extension of the technique trained during Phase 1-3. Training took about 10 hours, spread over multiple days (deviation from preregistration: occasionally there was more than one week between subsequent sessions TODO: CHECK).

### Phases 1-3: Selecting a predefined stimulus

In Phase 1, participants were trained to select one of two simultaneously presented stimuli. Blocks consisted of 16 selections. Participants completed at least 6 blocks, and at most 12 blocks. When a participant finished a block with 100% accuracy, after having completed at least 6 blocks, the training part of the phase was finished, and continued with a single block in gaze-stabilization mode, as described below. If, after 12 training blocks had been completed, accuracy on the last block was less than 80%, the phase was restarted with a more conservative threshold of 1.5 (default threshold = 1.375). If accuracy on the last block was less than 80% and the threshold has already been raised to 1.5, the experiment was aborted and training was considered unsuccessful. (To preview the results, this happened for only one participant.)

After the training blocks were completed, participants were tested on a single block in gaze-stabilization mode (see: Control for eye position).

Phases 2 and 3 were identical to Phase 1, except that participants selected one out of four (Phase 2) or eight (Phase 3) stimuli.

### Phase 4: Free writing

In Phase 4, participants were trained to write text by selecting letters and control characters ('backspace': a leftward arrow; 'space': a low bar; and 'accept': a square). Participants initially selected a group of four letters out of eight groups. This group subsequently 'unfolded' after which the participant selected one letter. Structurally, selecting a letter was therefore identical to a one-of-eight selection (Phase 3) followed by a one-of-four selection (Phase 2). This procedure is similar to the Hex-o-Spell P300-based human-computer interface [@Blankertz2006].

%--
figure:
 id: FigFreeWriting
 source: FigFreeWriting.svg
 caption: |
  The progressive selection procedure used for free writing. Initially, there are eight groups of letters and control characters ('backspace', 'space', and 'accept'). When one group has been selected (here 'abcd'), it unfolds into four individual letters (here 'a', 'b', 'c', and 'd'), after which a final selection is made (here 'a').
--%

First, participants familiarized themselves with the layout of the 'virtual keyboard'. Next, they practiced by writing the French word "ecrire" (without accent). Practice was completed when the word was written successfully, with a maximum of three attempts. Next, participants chose a short sentence (deviation from preregistration: several participants wanted to write a long sentence; we therefore abandoned our initial maximum of 15 characters). Participants were given two opportunities to write this sentence. Writing was considered correct when the final sentence matched the specified sentence. The use of backspace to correct mistakes during text input was permitted. Writing was considered incorrect when an incorrect sentence was accepted by the participant by selecting the 'accept' control character.
