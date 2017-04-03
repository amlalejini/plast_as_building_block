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

# List of experimental environment treatments:
exps = ["Q2", "Q3"]

# Maps treatment -- events base file
exps_mappings = {
                "Q2": {
                    "events_base": "events-BASE___RAND_CHANGING.cfg",
                    "total_updates": 200000,
                    "traits": ["NOT", "NAND", "AND", "ORN"]
                },
                "Q3": {
                    "events_base": "events-BASE___RAND_CHANGING.cfg",
                    "total_updates": 400000,
                    "traits": ["NOT", "NAND", "AND", "ORN", "OR", "ANDN", "NOR", "XOR", "EQU"]
                }
}

def GenerateRandomlyChangingEnv(start = 50, stop = 200000, change_rate = 50, traits = []):
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

def main():
    # Some parameters:

    exp_base_dir = "/Users/amlalejini/DataPlayground/slip_muts/iter_2"
    #exp_base_dir = "/mnt/home/lalejini/Data/slip_muts/iter_2"
    events_bank_dir = os.path.join(exp_base_dir, "event_bank")
    #configs_dir = "/mnt/home/lalejini/exp_ws/plast_as_building_block/avida_configs/slip_muts_configs"
    configs_dir = "/Users/amlalejini/devo_ws/plast_as_building_block/avida_configs/slip_muts_configs"
    mkdir_p(events_bank_dir)

    # For each experimental environment 'treatment':
    rep_start = 301
    rep_end = 400
    for exp in exps:
        print "Exp: " + str(exp)
        # Make an events file that transfers this seed_rep's organism to an experimental environment.
        for rep_id in range(rep_start, rep_end + 1):
            events_base_fname = exps_mappings[exp]["events_base"]
            print "\t  REP ID: " + str(rep_id)
            print "\t  Events base: " + str(events_base_fname)
            content = ""
            traits = exps_mappings[exp]["traits"]
            fupdate = exps_mappings[exp]["total_updates"]
            with open(os.path.join(configs_dir, events_base_fname), "r") as fp:
                content = fp.read()
                content = content.replace("<random_changes>", GenerateRandomlyChangingEnv(start = 50, stop = fupdate,
                                                    traits = traits, change_rate = 50))
                content = content.replace("<total_updates>", str(fupdate))

            events_fname = "events___%s__rep_%d.cfg" % (exp, rep_id)
            print "\t  Events fname = " + str(events_fname)
            with open(os.path.join(events_bank_dir, events_fname), "w") as fp:
                fp.write(content)
    print "Done!"

if __name__ == "__main__":
    main()
