# Plasticity as an Evolutionary Building Block
This repository contains avida configuration files and analysis scripts for experiments looking at the role plasticity plays in the evolution of complexity.

## TODO:
  * How should I split 6 logic functions into two groups?

## For ECAL 2017: Plasticity as a Building Block for Complexity
### Big question:
How does plasticity affect the evolution of more complex tasks?

### Experiments:
#### Questions
  1. What are the effects of existing regulation of multiple traits on the evolution of more complex regulation of those same traits?
  2. What are the effects of existing regulation of multiple traits on the evolution of different and more complex, unregulated traits?
  3. What are the effects of existing regulation of multiple traits on the evolution of different and more complex, regulated traits?
  4. What are the effects of existing regulation of multiple traits on the evolution of complex coordination, like division of labor?

#### General Design
To answer each of the above questions, digital organisms are evolved in a seed, or ancestral, environment. Organisms evolved under seed/ancestral environment conditions are then transferred to an experimental environment. See environment descriptions for descriptions of seed environments used.

##### General Design Decision Notes
  * Environmental change rate
    - Selecting a single change rate that seems to produce the most examples of plasticity in exploratory studies.
  * Mutational events
    - Allowing for insertion mutations because maybe duplications are useful for the evolution of more complex regulation?


##### Design by question:
  1. What are the effects of existing regulation of multiple traits on the evolution of more complex regulation of those same traits?
    * Ancestral Environments:
      - NAND/NOT (2 env) with sensing
        - NAND/NOT regulation is perfectly correlated when just 2 environments.
      - NAND/NOT (2 env) without sensing
      - NAND/NOT (static) with sensing (lower priority)
      - NAND/NOT (static) without sensing
    * Experimental Environment:
      - NAND/NOT (4 env) with sensing.
    * Data collection:
     - Rate of evolution of optimality with respect to ancestral environment (mark treatments w/optimal final dominant)
     - Update of optimal phenotype evolution in experimental environment
     - Optimal phenotype at end of experimental environment

  2. What are the effects of existing regulation of multiple traits on the evolution of different and more complex, unregulated traits?
    * Ancestral Environments:
      - NAND/NOT (4 env) with sensing
      - NAND/NOT (4 env) without sensing
      - NAND/NOT (static) with sensing (lower priority)
      - NAND/NOT (static) without sensing
    * Experimental Environment:
      - Full logic 9 (static) overlaid on ancestral environmental conditions.
    * Data collection:
      - Rate of evolution of optimality with respect to ancestral environment (mark treatments w/optimal final dominant)
      - Update of optimal phenotype evolution in experimental environment
      - Optimal phenotype at end of experimental environment

  3. What are the effects of existing regulation of multiple traits on the evolution of different and more complex, regulated traits?
    * Ancestral Environments:
      - NAND/NOT (4 env) with sensing
      - NAND/NOT (4 env) without sensing
      - NAND/NOT (static) with sensing (lower priority)
      - NAND/NOT (static) without sensing
    * Experimental Environments:
      - Full logic 9 (logic 9 = logic 9 - ancestral) (4 env) overlaid on ancestral environment.
      - Full logic 9 (random) overlaid on ancestral environment
    * Data collection:
      - Rate of evolution of optimality with respect to ancestral environment (mark treatments w/optimal final dominant)
      - Update of optimal phenotype evolution in experimental environment
      - Optimal phenotype at end of experimental environment

  4. What are the effects of existing regulation of multiple traits on the evolution of complex coordination, like division of labor?
    * Ancestral Environments:
      - NAND/NOT (4 env) with sensing
      - NAND/NOT (4 env) without sensing
      - NAND/NOT (static) with sensing (lower priority)
      - NAND/NOT (static) without sensing
    * Experimental Environments:
      - Division of labor due to task-switching costs.
      - Division of labor due to mutually exclusive tasks. (lower priority)
    * Data collection:
      - Rate of evolution of optimality with respect to ancestral environment (mark treatments w/optimal final dominant)
      - Division of labor measurements of final dominant colony at end of the experimental environment

### Configuration Notes
  * exp_configs -- EVENTS FILES
    * ENV-A: NAND/NOT (4 env) + ANDN/OR/ORN/AND/XOR/NOR/EQU (static)
    * ENV-B: NAND/NOT (static) + ANDN/OR/ORN/AND/XOR/NOR/EQU (static)
    * ENV-C: NAND/NOT (4 env) + correlated ANDN/OR/ORN/AND/XOR/NOR + EQU (static)
    * ENV-D: NAND/NOT (static) + changing ANDN/OR/ORN/AND/XOR/NOR + EQU (static)
    * ENV-E: NAND/NOT (4 env) + randomly changing ANDN/OR/ORN/AND/XOR/NOR/EQU + EQU (static)
    * ENV-F: NAND/NOT (static) + randomly changing ANDN/OR/ORN/AND/XOR/NOR/EQU + EQU (static)
## Environments

### Ancestral/Seed Environments:
  * Base Replicator
    - This is the case where there is no ancestral/seed environment. A base replicator is used to seed the experimental environment.
  * NAND/NOT (2 environment) with sensing
  * NAND/NOT (2 environment) without sensing
  * NAND/NOT (4 environment) with sensing
    * sensing -- sensing instructions are in place that return whether the expression of a trait is rewarded/punished/neither rewarded or punished.
  * NAND/NOT (4 environment) without sensing
    * without sensing -- sensing instructions are unavailable
  * NAND/NOT (static) with sensing
  * NAND/NOT (static) without sensing

### Experimental Environments:
  * NAND/NOT (4 environment) with sensing
  * Full logic 9 (static) overlay
    * Overlay implies that whatever the original ancestral environment is, we overlay the experimental overlay environment on top of it.
  * Full logic 9 (4 environment) overlay
    * NAND/NOT changing as if in NAND/NOT (4 env)
    * 3 traits correlated to NAND
    * 3 traits correlated with NOT
    * EQU always rewarded
  * Full logic 9 (randomly changing) overlay
    * Pre-generated, randomly changing environments (overlaid on top of NAND/NOT)
  * Division of labor (via task-switching costs)
  * Division of labor (via mutually exclusive tasks)
