'''
This script generates Avida events files for ECAL 2017 (plasticity as a building block for complexity experiments).
1 event file for each replicate of each treatment:
    * Events files must be configured to specify the correct ancestral seed organism.
    * Events files for Q4 must be configured for a randomly changing environment.

event bank of the form:
events_bank/
    events___<Q#T#>__rep_$seed#.cfg
'''

import os, random
from utilities.utilities import mkdir_p

# List of experimental environment traetments:
exps = ["Q1T1","Q1T2","Q1T3",
        "Q2T1","Q2T2","Q2T3",
        "Q3T1","Q3T2","Q3T3",
        "Q4T1","Q4T2","Q4T3"]

# Maps treatment -- events base file
exps_mappings = {
                "Q1T1": {
                    "events_base": "events-BASE___ntasks_2__envs_4__cr_50__tasks_NAND_NOT.cfg",
                    "ancestral_treatment": "ntasks_2__envs_2__cr_50__tasks_NAND_NOT__sensing_NAND_NOT"
                },
                "Q1T2": {
                    "events_base": "events-BASE___ntasks_2__envs_4__cr_50__tasks_NAND_NOT.cfg",
                    "ancestral_treatment": "ntasks_2__envs_2__cr_50__tasks_NAND_NOT__sensing_NONE"
                },
                "Q1T3": {
                    "events_base": "events-BASE___ntasks_2__envs_4__cr_50__tasks_NAND_NOT.cfg",
                    "ancestral_treatment": "ntasks_2__envs_1__cr_0__tasks_NAND_NOT__sensing_NONE"
                },
                "Q2T1": {
                    "events_base": "events-BASE___ENV-A.cfg",
                    "ancestral_treatment": "ntasks_2__envs_4__cr_50__tasks_NAND_NOT__sensing_NAND_NOT"
                },
                "Q2T2": {
                    "events_base": "events-BASE___ENV-A.cfg",
                    "ancestral_treatment": "ntasks_2__envs_4__cr_50__tasks_NAND_NOT__sensing_NONE"
                },
                "Q2T3": {
                    "events_base": "events-BASE___ENV-B.cfg",
                    "ancestral_treatment": "ntasks_2__envs_1__cr_0__tasks_NAND_NOT__sensing_NONE"
                },
                "Q3T1": {
                    "events_base": "events-BASE___ENV-C.cfg",
                    "ancestral_treatment": "ntasks_2__envs_4__cr_50__tasks_NAND_NOT__sensing_NAND_NOT"
                },
                "Q3T2": {
                    "events_base": "events-BASE___ENV-C.cfg",
                    "ancestral_treatment": "ntasks_2__envs_4__cr_50__tasks_NAND_NOT__sensing_NONE"
                },
                "Q3T3": {
                    "events_base": "events-BASE___ENV-D.cfg",
                    "ancestral_treatment": "ntasks_2__envs_1__cr_0__tasks_NAND_NOT__sensing_NONE"
                },
                "Q4T1": {
                    "events_base": "events-BASE___ENV-E.cfg",
                    "ancestral_treatment": "ntasks_2__envs_4__cr_50__tasks_NAND_NOT__sensing_NAND_NOT"
                },
                "Q4T2": {
                    "events_base": "events-BASE___ENV-E.cfg",
                    "ancestral_treatment": "ntasks_2__envs_4__cr_50__tasks_NAND_NOT__sensing_NONE"
                },
                "Q4T3": {
                    "events_base": "events-BASE___ENV-F.cfg",
                    "ancestral_treatment": "ntasks_2__envs_1__cr_0__tasks_NAND_NOT__sensing_NONE"
                }
}

def GenerateRandomlyChangingEnv(start = 50, stop = 200000, change_rate = 50):
    traits = ["AND", "ORN", "OR", "ANDN", "NOR", "XOR"]
    vals = [-1, 1]
    env = ""
    # Initialize:
    for trait in traits:
        #u 0 SetReactionValue NAND 1
        ival = random.choice(vals)
        env += "u 0 SetReactionValue %s %d \n" % (trait, ival)
    # Change env
    for u in range(start, stop + 1, change_rate):
        # What traits change?
        for trait in traits:
            ival = random.choice(vals)
            env += "u %d SetReactionValue %s %d \n" % (u, trait, ival)
    return env



    return "RANDOM ENV"

def main():
    # Some parameters:
 #   seed_dir = "/mnt/home/lalejini/Data/plast_as_building_block/seed_data"
    events_bank_dir = "/mnt/home/lalejini/Data/plast_as_building_block/event_bank"
    seed_analysis_dir = "/mnt/home/lalejini/Data/plast_as_building_block/seed_analysis"
    configs_dir = "/mnt/home/lalejini/exp_ws/plast_as_building_block/avida_configs/exp_configs"
    mkdir_p(events_bank_dir)

    # For each experimental environment 'treatment':
    #  * if (Q[1,2,3]): just worry about injecting the right organism.
    #  * if (Q[4]): need to inject correct organism and generate environment.
    all_seed_reps = [r for r in os.listdir(seed_analysis_dir) if "__rep_" in r]
    for exp in exps:
        # Get all relevant seeds
        exp_seeds = [r for r in all_seed_reps if exps_mappings[exp]["ancestral_treatment"] in r]
        print "EXP: " + str(exp)
        for seed_rep in exp_seeds:
            print "\tseed_rep: " + str(seed_rep)
            seed_rep_id = seed_rep.split("_")[-1]
            seed_rep_name = "__".join(seed_rep.split("__")[:-1])
            print "\t  NAME: " + str(seed_rep_name)
            print "\t  ID: " + str(seed_rep_id)
            # Make an events file that transfers this seed_rep's organism to an experimental environment.
            events_base_fname = exps_mappings[exp]["events_base"]
            print "\t  Events base: " + str(events_base_fname)
            content = ""
            with open(os.path.join(configs_dir, events_base_fname), "r") as fp:
                for line in fp:
                    if "<ancestral_organism>" in line:
                        org_fname = [o for o in os.listdir(os.path.join(seed_analysis_dir, seed_rep, "final_dom")) if ".gen" in o][0]
                        ancestral_org = os.path.join(seed_analysis_dir, seed_rep, "final_dom", org_fname)
                        line = line.replace("<ancestral_organism>", ancestral_org)
                    elif "<random_changes>" in line and "Q4" in exp:
                        changing_env = GenerateRandomlyChangingEnv()
                        line = line.replace("<random_changes>", changing_env)
                    content += line
            events_fname = "events___%s__rep_%s.cfg" % (exp, seed_rep_id)
            print "\t  Events fname = " + str(events_fname)
            with open(os.path.join(events_bank_dir, events_fname), "w") as fp:
                fp.write(content)
    print "Done!"

if __name__ == "__main__":
    main()
