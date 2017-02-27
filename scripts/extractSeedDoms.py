#!/usr/bin/python2

"""
Manage the running of Avida's analyze mode given the settings specified in the given settings file.

# 1) edit analysis config file, make temporary file.
# 2) run avida analysis mode with temporary file.
# 3) clean up temporary file
# 4) create a .org file from the .gen file.
# 5) put .org file in ancestral seed bank
"""

import os, subprocess, sys
from utilities.utilities import mkdir_p

def main():
    exp_base_dir = "/mnt/home/lalejini/Data/plast_as_building_block"
    seed_data_dir = os.path.join(exp_base_dir, "seed_data")
    configs_dir = "/mnt/home/lalejini/exp_ws/plast_as_building_block/avida_configs"
    analysis_cfgs_dir = os.path.join(configs_dir, "analysis")
    seed_configs_dir = os.path.join(configs_dir, "seed_configs")
    ancestral_seed_bank_dir = os.path.join(exp_base_dir, "ancestral_seed_bank")

    start_rep = 1
    end_rep = 100
    final_update = 200000

    mkdir_p(ancestral_seed_bank_dir)

    # Build avida commands from run list file.
    avida_args_by_treatment = {}
    with open(os.path.join(seed_configs_dir, "run_list"), "r") as fp:
        for line in fp:
            if "./avida" in line:
                mline = line.split(" ./avida ")
                treatment = mline[0].split(" ")[-1].replace("__rep_", "")
                args = mline[1].strip()
                avida_args_by_treatment[treatment] = args.replace("-s $seed", "")
    print avida_args_by_treatment
    print "Extracting seed dominants."

    # Build a temporary analysis file.
    for treatment in avida_args_by_treatment:
        print "Processing treatment: " + str(treatment)
        acfg_fpath = os.path.join(analysis_cfgs_dir, "extract_seed_doms.cfg")
        temp_acfg_content = ""
        with open(acfg_fpath, "r") as fp:
            temp_acfg_content = fp.read()
        temp_acfg_content = temp_acfg_content.replace("<start_replicate>", str(start_rep))
        temp_acfg_content = temp_acfg_content.replace("<end_replicate>", str(end_rep))
        temp_acfg_content = temp_acfg_content.replace("<final_update>", str(final_update))
        temp_acfg_content = temp_acfg_content.replace("<base_experiment_directory>", seed_data_dir)
        temp_acfg_content = temp_acfg_content.replace("<treatments>", treatment)
        # Write out temp analysis file.
        temp_acfg = os.path.join(seed_configs_dir, "temp_extract_seed_doms.cfg")
        with open(temp_acfg, "w") as fp:
            fp.write(temp_acfg_content)
        # Build analysis command
        cmd = "./avida %s -a -set ANALYZE_FILE %s" % (avida_args_by_treatment[treatment], temp_acfg)
        # Run avida analysis.
        return_code = subprocess.call(cmd, shell = True, cwd = seed_configs_dir)
        # Create .org file from generated .gen file.
        #geno_fpath = os.path.join(seed_configs_dir, "archive", treatment )
        # Clean up temp analysis file.
        return_code = subprocess.call("rm temp_extract_seed_doms.cfg", shell = True, cwd = seed_configs_dir)
    print "Done!"

if __name__ == "__main__":
    main()
