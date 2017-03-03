"""
This script processes output of exp_analysis.cfg (Avida analyze mode).

* For seed environments:
    * seed org:
        * Phenotype score, max phenotype score, env count
* For exp environments:
    * final dominant
        * Phenotype score, max phenotype score, env count, equ count
    * final dominant lineage:
        * Phenotype score sequence, phenotype update sequence, max phenotype score, env count, equ count
"""

import os
from utilities.ParseAvidaOutput import ParseDetailFile

trait_map = {"NOT": "Not", "NAND": "Nand", "AND": "And", "ORN": "OrNot", "OR": "Or",
             "ANDN": "AndNot", "NOR": "Nor", "XOR": "Xor", "EQU": "Equals"}

def ExtractEnvDetails(env):
    env = env.replace("ENV___", "")
    return {trait.split("_")[0]:trait.split("_")[-1] for trait in env.split("__")}

def NormalizePhenotypeScore(score, max_score):
    """
    Return score between -100 and 100.
    """
    return float(score) / float(max_score) * 100

def AnalyzeOrg(org_details, env_details, skip_traits = []):
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
    max_phen_score = len(env_details) - len(skip_traits)
    phenotype_score = 0
    perf_equ = 0
    if trait_map["EQU"].lower() in org_details:
        perf_equ = 1 if org_details[trait_map["EQU"].lower()] == "1" else 0
    for trait in env_details:
        if trait in skip_traits: continue
        trait_name = trait_map[trait].lower()
        expression = org_details[trait_name]
        if expression == "1" and env_details[trait] == "1":     # True positive (+1)
            phenotype_score += 1
        elif expression == "0" and env_details[trait] == "-1":  # True negative (+1)
            phenotype_score += 1
        elif expression == "1" and env_details[trait] == "-1":  # False positive (-1)
            phenotype_score -= 1
        elif expression == "0" and env_details[trait] == "1":   # False negative (-1)
            phenotype_score -= 1
        else:
            print "Unexpected expression/environment case!"
            exit(-1)
    return {"max_score": max_phen_score, "score": phenotype_score, "perf_equ": perf_equ}

def main():
    # Some relevant parameters.
    exp_base_dir = "/Users/amlalejini/DataPlayground/plast_as_building_block"
    evorgs_dir = os.path.join(exp_base_dir, "analysis")
    skip_runs = ["Q2T1_46", "Q3T1_46", "Q4_T1_46"]
    # Get all relevant runs.
    runs = [d for d in os.listdir(evorgs_dir) if "__rep_" in d]
    # From runs, resolve what treatments we have.
    treatment_set = {t.split("__")[0] for t in runs}
    # Organize runs by treatment.
    treatments = {t:[r for r in runs if t in r] for t in treatment_set}
    data_content = [["treatment", "question", "rep_id", "seed_env_count", "seed_phenotype_score", "seed_max_phenotype_score",
                    "seed_norm_phenotype_score", "fdom_env_count", "fdom_phenotype_score",
                    "fdom_max_phenotype_score", "fdom_norm_phenotype_score", "fdom_equ"]]
    for treatment in treatments:
        print "Processing treatment: %s" % treatment
        for run in treatments[treatment]:
            print "  Processing run: %s" % run
            if run in skip_runs: continue
            run_dir = os.path.join(evorgs_dir, run)
            seed_dir = os.path.join(run_dir, "seed")
            fdom_dir = os.path.join(run_dir, "final_dominant")
            ####################
            # Seed analysis.
            ####################
            seed_envs = [e for e in os.listdir(seed_dir) if "ENV___" in e] # Extract seed environments.
            seed_phen_score = 0
            seed_phen_mscore = 0
            for env in seed_envs:
                env_dir = os.path.join(seed_dir, env)
                # 1) Extract environment characteristics
                env_dets = ExtractEnvDetails(env)
                # 2) Extract seed organism details.
                seed_dets = ParseDetailFile(os.path.join(env_dir, "seed_details.dat"))[0]
                # 3) Analyze seed organism in environment.
                #   * calc phenotype score
                #   * calc max phenotype score
                analysis = AnalyzeOrg(seed_dets, env_dets)
                seed_phen_mscore += analysis["max_score"]
                seed_phen_score += analysis["score"]
            ####################
            # Final dominant analysis.
            ####################
            fdom_envs = [e for e in os.listdir(fdom_dir) if "ENV___" in e] # Extract fdom environments.
            fdom_phen_score = 0
            fdom_phen_mscore = 0
            fdom_perf_equ_cnt = 0
            for env in fdom_envs:
                env_dir = os.path.join(fdom_dir, env)
                # 1) Extract environment characteristics.
                env_dets = ExtractEnvDetails(env)
                # 2) Extract fdom organism details.
                fdom_dets = ParseDetailFile(os.path.join(env_dir, "fdom_details.dat"))[0]
                # 3) Analyze fdom organism in the environment.
                skip_traits = [] if "Q1" in treatment else ["NAND", "NOT"]
                analysis = AnalyzeOrg(fdom_dets, env_dets, skip_traits)
                fdom_phen_mscore += analysis["max_score"]
                fdom_phen_score += analysis["score"]
                fdom_perf_equ_cnt += analysis["perf_equ"]
            # Aggregate data for this run.
            run_data = {"treatment": treatment,
                        "question": treatment[:2],
                        "rep_id": run,
                        "seed_env_count": len(seed_envs),
                        "seed_phenotype_score": seed_phen_score,
                        "seed_max_phenotype_score": seed_phen_mscore,
                        "seed_norm_phenotype_score": NormalizePhenotypeScore(seed_phen_score, seed_phen_mscore),
                        "fdom_env_count": len(fdom_envs),
                        "fdom_phenotype_score": fdom_phen_score,
                        "fdom_max_phenotype_score": fdom_phen_mscore,
                        "fdom_norm_phenotype_score": NormalizePhenotypeScore(fdom_phen_score, fdom_phen_mscore),
                        "fdom_equ": fdom_perf_equ_cnt
                    }
            # Order and append data to content list
            data_content.append([str(run_data[attr]) for attr in data_content[0]])
            print "    Seed env cnt: " + str(len(seed_envs))
            print "    Seed score: " + str(seed_phen_score)
            print "    Max seed score: " + str(seed_phen_mscore)
            print "    Seed norm score: " + str(NormalizePhenotypeScore(seed_phen_score, seed_phen_mscore))
            print "    Fdom env cnt: " + str(len(fdom_envs))
            print "    Fdom score: " + str(fdom_phen_score)
            print "    Fdom max score: " + str(fdom_phen_mscore)
            print "    Fdom norm score: " + str(NormalizePhenotypeScore(fdom_phen_score, fdom_phen_mscore))
            print "    Fdom pef equ: " + str(fdom_perf_equ_cnt)
    print data_content
    # Write out data content to file.
    with open("grungeback_does_science.data", "w") as fp:
        fp.write("\n".join([",".join(line) for line in data_content]))

if __name__ == "__main__":
    main()
