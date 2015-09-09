## Phases 1-3: Selecting a predefined stimulus

### Criteria and statistical analyses

No participants or selections were excluded from the analysis. Two blocks (32 selections) were lost due to technical problems. Two participants chose not to finish the experiment, and were replaced. In total, 257 blocks (4,112 selections) were included in the analysis.

We analyzed accuracy using Generalized Linear Mixed-Effects Models (GLMER) with correctness (binomial) as dependent variable. We analyzed response times using Linear Mixed-Effects Models with response time as dependent variable. We included by-participant random intercepts and slopes (i.e. maximal random effects), unless this model failed to converge, in which case we included only random intercepts. Fixed effects were considered reliable when p < .05; however, we emphasize general patterns over significance of individual results. These analyses were conducted in R [@R+core+team2014], using the packages `lme4` [@Bates2015Lme4] and `lmerTest` [@Kuznetsova2015].

Information-transfer rate (ITR) is a measure of communication efficiency, and depends on both accuracy and speed. ITR was determined using the following formula [@Yuan2013InformationTransfer]:

![](resources/formula ITR.png)

Here, *ITR* is in bits per minute, *N* is the number of response options, *Acc* is proportion correct responses, and *RT* is the response time in seconds.

The response time was the interval between the start of the first selection cycle and the end of the last selection cycle. Mean accuracy, response time, and ITR were first determined per participant, and then averaged to arrive at grand means (i.e. a means-of-means approach).

### Pupillary responses

%FigPupilTrace::a shows how pupil size evolved during one cycle (1.25 s) as a function of whether the attended stimulus changed from bright to dark (blue line) or dark to bright (orange line). This is data from one participant. Each cycle started with a 500 ms transition period, during which the brightness of the stimuli smoothly changed. During transition, pupil size still reflected the pretransition brightness: the pupil was larger if the attended stimulus was dark (orange line) than if it was bright (blue). Next, there was an adaptation period of 500 ms. During adaptation, the pupil gradually started to reflect the new brightness of the attended stimulus, as reflected by the crossover of the blue and orange lines. Finally, there was a measurement period of 250 ms, during which the brightness effect (i.e. the difference between the orange and blue lines) was roughly stable. Median pupil size during this period was used for the analysis; that is, our method exploited the fact that pupil size was larger when a target was dark (blue line) than when it was bright (orange line; see also Methods: Pupil-size measurement).

As shown in in %FigPupilTrace::b, all participants showed a qualitatively identical pattern. One participant (indicated in red) showed a weak effect; this was the only participant who did not reach our criteria for successful training (see Selection accuracy and speed).

%--
figure:
 source: FigPupilTrace.svg
 id: FigPupilTrace
 caption: |
  a) Example data from one participant. Pupil size as a function of whether the target changes from bright to dark (blue line) or from dark to bright (orange line). Shadings indicate standard deviation. b) The pupil size difference (i.e. orange - blue) for all participants. The participant indicated in red did not reach our criteria for successful training. The participant indicated by the arrow corresponds to the example shown in (a). All data is from Phase 1, in which participants selected one out of two stimuli.
--%

### Selection accuracy and speed

The main results are shown in %FigFullBarPlot, which shows the mean selection accuracy and speed for each participant.

%--
figure:
 source: FigFullBarPlot.svg
 id: FigFullBarPlot
 caption: |
  Selection accuracy (top row) and speed (bottom row) for individual participants (gray bars) and across participants (blue bars). Horizontal dashed lines indicate chance level. a) Results for Phase 1. b) Results for Phase 2. c) Results for Phase 3. Error bars indicate 95% confidence intervals [within-subject where applicable, cf. @Cousineau2005].
--%

In Phase 1, the mean accuracy was 88.9% (chance = 50%; *N* = 10), with a mean selection time of 14.9 s. ITR was 2.58 bits/min (%FigITR). Nine out of ten participants met our criteria for successful training (see Methods: Training program). One participant did not meet our criteria for success, and therefore did not participate in subsequent phases (#10 in %FigFullBarPlot; red line in %FigPupilTrace::b); however, this participant's accuracy was still 70%, which is often taken as the lower limit for useful HCI performance [@Astrand2014Selective;@Birbaumer2006Breaking]. In Phase 2, the mean accuracy was 91.0% (chance = 25%; *N* = 9), with a mean selection time of 20.2 s. The ITR was 4.55 bits/min. All participants met our criteria for successful training. In Phase 3, the mean accuracy was 87.6% (chance = 12.5%; *N* = 9), with a mean selection time of 28.0 s. The ITR was 4.86 bits/min. Again, all participants met our criteria for successful training.

%--
figure:
 source: FigITR.svg
 id: FigITR
 caption: |
  The information-transfer rate (ITR) in bits per minute. Bars indicate the mean ITR. Dots indicate individual participants.
--%

### Learning

%FigFullTracePlot shows how selection accuracy and speed evolve over time. To test whether significant learning occurred, we conducted a GLMER on accuracy with block (continuous) as fixed effect. This was done for each phase separately. There was no notable effect of block (i.e. no learning effect) in any phase: Phase 1 (z = 1.62, p = .104), Phase 2 (z = 1.30, p = .195), Phase 3 (z = 1.48, p = .139). An LMER on response time also did not reveal any notable effect of block: Phase 1 (t = 0.57, p = .565; intercept-only model), Phase 2 (t = 0.37, p = .721), Phase 3 (t = 0.73, p = .488).

Looking at %FigFullTracePlot::a, some learning did appear to occur between blocks 1 and 2 of Phase 1; that is, participants needed a single block of training, before they reached a more-or-less stable level of performance. Importantly, learning effects, if any, were small, and participants were able to use our method right away.

%--
figure:
 source: FigFullTracePlot.svg
 id: FigFullTracePlot
 caption: |
  Selection accuracy (top row) and speed (bottom row) as a function of block number. Blue lines indicate across-participant means during the first six blocks, which were completed by all participants. The size of the gray circles indicates how often a score occurred. Performance during gaze-stabilization blocks is indicated by Stb. Horizontal dotted lines indicate chance level. a) Results for Phase 1. b) Results for Phase 2. c) Results for Phase 3. Error bars indicate 95% within-subject confidence intervals [cf. @Cousineau2005].
--%

### Gaze independence

A crucial question is whether selection is fully independent of eye position. To test this, we conducted a GLMER on accuracy with gaze stabilization (on/ off) as fixed effect. This revealed no notable effect of gaze stabilization (z = 1.64, p = .102). An LMER on response times also revealed no effect (t = 1.39, p = .174). If anything, performance was slightly better when gaze-stabilization mode was enabled (see also %FigFullTracePlot in which gaze-stabilization blocks are marked as 'Stb.').

Crucially, this shows that performance did not depend on small eye movements toward the attended stimuli [cf. @EngbertKliegl2003], which participants could have made when gaze-stabilization was disabled. Our method is fully driven by covert attention.

## Phase 4: Free writing

Eight out of nine participants successfully wrote a self-selected sentence (%TblFreeWriting). The remaining participant made a sentence that was correct except for one typo.

Participants could use a 'backspace' symbol to correct mistakes, and needed to enter an 'accept' symbol to end text input. Therefore, we can distinguish the symbols that were entered (including characters that were later deleted, etc.) from the useful text (the text string that was eventually accepted). In total, participants entered 190 symbols (letters, '?', 'space', 'backspace', and 'accept') for 133 characters of useful text (letters, '?', and 'space'). On average, one symbol took 51.1 s (SD = 9.6; including 'backspace' and 'accept'), and one character of functional text took 75.2 s (SD = 20.5). The functional ITR was 3.91 bits/min. (A bug in an early version of the software occasionally required participants to enter unnecessary 'backspace' symbols. One sentence was affected by this issue, and was excluded from the analysis above.)

%--
table:
 source: TblFreeWriting.csv
 id: TblFreeWriting
 caption: Results of Phase 4, during which participants wrote a self-selected sentence. Names have been replaced by asterisks (*).
--%
