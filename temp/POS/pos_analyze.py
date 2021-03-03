#!/usr/bin/env python
# -*- coding: utf-8 -*-
import spacy
from spacy import displacy

nlp = spacy.load("en_core_web_sm")

doc = nlp(
    "I tested this scenario in 1.4.6 and the call to the non-Istio workload fails with 503 which is diff than 1.7.3.")

displacy.serve(doc, style="dep")

"""
we set the ingress traffic

> (we, set, ingress traffic)

I tested this scenario in 1.4.6 and the call to the non-Istio workload fails with 503 which is diff than 1.7.3. To make the call work, I had to add a destination rule as doc’d in 1.4.6

                test
                VERB
        /          \           \ 
    I            scenario      in
  PRON             NOUN        ADP
                /               \  
             this              1.4.6
             DET                NUM

> (I, test, scenario)
> (scenario, 1.4.6)
> (call, fail)
> (call, non-Istio workload)
> (fail, 503)


area: title, raw text

steps:

1. syntax analysis
2. sentence split
3. split main clause and subordinate clause
4. extract the chucks(noun phrase and verb)
5. filter out the words into the following lists: (subj)
    - strong (informative)
    - weak



"""
