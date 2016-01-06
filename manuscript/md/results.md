## Phases 1-3: Selecting a predefined stimulus

In the first part of the experiment, participants learned to select one ++of++ two (Phase 1), four (Phase 2), or eight (Phase 3) letters (see %FigParadigm). Letters were presented within circles that oscillated between brightness and darkness in cycles of 1.25 s. Participants selected a letter by covertly attending to it, while keeping the eyes on the central fixation dot. We measured median pupil size during the last 0.25 s of each cycle, and used the following logic to determine which letter the participant intended to select: If pupil size decreased, the participant likely intended to select a letter that changed from darkness to brightness ('a' in %FigParadigm::b); if pupil size increased, the participant likely intended to select a letter that changed from brightness to darkness ('b' in %FigParadigm::b). The estimate of which letter the participant intended to select was updated after each cycle, until there was sufficient evidence for a reliable selection (%FigParadigm::c); therefore, selection times varied. If there were more than two letters, letters were first divided into two groups, of which one was eliminated. This resulted in a step-wise selection procedure, in which eight letters were reduced to four, which were reduced to two, which were reduced to a single winner (%FigParadigm::d). (For details, see Methods.)

We designed the display to make selection as intuitive as possible. First, the size of the letters indicated how close they were to being selected; that is, a letter increased in size until it was selected. This type of sensory feedback is believed to increase BCI/ HCI performance [e.g., @Astrand2014Selective]. Second, after a letter had been selected, it smoothly moved towards the display center. This animation increased the participants' sensation of *grabbing* letters with their mind's eye.

Training was considered successful if a participant reached at least 80% selection accuracy at the end of the training phase. This is more stringent than the threshold of 70% accuracy that is often taken as a lower limit for a useful BCI/ HCI [e.g., @Astrand2014Selective;@Birbaumer2006Breaking].

%--
figure:
 id: FigParadigm
 source: FigParadigm.svg
 caption: |
  The selection procedure. a) Participants selected one of two (Phase 1), four (Phase 2), or eight (Phase 3) simultaneously presented stimuli. b) During each cycle, the brightness of the stimulus gradually changed in 0.5 s, and then remained constant for 0.75 s. Pupil size was measured during the last 0.25 s.
  c) The target stimulus was indicated by a cue. This example shows a correct selection, because the selected stimulus ('a') matches the cue. The size of the letters indicated how close they were to being selected. When a letter was selected, it smoothly moved toward the center. d) If there were more than two letters, letters were grouped by the brightness of their background. One group was eliminated on each selection, after which the remaining group was subdivided anew. This step-wise selection procedure repeated until a single winning stimulus remained.
--%

### Pupillary responses

++%FigPupilTrace::a shows the average pupil size during a cycle, as a function of whether the attended stimulus changed from bright to dark (blue line) or dark to bright (orange line); this is based on the average of all cycles (*N*=112) for a single participant during Phase 1.++ Each cycle started with a 0.5 s transition period, during which the brightness of the stimuli smoothly changed. During transition, pupil size still reflected the pretransition brightness: The pupil was larger if the attended stimulus was dark (orange line) than if it was bright (blue). Next, there was an adaptation period of 0.5 s. During adaptation, the pupil gradually started to reflect the new brightness of the attended stimulus, as reflected by the crossover of the blue and orange lines. Finally, there was a measurement period of 0.25 s, during which the brightness effect (i.e. the difference between the orange and blue lines) was roughly stable. Median pupil size during this period was used for the analysis; that is, our method exploited the fact that pupil size was larger when a target was dark (blue line) than when it was bright (orange line; see also Methods: Pupil-size measurement).

++In addition to the effects of the brightness of the attended stimulus, there were also pronounced overall changes in pupil size during each cycle. Specifically, the brightness transition (0 - 0.5 s) induced a pupillary constriction around 0.2 s after the transition had finished; this is a pupillary response to visual change, which occurs even if overall luminance remains constant [e.g. @MathôtMelmiCastet2015;@Slooter1980;@Ukai1985]. This constriction lasted only briefly, and was followed by a recovery (i.e. a redilation) that carried over into the start of the next cycle, resulting in an overall dilate-constrict-dilate pattern during each cycle.++

As shown in in %FigPupilTrace::b, all participants showed a qualitatively identical pattern. One participant (indicated in red) showed a weak effect; this was the only participant who did not reach our criteria for successful training (see Results: Selection accuracy and speed).

%--
figure:
 source: FigPupilTrace.svg
 id: FigPupilTrace
 caption: |
  Pupillary responses during one brightness-transition cycle. a) Example data from one participant. Pupil size as a function of whether the target changes from bright to dark (blue line) or from dark to bright (orange line). Shadings indicate standard deviation. b) The pupil size difference (i.e. orange - blue) for all participants. The participant indicated in red did not reach our criteria for successful training. The participant indicated by the arrow corresponds to the example shown in (a). All data is from Phase 1, in which participants selected one out of two stimuli.
--%

### Selection accuracy and speed

%FigFullBarPlot shows the mean selection accuracy and speed for each participant.

%--
figure:
 source: FigFullBarPlot.svg
 id: FigFullBarPlot
 caption: |
  Selection accuracy (top row) and speed (bottom row) for individual participants (gray bars) and across participants (blue bars). Horizontal dashed lines indicate chance level. a) Results for Phase 1. b) Results for Phase 2. c) Results for Phase 3. Error bars indicate 95% confidence intervals, within-subject where applicable [cf. @Cousineau2005].
--%

In Phase 1, mean accuracy was 88.9% (chance = 50%; *N* = 10), with a mean selection time of 14.9 s. Information-transfer rate (ITR) was 2.58 bits/min (%FigITR; see Methods: Criteria and statistical analyses for a definition of ITR). Nine out of ten participants met our criteria for successful training (see Methods: Training program). One participant did not meet our predefined criteria for success, and therefore did not participate in subsequent phases (#10 in %FigFullBarPlot; red line in %FigPupilTrace::b); however, this participant's accuracy was still 70%, which is often taken as the lower limit for useful HCI performance [@Astrand2014Selective;@Birbaumer2006Breaking]. ++All other participants met our criteria for successful training (without increasing the decision threshold *T*; see Methods: Selection algorithm).++ In Phase 2, mean accuracy was 91.0% (chance = 25%; *N* = 9), with a mean selection time of 20.2 s. ITR was 4.55 bits/min. All participants met our criteria for successful training ++(without increasing *T*)++. In Phase 3, mean accuracy was 87.6% (chance = 12.5%; *N* = 9), with a mean selection time of 28.0 s. ITR was 4.86 bits/min. Again, all participants met our criteria for successful training ++(without increasing *T*)++.

%--
figure:
 source: FigITR.svg
 id: FigITR
 caption: |
  The information-transfer rate (ITR) in bits per minute. Bars indicate the mean ITR. Dots indicate individual participants.
--%

### Gaze independence

A crucial question is whether selection is fully independent of eye position. In each but the final block of each phase, the experiment was paused when fixation was lost (gaze deviated more than 2.6° from the display center for more than 10 ms), and continued when fixation was re-established. This controls for large eye movements, but not for small fixational eye movements. Therefore, in the final block of each phase, the entire display was locked to gaze position (from now on: gaze-stabilization mode): When the eyes drifted slightly to the left, all stimuli except the central fixation dot would shift slightly to the left as well. This made sure that selection was not driven by small eye movements in the direction of the attended stimulus [cf. @Mathôt2014Exo;@Mathôt2013Plos].

To test whether selection was independent of gaze, we conducted a Generalized Linear Mixed-Effects Model (GLMER) on accuracy with gaze stabilization (on/ off) as fixed effect (for details of statistical models, see Methods: Criteria and statistical analyses). This revealed no notable effect of gaze stabilization (z = 1.64, p = .102). ++A++ Linear Mixed-Effects Model (LMER) on response times also revealed no effect (t = 1.39, p = .174). If anything, performance was slightly better when gaze-stabilization mode was enabled (see also %FigFullTracePlot in which gaze-stabilization blocks are marked as 'Stb.').

Crucially, this shows that selection did not depend on small eye movements toward the attended stimuli [cf. @EngbertKliegl2003], which participants could have made when gaze-stabilization was disabled. Our method is fully driven by covert attention.

### Learning

%FigFullTracePlot shows how selection accuracy and speed evolved over time. To test whether significant learning occurred, we conducted a GLMER on accuracy with block (continuous) as fixed effect. This was done for each phase separately. There was no notable effect of block (i.e. no learning effect) in any phase: Phase 1 (z = 1.62, p = .104), Phase 2 (z = 1.30, p = .195), Phase 3 (z = 1.48, p = .139). An LMER on response time also did not reveal any notable effect of block: Phase 1 (t = 0.57, p = .565; intercept-only model), Phase 2 (t = 0.37, p = .721), Phase 3 (t = 0.73, p = .488).

Looking at %FigFullTracePlot::a, some learning did appear to occur between blocks 1 and 2 of Phase 1; that is, participants needed a single block of training, before they reached a more-or-less stable level of performance. Importantly, learning effects, if any, were small, and participants were able to use our method right away.

%--
figure:
 source: FigFullTracePlot.svg
 id: FigFullTracePlot
 caption: |
  Selection accuracy (top row) and speed (bottom row) as a function of block number. Blue lines indicate across-participant means during the first six blocks, which were completed by all participants. The size of the gray circles indicates how often a score occurred. Performance during gaze-stabilization blocks is indicated by Stb. Horizontal dotted lines indicate chance level. a) Results for Phase 1. b) Results for Phase 2. c) Results for Phase 3. Error bars indicate 95% within-subject confidence intervals [cf. @Cousineau2005].
--%

## Phase 4: Free writing

In the final part of the experiment, participants used a virtual keyboard to write a self-selected sentence. This keyboard was similar to the displays used in Phases 1-3, but contained a full alphabet and several control symbols (see %FigFreeWriting). (For details, see ++Methods: Training program: Phase 4: Free writing++.)

%--
figure:
 id: FigFreeWriting
 source: FigFreeWriting.svg
 caption: |
  The symbol-selection procedure used for free writing. Initially, there are eight groups of characters and control symbols ('backspace', 'space', and 'accept'). When one group has been selected (here 'abcd'), it unfolds into four individual symbols (here 'a', 'b', 'c', and 'd'), after which a final selection is made (here 'a').
--%

Eight out of nine participants successfully wrote a self-selected sentence (%TblFreeWriting). The remaining participant wrote a sentence that was correct except for one typo.

Participants used a 'backspace' symbol to correct mistakes, and entered an 'accept' symbol to end text input. Therefore, we can distinguish the symbols that were entered (including characters that were later deleted, etc.) from the useful text (the text string that was eventually accepted). In total, participants entered 190 symbols (letters, '?', 'space', 'backspace', and 'accept') for 133 characters of useful text (letters, '?', and 'space'). On average, one symbol took 51.1 s (SD = 9.6; including 'backspace' and 'accept'), and one character of functional text took 75.2 s (SD = 20.5). The functional ITR was 3.91 bits/min. (A bug in an early version of the software occasionally required participants to enter unnecessary 'backspace' symbols. One sentence was affected by this issue, and was excluded from the analysis above.)

%--
table:
 source: TblFreeWriting.csv
 id: TblFreeWriting
 caption: Results of Phase 4, during which participants wrote a self-selected sentence. Names have been replaced by asterisks (*).
--%
