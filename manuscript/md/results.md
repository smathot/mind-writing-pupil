## Phases 1-3: Selecting a predefined stimulus

### Criteria and statistical analyses

No participants or selections were excluded from the analysis. Two blocks (32 selections) were lost due to technical problems. Two participants chose not to finish the experiment, and were replaced. In total, 257 blocks (4,112 selections) were included in the analysis.

We analyzed accuracy using Generalized Linear Mixed-Effects Models (GLMER) with correctness (binomial) as dependent variable. We analyzed response times using Linear Mixed-Effects Models with response time as dependent variable. We included by-participant random intercept and slopes (i.e. maximal random effects). Fixed effects were considered reliable when p < .05; however, we emphasize general patterns over significance of individual results. These analyses were conducted in R [@R+core+team2014], using the packages `lme4` [@Bates2015Lme4] and `lmerTest` [@Kuznetsova2015].

Information-transfer rate (ITR) was determined using the following formula [@Yuan2013InformationTransfer]:

    ITR = (log2(N) + P*log2(P) + (1−P)*log2((1 − P)/(N − 1))) * (60/T)

Here, ITR is in bits per minute, `N` is the number of response options, `P` is proportion correct responses, and `T` is the response time in seconds. ITR was determined per participant.

The response time was the interval between the start of the first selection cycle and the end of the last selection cycle.

### Pupillary responses

%FigPupilTrace::a shows how pupil size evolves during one cycle (1.25 s) as a function of whether the attended stimulus changes from bright to dark (blue line) or dark to bright (orange line). This is data for one participant. Each cycle starts with a 500 ms transition period, during which the brightness of the stimuli smoothly changes. During this entire period, pupil size still reflects the pretransition brightness: pupil size is larger if the attended stimulus was dark (orange line), compared to bright (blue). Next, there is an adaptation period of 500 ms. During adaptation, the pupil gradually starts to reflect the new brightness of the attended stimulus, as reflected by the crossover of the blue and orange lines. Finally, there is a measurement period of 250 ms, during which the brightness effect (i.e. the difference between the orange and blue lines) is roughly stable. The median pupil size during this period is used for the analysis (see also Methods: Pupil-size measurement).

As shown in in %FigPupilTrace::b, all participants show a qualitatively identical pattern. One participant (indicated in red) showed a weak effect; this was the only participant who did not reach our criteria for successful training (see Selection accuracy and speed).

%--
figure:
 source: FigPupilTrace.svg
 id: FigPupilTrace
 caption: |
  a) Example data from one participant. Pupil size as a function of whether the target changes from bright dark to bright (blue line) or from dark to bright (orange line). Shadings indicate standard deviation. b) The pupil size difference (i.e. orange - blue) for all participants. The participant indicated in red did not reach our criteria for successful training. The participant indicated by the arrow corresponds to the example shown in (a). All data is from Phase 1, in which participants selected one out of two stimuli.
--%

### Selection accuracy and speed

The main results are shown in %FigFullBarPlot, which shows the mean selection accuracy and speed for each participant. This figure shows data for the first six blocks, which were completed by all participants.

%--
figure:
 source: FigFullBarPlot.svg
 id: FigFullBarPlot
 caption: |
  Selection accuracy (top row) and speed (bottom row) for individual participants (gray bars) and across participants (blue bars). Horizontal dashed lines indicate chance level. a) Results for Phase 1. b) Results for Phase 2. c) Results for Phase 3.
--%

In Phase 1, the mean accuracy was 90.8% (chance = 50%; N = 10), with a mean selection time of 14.7 s. ITR was 2.28 bits/min (%FigITR). Nine out of ten participants met our criteria for successful training (see Methods: Training program). One participant did not meet our criteria, and therefore did not participate in subsequent phases (#10 in %FigFullBarPlot; red line in %FigPupilTrace::b). In Phase 2, the mean accuracy was 90.2% (chance = 25%; N = 9), with a mean selection time of 19.7 s. The ITR was 4.20 bits/min. All participants met our criteria for successful training. In Phase 3, the mean accuracy was 86.3% (chance = 12.5%; N = 9), with a mean selection time of 28.1 s. The ITR was 4.36 bits/min. Again, all participants met our criteria for successful training.

%--
figure:
 source: FigITR.svg
 id: FigITR
 caption: |
  The information-transfer rate (ITR) expressed in bits per minute. Bars indicate the mean ITR. Dots indicate individual participants.
--%

### Learning

%FigFullTracePlot shows how selection accuracy evolves over time. To test whether significant learning occurred, we conducted a GLMER on accuracy with block (continuous) as fixed effect. This was done for each phase separately. There was no notable effect of block (i.e. no learning effect) in any phase: Phase 1 (z = 1.62, p = .104), Phase 2 (z = 1.30, p = .195), Phase 3 (z = 1.48, p = .139). An LMER on response time also did not reveal any notable effect of block: Phase 1 (t = 1.02, p-value non-identifiable, because model does not converge), Phase 2 (t = 0.37, p = .721), Phase 3 (t = 0.73, p = 0.488).

Looking at %FigFullTracePlot::a, some learning did appear to occur between blocks 1 and 2 of Phase 1; that is, participants needed a single block of training, before they reached a more-or-less stable level of performance.

The fact that there was little if any learning within one phase suggests that the ITR increase across phases (%FigITR) reflects a 'startup cost': At the start of each selection, it takes some time to locate, and shift attention towards, the target stimulus. This startup cost is proportionally less when there are more stimuli and selection takes longer.

%--
figure:
 source: FigFullTracePlot.svg
 id: FigFullTracePlot
 caption: |
  Selection accuracy as a function of block number. The bl81ue lines indicate mean accuracy during the first six blocks, which were completed by all participants. The size of the gray circles indicates how often a score occurred. Accuracy during gaze-stabilization blocks is indicated by Stb. Horizontal dotted lines indicate chance level. a) Results for Phase 1. b) Results for Phase 2. c) Results for Phase 3.
--%

### Gaze independence

A crucial question is whether selection is fully independent of eye position. To test this, we conducted a GLMER on accuracy with gaze stabilization (on/ off) as fixed effect. This revealed no notable effect of gaze stabilization (z = 1.64, p = .102). An LMER on response times also revealed no effect (t = 1.39, p = .174). If anything, performance was slightly better when gaze-stabilization mode was enabled (see also %FigFullTracePlot in which gaze-stabilization blocks are marked as 'Stb.'). This shows that performance did not depend on small eye movements towards the attended stimuli, which participants could have made when gaze-stabilization was disabled.

## Phase 4: Free writing

Eight out of nine participants successfully wrote a self-selected sentence (%TblFreeWriting). The remaining participant made a sentence that was correct except for one typo.

In total, participants entered 190 symbols (letters, '?', 'space', 'backspace', and 'accept') for 133 characters of useful text (letters, '?', and 'space'). On average, one symbol took 51.1 s (SD = 9.6; including 'backspace' and 'accept'), and one character of functional text took 75.2 s (SD = 20.5). The functional ITR was 3.91 bits/min. (A bug in an early version of the software required participants to occasionally enter unnecessary 'backspace' symbols. One sentence was affected by this issue, and was excluded from the above analysis.)

%--
table:
 source: TblFreeWriting.csv
 id: TblFreeWriting
 caption: Results of Phase 4, during which participants wrote a self-selected sentence. Names have been replaced by asterisks (*).
--%
