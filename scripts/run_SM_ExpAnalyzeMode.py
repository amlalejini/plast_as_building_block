"""
Run on post-experiment data.

Test and detail seed genotypes for each run (in all seed environments).
Test and detal final dominants for each run (in all experimental environments).
Test and detail final dominant lineages for each run (in all experimental environments).

"""
import itertools, copy, os, subprocess, sys
from utilities.utilities import mkdir_p

def GenAllPossibleEnvs(traits = []):
    """
    Given list of traits, generate all possible environments (where traits are either punished or
    rewarded).
    """
    envs = []
    states = [-1, 1]
    for trait in traits:
        if len(envs) == 0:
            envs = [{trait: state} for state in states]
            continue
        new_envs = []
        for env in envs:
            for state in states:
                new_envs.append(copy.deepcopy(env))
                new_envs[-1][trait] = state
        envs = new_envs
    return envs

def GenQ3Envs():
    return GenAllPossibleEnvs(["NAND", "NOT", "AND", "ORN", "OR", "ANDN", "XOR", "NOR", "EQU"])

def GenQ2Envs():
    return GenAllPossibleEnvs(["NAND", "NOT", "AND", "ORN"])

# impose an arbitray ordering on traits (for consistancy purposes)
trait_ordering = ["NOT", "NAND", "AND", "ORN", "OR", "ANDN", "NOR", "XOR", "EQU"]

treatment_info = {
    "Q1": {
        "environments": [{"NAND": 1, "NOT": 1, "AND": 1, "ORN": 1, "OR": 1, "ANDN": 1, "NOR": 1, "XOR": 1, "EQU": 1}],
        "traits": ["NOT", "NAND", "AND", "ORN", "OR", "ANDN", "NOR", "XOR", "EQU"],
        "final_update": 200000
    },
    "Q2": {
        "environments": GenQ2Envs(),
        "traits": ["NOT", "NAND", "AND", "ORN"],
        "final_update": 200000
    },
    "Q3": {
        "environments": GenQ3Envs(),
        "traits": ["NOT", "NAND", "AND", "ORN", "OR", "ANDN", "NOR", "XOR", "EQU"],
        "final_update": 400000
    }
}

def EnvToString(env):
    """
    Given a dictionary that describes an environment, serialize it in a standard way.
    """
    return "__".join(["%s_%d" % (trait, env[trait]) for trait in trait_ordering if trait in env])

def GetDetArgs(treatment):
        return " ".join(["id", "ancestor_dist", "parent_dist", "fitness_ratio", "comp_merit_ratio",
                "parent_muts", "num_cpus", "fitness", "update_born", "depth", "viable",
                "length", "copy_length", "exe_length", "gest_time", "sequence",
                " ".join(["task.%d" % i for i in range(0, len(treatment_info[treatment]["traits"]))])])

def GenExpTests(treatment):
    """
    Generate analysis file code for each treatment.
    """
    tests = ""
    # For each environment, run tests.
    envs = treatment_info[treatment]["environments"]
    tests += "###################\n# EXPERIMENTAL ENV TESTS \n###################\n"
    tests += "ECHO \"BEGIN: EXP TESTS\"\n"
    for env in envs:
        env_str = EnvToString(env)
        tests += "\n# ENV: %s\n" % str(env)
        # Setup this environment.
        tests += "\n".join(["SetReactionValue %s %d" % (t, env[t]) for t in env]) + "\n"
        # Run tests on FDOM.
        tests += "SET_BATCH 1\n"
        tests += "RECALC \n"
        tests += "DETAIL analysis/$t__rep_$i/final_dominant/ENV___%s/fdom_details.dat %s\n" % (env_str, GetDetArgs(treatment))
        tests += "TRACE analysis/$t__rep_$i/final_dominant/ENV___%s/trace/\n" % (env_str, )
        tests += "PRINT analysis/$t__rep_$i/final_dominant/ENV___%s/ fdom_print.gen\n" % (env_str, )
        # Run tests on FDOM.
        tests += "SET_BATCH 2\n"
        tests += "RECALC \n"
        det_args = GetDetArgs(treatment)
        tests += "DETAIL analysis/$t__rep_$i/final_dominant/ENV___%s/fdom_lineage_details.dat %s\n" % (env_str, GetDetArgs(treatment))

    tests += "ECHO \"DONE: EXP TESTS\"\n"
    return tests

def main():
    """
    Manage the runnign of Avida's analyze mode given the settings specified.

    # 1) Edit analysis config file, make temporary file.
    # 2) Run avida analysis mode with temporary file.
    # 3) Clean up temporary file.
    """

    # Settings
    #exp_base_dir = "/Users/amlalejini/DataPlayground/slip_muts/iter_2"
    #cfgs_dir = "/Users/amlalejini/devo_ws/plast_as_building_block/avida_configs"
    exp_base_dir = "/mnt/home/lalejini/Data/slip_muts/iter_2"
    cfgs_dir = "/mnt/home/lalejini/exp_ws/plast_as_building_block/avida_configs"
    data_dir = os.path.join(exp_base_dir, "extra_runs_data")
    analysis_cfgs_dir = os.path.join(cfgs_dir, "analysis")
    exp_cfgs_dir = os.path.join(cfgs_dir, "slip_muts_configs")
    exp_analysis_script = "exp_SM_analysis.cfg"

    mgen100_start_rep = 301
    mgen100_end_rep = 400

    mgen0_start_rep = 201
    mgen0_end_rep = 250

    # Build avida commands from run list file.
    avida_args_by_treatment = {}
    with open(os.path.join(exp_cfgs_dir, "run_list_ECAL17"), "r") as fp:
        for line in fp:
            if "./avida" in line:
                mline = line.split(" ./avida ")
                treatment = mline[0].split(" ")[-1].replace("__rep", "")
                args = mline[1].strip()
                args = args.replace("-s $seed", "")
                args = args.replace("$seed", str(0))
                avida_args_by_treatment[treatment] = args
    # Because avida commands for these runs are customized by replicate ID, I have several options:
    #  1) Pull commands directly from command.sh file for each run. This means I'll run avida analyze mode 1 rep at a time.
    #  2) Pull commands from a single replicate for that treatment (rep 1).
    runs = [d for d in os.listdir(data_dir) if "__rep_" in d]
    #print runs
    treatments = {"__".join(t.split("__")[:-1]) for t in runs}
    # Only include particular treatments:
    #treatments = ["Q2T1", "Q3T1", "Q4T1"]
    # print treatments
    treatments = {t:[r for r in runs if t in r] for t in treatments}
    print treatments
    treatments = list(treatments).sort()
    # Q3 slip slip nop mgen 100: 101-155 done
    for treatment in treatments:
        print "Analyzing treatment: %s" % treatment
        # Generate analysis file.
        q = treatment[:2]
        #if q in skip_questions or treatment in finished_treatments: continue
        start_rep = mgen100_start_rep if ("MinGen_100" in treatment) else mgen0_start_rep
        end_rep = mgen100_end_rep if ("MinGen_100" in treatment) else mgen0_end_rep
        final_update = treatment_info[q]["final_update"]
        content = ""
        with open(os.path.join(analysis_cfgs_dir, exp_analysis_script), "r") as fp:
            content = fp.read()
        content = content.replace("<start_replicate>", str(start_rep))
        content = content.replace("<end_replicate>", str(end_rep))
        content = content.replace("<final_update>", str(final_update))
        content = content.replace("<base_experiment_directory>", data_dir)
        content = content.replace("<treatments>", treatment)
        content = content.replace("<exp_tests>", GenExpTests(treatment[:2]))
        # write out temporary analysis file
        temp_acfg = os.path.join(exp_cfgs_dir, "temp_exp_analysis.cfg")
        with open(temp_acfg, "w") as fp:
            fp.write(content)
        # Build run command.
        cmd = "./avida %s -a -set ANALYZE_FILE %s -set EVENT_FILE dummy_events.cfg" % (avida_args_by_treatment[treatment], temp_acfg)
        # Run avida analysis.
        return_code = subprocess.call(cmd, shell = True, cwd = exp_cfgs_dir)
        # Clean up temporary analysis file.
        return_code = subprocess.call("rm temp_exp_analysis.cfg", shell = True, cwd = exp_cfgs_dir)

if __name__ == "__main__":
    main()
