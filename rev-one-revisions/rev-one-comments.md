Deadline: October 21, 2019.

---
title: Revisions summary for JGR paper
---


# ANCEY:

1. explain dependence of rates on m more carefully. describe how the number of particles relates to the bed elevation

2. write a supplement on the simulation algorithm

3. better justify the use of a single cell instead of an array of multiple scales

4. split the discussion into subsections

---

# Reviewer (1):

1. I have some concerns regarding the main conclusions of this paper, where the authors claim an asymptotically heavy-tailed resting time distribution. 

2. “If residence times have an infinite-mean power law distribution... the virtual velocity will continue to decay as a power law... it implies that all particles will eventually be immobile – an unattractive idea for a non-aggrading bed.” It seems that an asymptotically heavy-tailed resting time distribution contradicts the steady-state (or equilibrium) transport conditions. Instead, I agree with Voepel et al. (2013) that at some timescale this heavy-tailed power-law decay for resting time distribution should transition into a faster thin-tailed decay, as supported by empirical evidences presented in that paper.

3. The authors may check the vertical domain of the simulated bed (e.g. as depicted by the tails of the Gaussian distribution in figure 3b), to see if it increases as the simulation spans across different timescales. as simulation duration increases, possibly more extreme elevation values will be sampled. It is not clear how this issue will affect the conclusion.

---

# Reviewer (2):
The only hesitation that I may have is regarding the lack of adequate comparison of the results with other findings on the topic available in literature but overall I believe that the manuscript should be published in the present form. i.e. Pelosi 2014 and Wong 2007

---

# Reviewer (3):

1. it is still unclear to me how a heavy tailed PDF emerges from this framework, while the title says "Derivation of heavy-tailed resting times".

2. my concern is that while the framework is new, it seems not yielding reasonably novel results.

3. experiments of Wong et al. (2007) and analyses of Pelosi et al. (2014) also suggested relatively heavy tailed distribution of channel bed elevation. The fact that there are inconsistencies between the new model and experiments without proper explanations weakens the Discussion and Conclusion significantly.

4. Particularly, many tangent materials that appears in the Discussion (although making sense) seems irrelevant to the essence of the work.

5.  Singh et al 2009 did not mention bed elevation distributions to be symmetric (as mentioned in line 137-138); in fact in Singh et al 2012, they showed bed elevation fluctuations to be asymmetric. Even Wong et al. 2007 argue adeviation from Gaussian behavior at the tails. Similarly, Aberle and Nikora 2006 argue for bed elevation fluctuations pdf to be asymmetric specially with increasing armoring discharge. I wonder if the proposed model needs to be modified in order to obtain the realistic results (asymmetric bed elevation pdfs) and perhaps that would also provide better bedload activity predictions.

6.  I also noticed that the pdfs of bed elevations do not change shape (remain Gaussian;Figure 3), however recent work argue against it, i.e. the pdfs change shape with scale (e.g. Aberle and Nikora 2006; Singh et al 2009; 2012). I wonder what authors need to change in the model to account for this multiscale behavior.

---

# more minor revisions from reviewer (3):

1. Line 225: How is coupling defined? Is this based on linear correlation between bed elevation and bedload activity?

2. The current abstract is very brief and does not provide any information about what is expected in the paper. I think it can be improved by adding some more highlights of results as I believe JGR provides more space for details than currently used.

3. The title. The heavy-tailed resting times are not “derived” but results of numerical simulations. A different word like “implications” is suggested.

4. Line 17. What is “bedload fluctuations”? transport rates?

5. Line 68: it is?

6. Line 70. What about Voepel et al. (2013)? This work also provides evidence of heavy-tailed resting time distributions at some timescales due to burial, as reflected by the empirical results.

7. Line 114. “though”-> “through”?

8. Line 140. Why “anti-symmetrical”?

9. Line 173. Does this random value mean an equal chance for different types of transitions (2) – (7)?

10. Line 362. “a<1”?

11. Line 369. Why “t^{3.64+-0.45}”?

12. I think it will be useful for the reader to provide more detailed figure captions (e.g. fig 3).

---

# key tasks to improve discussion

1. Study bedload fluctuations marginal to elevations

2. Describe asymmetry in pdf(m) as a function of asymmetry in entrainment and deposition rates

