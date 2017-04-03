"""
This script processes lineage data output from exp_analysis.cfg (Avida analyze mode).

* For exp environments:
    * Final dominant lineage orgs
        * Phenotype score, max phenotype score, normalized phenotype score.

Output data files:
    * Score/update (for each trial, 200k score data points):
        * replicate,
"""

import os, gc
from utilities.ParseAvidaOutput import ParseDetailFile
from utilities.utilities import mkdir_p

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

def AnalyzeOrgSimple(org_details, env_details, skip_traits = []):
    """
    Given seed details dictionary and environment details dictionary, calculate max possible phenotype
    score and achieved phenotype score.
    Phenotype score:
        * False positives (expressing punished trait): -1
        * True positives (expressing rewarded trait): +1
    Max score:
        * Sum of total number of traits in environment
    """
    max_phen_score = len(env_details) - len(skip_traits)
    phenotype_score = 0
    for trait in env_details:
        if trait in skip_traits: continue
        trait_name = trait_map[trait].lower()
        expression = org_details[trait_name]
        if expression == "1" and env_details[trait] == "1":     # True positive (+1)
            phenotype_score += 1
        elif expression == "1" and env_details[trait] == "-1":  # False positive (-1)
            phenotype_score -= 1
    return {"max_score": max_phen_score, "score": phenotype_score}


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
    return {"max_score": max_phen_score, "score": phenotype_score}

def GetEnvIndAttr(attr_key, org_by_env):
    attr = set([org_by_env[env][attr_key] for env in org_by_env])
    assert len(attr) == 1
    return list(attr)[0]

def main():
    # Some relevant parameters.
    #exp_base_dir = "/Users/amlalejini/DataPlayground/slip_muts/iter_2"
    exp_base_dir = "/mnt/home/lalejini/Data/slip_muts/iter_2"
    evorgs_dir = os.path.join(exp_base_dir, "analysis")
    lin_ts_fname = "SM_q3_lineage_score_ts.csv"
    dest = "proc_lins"
    final_update = 200000
    # Score time series data
    score_ts_content = ",".join(["update", "treatment", "question", "rep", "score"]) + "\n"
    mkdir_p(dest)
    with open(os.path.join(dest, "head__" + lin_ts_fname), "w") as fp:
        fp.write(score_ts_content)
    score_ts_content = ""
    # Get all relevant runs.
    runs = [d for d in os.listdir(evorgs_dir) if "__rep_" in d]
    # From runs, resolve what treatments we have.
    treatment_set = {"__".join(t.split("__")[:-1]) for t in runs}
    # Organize runs by treatment.
    treatments = {t:[r for r in runs if t in r] for t in treatment_set}
    skip_qs = ["Q1", "Q2"]
    for treatment in treatments:
        q = treatment[:2]
        if q in skip_qs: continue
        print "Processing treatment: %s" % treatment
        if q == "Q1" or q == "Q2":
            final_update = 200000
        elif q == "Q3":
            final_update = 400000
        else:
            print "Unknown question!"
            exit(-1)
        for run in treatments[treatment]:
            print "  Processing run: %s" % run
            run_dir = os.path.join(evorgs_dir, run)
            fdom_dir = os.path.join(run_dir, "final_dominant")

            ####################
            # Final dominant lineage analysis.
            ####################
            envs = [e for e in os.listdir(fdom_dir) if "ENV___" in e] # Extract fdom environments.
            lin_dets_by_env = {}
            lin_len = set() # We'll do some checking to make sure all lineages are same length in all envs.
            for env in envs:
                env_dir = os.path.join(fdom_dir, env)
                # 1) Extract environment characteristics.
                env_dets = ExtractEnvDetails(env)
                # 2) Extract fdom lineage details.
                lin_dets = ParseDetailFile(os.path.join(env_dir, "fdom_lineage_details.dat"))
                # 3) Store by environment
                lin_dets_by_env[env] = lin_dets
                # 4) Some book keeping
                lin_len.add(len(lin_dets))
            assert len(lin_len) == 1
            lin_len = list(lin_len)[0]
            lin_dets = [{env:lin_dets_by_env[env][i] for env in envs} for i in range(0, lin_len)]

            full_score_seq = [None for _ in range(0, lin_len)]
            full_start_updates = [None for _ in range(0, lin_len)]
            full_duration_updates = [None for _ in range(0, lin_len)]
            max_score = set()
            for i in range(0, lin_len):
                org_by_env = lin_dets[i]

                # Get environment-dependent info for this organism
                # Score organism.
                org_phen_score = 0
                org_phen_score_max = 0
                for env in org_by_env:
                    # Get environment details.
                    env_dets = ExtractEnvDetails(env)
                    # Analyze organism in this environment.
                    analysis = None
                    if q == "Q1":
                        analysis = AnalyzeOrgSimple(org_by_env[env], env_dets)
                    else:
                        analysis = AnalyzeOrg(org_by_env[env], env_dets)

                    org_phen_score += analysis["score"]
                    org_phen_score_max += analysis["max_score"]

                # Get environment-independent info for this organism.
                # * Get start update for this organism.
                start_update = int(GetEnvIndAttr("update born", org_by_env))
                if start_update == -1: start_update = 0

                # * Duration in updates (next start - this start) or (final update - this start)
                next_start_update = int(GetEnvIndAttr("update born", lin_dets[i + 1])) if i + 1 < lin_len else final_update + 1
                duration_update = next_start_update - start_update

                # Record relevant values.
                full_score_seq[i] = org_phen_score
                full_start_updates[i] = start_update
                full_duration_updates[i] = duration_update
                max_score.add(org_phen_score_max)


            sample_range = final_update
            sample_rate = 100
            cur_seq = 0
            cur_range = (full_start_updates[cur_seq], full_start_updates[cur_seq] + full_duration_updates[cur_seq])
            for cur_update in range(0, sample_range + 1, sample_rate):
                # Is current update in cur_seq? If not, find current seq for this sample.
                while (cur_update < cur_range[0]) or (cur_update > cur_range[1]):
                    cur_seq += 1
                    cur_range = (full_start_updates[cur_seq], full_start_updates[cur_seq] + full_duration_updates[cur_seq])
                # We're at the correct location, appent it to score ts content.
                score_ts_content += ",".join([str(cur_update), treatment, treatment[:2], run, str(full_score_seq[cur_seq])]) + "\n"

            # # Expand scores (1 per upate)
            # score_time_series = [-1 for u in range(0, final_update + 1)]
            # for k in range(0, len(full_score_seq)):
            #     start = full_start_updates[k]
            #     if start > sample_range: break
            #     dur = full_duration_updates[k]
            #     score = full_score_seq[k]
            #     for j in range(start, start + dur):
            #         score_time_series[j] = score
            # assert(len(max_score) == 1)
            # max_score = list(max_score)[0]
            # Clean up some memory
            full_score_seq = None
            full_start_updates = None
            full_duration_updates = None
            gc.collect()
            # # Sample rate:
            # samp_rate = 50
            # #sampled_score_ts = {s:score_time_series[s] for s in range(0, final_update + 1, samp_rate) if s < len(score_time_series)}
            # for t in range(0, sample_range, samp_rate):
            #     score_ts_content += ",".join([str(t), treatment, treatment[:2], run, str(score_time_series[t])]) + "\n"
            # score_time_series = None

            # Output content so far.
            with open(os.path.join(dest, run + "__" + lin_ts_fname), "a") as fp:
                fp.write(score_ts_content)
            score_ts_content = ""

if __name__ == "__main__":
    main()
