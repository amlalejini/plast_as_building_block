# Plasticity as an Evolutionary Building Block
This repository contains avida configuration files and analysis scripts for experiments looking at the role plasticity plays in the evolution of complexity.

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

##### Design by question:
  1. What are the effects of existing regulation of multiple traits on the evolution of more complex regulation of those same traits?

  2. What are the effects of existing regulation of multiple traits on the evolution of different and more complex, unregulated traits?
  3. What are the effects of existing regulation of multiple traits on the evolution of different and more complex, regulated traits?
  4. What are the effects of existing regulation of multiple traits on the evolution of complex coordination, like division of labor?


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
