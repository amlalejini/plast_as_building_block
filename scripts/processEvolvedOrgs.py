"""
This script processes output of exp_analysis.cfg (Avida analyze mode).

* For seed environments:
    * seed org:
        * Phenotype score, max phenotype score, env count
* For exp environments:
    * final dominant
        * Phenotype score, max phenotype score, env count
    * final dominant lineage:
        * Phenotype score sequence, phenotype update sequence, max phenotype score, env count
"""

import os
from utilities.ParseAvidaOutput import ParseDetailFile

#trait_map = {"NOT": , "NAND": , "AND": , "ORN": , }

def ExtractEnvDetails(env):
    env = env.replace("ENV___", "")
    return {trait.split("_")[0]:trait.split("_")[-1] for trait in env.split("__")}

def AnalyzeOrg(seed_details, env_details):
    """
    Given seed details dictionary and environment details dictionary, calculate max possible phenotype
    score and achieved phenotype score.
    Phenotype score:
        * False positives (expressing punished trait): -1
        * False negatives (not expressing rewarded trait): -1
        * True positives (expressing rewarded trait): +1
        * True negatives (not expressing punished trait): +1
    Max score:
        * Sum of total number of traits in environment
    """
    max_phen_score = len(env_details)
    phenotype_score = 0
    for trait in env_details:


def main():
    # Some relevant parameters.
    exp_base_dir = "/Users/amlalejini/DataPlayground/plast_as_building_block"
    evorgs_dir = os.path.join(exp_base_dir, "analysis")

    # Get all relevant runs.
    runs = [d for d in os.listdir(evorgs_dir) if "__rep_" in d]
    # From runs, resolve what treatments we have.
    treatment_set = {t.split("__")[0] for t in runs}
    # Organize runs by treatment.
    treatments = {t:[r for r in runs if t in r] for t in treatment_set}
    print treatments
    for treatment in treatments:
        print "Processing treatment: %s" % treatment
        for run in treatments[treatment]:
            print "  Processing run: %s" % run
            run_dir = os.path.join(evorgs_dir, run)
            seed_dir = os.path.join(run_dir, "seed")
            fdom_dir = os.path.join(run_dir, "final_dominant")
            # Seed analysis.
            seed_envs = [e for e in os.listdir(seed_dir) if "ENV___" in e] # Extract seed environments.
            for env in seed_envs:
                env_dir = os.path.join(seed_dir, env)
                # 1) Extract environment characteristics
                env_dets = ExtractEnvDetails(env)
                # 2) Extract seed organism details.
                seed_dets = ParseDetailFile(os.path.join(env_dir, "seed_details.dat"))[0]
                # 3) Analyze seed organism in environment.
                #   * calc phenotype score
                #   * calc max phenotype score
                AnalyzeOrg(seed_dets, env_dets)
            # Final dominant analysis.
            fdom_envs = [e for e in os.listdir(fdom_dir) if "ENV___" in e] # Extract fdom environments.


if __name__ == "__main__":
    main()
