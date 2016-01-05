Prior to the training program discussed above, we conducted five pilot experiments to optimize the design of our human-computer interface. In all pilot experiments, two authors (SM and LvdL) served as participants. In all pilot experiments, we varied one parameter, and then selected the parameter value that resulted in best performance for further development. We tested only one-of-two selections. These pilot experiments were purely exploratory, no statistical testing was performed, and no interpretations are provided. We report these pilot experiments for completeness, but their main goal was to aid in the design of the system.

Across all pilot experiments, only 5 of 2064 selections were incorrect (99.8% accuracy). Therefore, accuracy was not analyzed for the Pilot Experiments.

%--
figure:
 id: FigPilotResults
 source: FigPilotResults.svg
 caption: The results from the pilot experiments. Error bars indicate 95% confidence intervals (based on all trials, across both participants).
--%

## Pilot Experiment 1: Stimulus configuration

We tested the following geometric configurations (80 selections per configuration):

- Horiz.: Two letters on the horizontal axis, left and right of fixation.
- Up+: Two letters in the upper visual field with mirror-symmetric placeholders in the lower visual field (cf. %FigParadigm::a).
- Down+: Two letters in the lower visual field with mirror-symmetric placeholders in the upper visual field (i.e. the vertical mirror image of Up+).
- Up-: Two letters in the upper visual field (i.e. like Up+ but without symmetric placeholders).
- Down-: Two letters in the lower visual field (i.e. like Down+ but without symmetric placeholders).

Configuration was varied within blocks. Based on response time (%FigPilotResults::a), we continued with the Up+ configuration.

## Pilot Experiment 2: Stimulus eccentricity

We tested the following stimulus eccentricities (128 selections per eccentricity): 3.86°, 7.15°, 10.47°, and 13.76°. Eccentricity was varied within blocks. Based on response time (%FigPilotResults::b), we continued with an eccentricity of 13.76°.

## Pilot Experiment 3: Stimulus size

We tested the following stimulus sizes (128 selections per size): 0.78°, 1.55°, 2.33°, and 3.11°. Size was varied within blocks. Based on response time (%FigPilotResults::c), we continued with a stimulus size of 3.11°.

## Pilot Experiment 4: More stimulus eccentricities

We felt that the optimal eccentricity might differ for the new stimulus size selected during Pilot Experiment 3 (3.11°). In addition, with the previously selected eccentricity (13.76°), a full circle of stimuli did not fit on the screen. Therefore, we tested two new eccentricities (128 selections per eccentricity): 8.82° and 10.49°. Eccentricity was varied within blocks.

There was little overall effect of eccentricity on selection speed (%FigPilotResults::d), and the optimal eccentricity was different for the two participants (not shown). Therefore, we selected an intermediate eccentricity of 9.2° for further development.

## Pilot Experiment 5: Display-background luminance

We tested the following display-background luminances (128 selections per size): 3.6 cd/m² (dark), 22.9 cd/m² (medium), and 61.5 cd/m² (bright). Background luminance was varied between blocks of 16 selections. Block order was randomized.

Clearly, dark display backgrounds are more effective than bright display backgrounds (%FigPilotResults::e). However, the darkest display background that we tested (3.6 cd/m²) seemed to merge with the dark phase of the stimulus' backgrounds; that is, the stimulus' backgrounds seemed to disappear when they were dark. Therefore, we used a slightly less dark display background for the training program (13.0 cd/m²).
