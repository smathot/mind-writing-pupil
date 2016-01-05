## Preregistration

This experiment was preregistered on Jan 21, 2015 (<https://osf.io/yvaqs/>). Whenever a deviation from registration occurred, it is indicated in the sections below.

## Materials and availability

Participant data, experimental software, and analysis scripts are available from: <https://github.com/smathot/mind-writing-pupil>. This repository also includes a ready-to-use package for using our HCI with supported systems (currently tested with EyeLink and EyeTribe eye trackers, and Windows and Linux operating systems). A screencast of our method is available on-line: <https://youtu.be/cGfkD2opTz4>

## Participants

Ten naive participants from the community of Aix-Marseille Université were recruited (normal or corrected vision; 7 women; age range: 20-25). Participants received €90 for their participation (deviation from preregistration: We originally planned to pay €60). Participants provided written informed consent prior to the experiment. The study was conducted with approval of the ethics committee of Aix-Marseille Université (Ref.: 2014-12-03-09), and conformed to the Declaration of Helsinki (7^th^ rev.).

## Software and apparatus

Eye position and pupil size were recorded monocularly with an EyeLink 1000 (SR Research, Mississauga, ON, Canada), a video-based eye tracker sampling at 1000 Hz. The right eye was recorded, unless the left eye provided a better signal. Stimuli were presented on a 21" ViewSonic p227f CRT monitor (1280 x 1024 px, 85 Hz) running Ubuntu Linux 14.04. Testing took place in a dimly lit room. The experiment was implemented with OpenSesame [@MathôtSchreij2012] using the PsychoPy back-end [@Peirce2007] for display control and PyGaze [@Dalmaijer2014Pygaze] for eye tracking.

## General stimuli and procedure

Before each block, a nine-point eye-tracker calibration was performed. At the start of each selection trial, an automatic single-point recalibration (drift correction) was performed. The display consisted of a green central fixation dot (r = 0.2°) on a gray background (13.0 cd/m^2^). Items were presented in a circular configuration at an eccentricity of 9.2° (%FigParadigm). Items consisted of colored letters against a circular background (r = 3.1°). When only two items were presented, each item was accompanied by a mirror-symmetric placeholder (see %FigParadigm::a; this configuration was chosen because pilot experiments showed it to be the most effective of several tested configurations). The backgrounds alternated between brightness (97.0 cd/m^2^) and darkness (5.1 cd/m^2^) in cycles of 1.25 s (0.8 Hz). Each cycle consisted of a smooth brightness transition of 0.5 s, followed by 0.75 s of constant brightness (%FigParadigm::b).

The participant attended covertly to the target stimulus, while keeping gaze on the central fixation dot. The target was either indicated by a cue (Phase 1-3) or chosen by the participant (Phase 4). The cue was both visual (e.g., the letter 'A' shown on the display) and auditory (e.g., a synthesized French voice saying *Sélectionnez A*). The participant could replay the auditory cue at any moment by pressing the space bar. The trial ended when a selection was made (%FigParadigm::c, see Selection algorithm).

## Selection algorithm

Letters are divided into two groups: bright and dark backgrounds. Each group has a parameter *L* that reflects how likely it is that the attended letter is part of that group. Initially, *L* is 1 for both groups. After each cycle, a proportional pupil-size difference (*PPSD*) is determined (see Pupil-size measurement). For the letter group that has changed from bright to dark, *L* is multiplied by *PPSD* (because we expect the pupil to dilate if the target is part that group). For the letter group that has changed from dark to bright, *L* is divided by *PPSD* (because we expect the pupil to constrict if the target is part that group). Cycling continues until the proportional difference between the *L*s for both groups exceeds a threshold *T* (*L1*/*L2* > *T* or *L1/L2* < 1/*T*), after which the group with the highest *L* is designated as the winner. If groups consist of more than one letter, the losing group is discarded, and the winning group is subdivided into two new bright/ dark groups (See %FigParadigm::d). The selection process then starts anew. This continues until the winning group contains only a single letter, after which the final selection is made. The analysis is performed on-line, while the participant performs the task.

A crucial property of this algorithm is that it continues until there is sufficient evidence for reliable selection. Selection can be made faster but less accurate by reducing the threshold *T*, and slower but more accurate by increasing it.

++The reason that we presented up to eight separate letters, even though the algorithm made only one-of-two selections, was to avoid users from having to re-orient their attention after each selection; that is, once users shifted their attention toward a to-be-selected letter, they simply kept attending to it, while the algorithm gradually pruned the non-attended letters through a series of one-of-two selections.++

## Pupil-size measurement

The proportional pupil-size difference on cycle *i* (*PPSD(i)*) is defined as:

![](resources/formula PPSD.png)

Here, *PS(i)* is the median pupil size during the last 250 ms of cycle *i* (see %FigParadigm::b).

## Training program

The training program consisted of four phases. In Phases 1-3, participants were trained to make progressively more complicated selections. In Phase 4, participants wrote a short self-selected sentence using an extension of the technique trained in Phases 1-3. Training took about 10 hours, spread over multiple days.

### Phases 1-3: Selecting a predefined stimulus

In Phase 1, participants were trained to select one of two simultaneously presented stimuli. Blocks consisted of 16 selections.

Training was successful when participants reached: 100% accuracy after completing at least 6 ++blocks++; or at least 80% accuracy on block 12. Thus, participants completed between 6 and 12 blocks. If training was unsuccessful, the phase was restarted with a more conservative threshold of 1.5 (default threshold = 1.375). If training then failed again, the experiment was aborted and training was considered unsuccessful for that participant. After training was successfully completed, participants completed a single block in gaze-stabilization mode. Our criteria for success were stringent: Commonly, 70% accuracy is taken as a lower limit for a useful BCI/ HCI [e.g., @Astrand2014Selective;@Birbaumer2006Breaking].

Phases 2 and 3 were identical to Phase 1, except that participants selected one out of four (Phase 2) or eight (Phase 3) stimuli.

### Phase 4: Free writing

In Phase 4, participants trained to write text by selecting characters and control symbols ('backspace': a leftward arrow; 'space': a low bar; and 'accept': a square) on a virtual keyboard. The participant initially selected one of eight symbol groups. This group then unfolded, after which the participant selected one symbol. Structurally, selecting a symbol was therefore identical to a one-of-eight selection (Phase 3) followed by a one-of-four selection (Phase 2), or, in the case of 'accept' and 'backspace', a one-of-two selection (Phase 1). This procedure is similar to the Hex-o-Spell P300-based human-computer interface [@Blankertz2006].

First, participants were given a print-out of the virtual keyboard to familiarize themselves with its layout (see %FigFreeWriting). Next, they practiced by writing the French word "ecrire" (without accent). Practice was completed when the word was written successfully, with a maximum of three attempts. Next, participants chose a short sentence (deviation from preregistration: several participants wanted to write a long sentence, and we therefore abandoned our initial maximum of 15 characters). Participants were given two opportunities to write this sentence. Writing was considered successful when the final sentence matched the specified sentence. The use of backspace to correct mistakes during text input was allowed.

### Criteria and statistical analyses

No participants or selections were excluded from the analysis. Two blocks (32 selections) were lost due to technical problems. Two participants chose not to finish the experiment, and were replaced. In total, 257 blocks (4,112 selections) were included in the analysis.

We analyzed accuracy using Generalized Linear Mixed-Effects Models with correctness (binomial) as dependent variable. We analyzed response times using Linear Mixed-Effects Models with response time as dependent variable. We included by-participant random intercepts and slopes (i.e. maximal random effects), unless this model failed to converge, in which case we included only random intercepts. Fixed effects were considered reliable when p < .05; however, we emphasize general patterns over significance of individual results. These analyses were conducted in R [@R+core+team2014], using the packages `lme4` [@Bates2015Lme4] and `lmerTest` [@Kuznetsova2015].

Information-transfer rate (ITR) is a measure of communication efficiency, and depends on both accuracy and speed. ITR was determined using the following formula [@Yuan2013InformationTransfer]:

![](resources/formula ITR.png)

Here, *ITR* is in bits per minute, *N* is the number of response options, *Acc* is proportion correct responses, and *RT* is the response time in seconds.

The response time was the interval between the start of the first selection cycle and the end of the last selection cycle. Mean accuracy, response time, and ITR were first determined per participant, and then averaged to arrive at grand means (i.e. a means-of-means approach).
