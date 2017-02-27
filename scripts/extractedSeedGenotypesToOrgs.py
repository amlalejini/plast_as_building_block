
import os
from utilities.utilities import mkdir_p

def main():
    exp_base_dir = "/mnt/home/lalejini/Data/plast_as_building_block"
    seed_analysis_dir = os.path.join(exp_base_dir, "seed_analysis")
    ancestral_seed_bank_dir = os.path.join(exp_base_dir, "ancestral_seed_bank")
    mkdir_p(ancestral_seed_bank_dir)
    reps = [r for r in os.listdir(seed_analysis_dir) if "__rep_" in r]
    for rep in reps:
        fpath = os.path.join(seed_analysis_dir, rep, "final_dom")
        org = [o for o in os.listdir(fpath) if "org-" in o][0]
        org_content = ""
        geno_content = ""
        with open(os.path.join(fpath, org), "r") as fp:
            geno_content = fp.read()
        geno_content = geno_content.split("\n\n")
        print geno_content
        exit()


if __name__ == "__main__":
    main()
