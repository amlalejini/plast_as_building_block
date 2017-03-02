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

def GenQ4T1Envs():
    envs = GenAllPossibleEnvs(["NAND", "NOT", "AND", "ORN", "OR", "AND", "XOR", "NOR"])
    for e in range(0, len(envs)):
        envs[e]["EQU"] = 1
    return envs

def GenQ4T2Envs():
    envs = GenAllPossibleEnvs(["NAND", "NOT", "AND", "ORN", "OR", "AND", "XOR", "NOR"])
    for e in range(0, len(envs)):
        envs[e]["EQU"] = 1
    return envs

def GenQ4T3Envs():
    envs = GenAllPossibleEnvs(["AND", "ORN", "OR", "AND", "XOR", "NOR"])
    for e in range(0, len(envs)):
        envs[e]["EQU"] = 1
        envs[e]["NAND"] = 1
        envs[e]["NOT"] = 1
    return envs

# impose an arbitray ordering on traits (for consistancy purposes)
trait_ordering = ["NOT", "NAND", "AND", "ORN", "OR", "ANDN", "NOR", "XOR", "EQU"]

treatment_info = {
    "Q1T1": {
        "ancestral": {
            "environments": [{"NAND": -1, "NOT": 1},
                             {"NAND": 1, "NOT": -1}]
        },
        "experimental": {
            "environments": [{"NAND": 1, "NOT": 1},
                             {"NAND": -1, "NOT": 1},
                             {"NAND": 1, "NOT": -1},
                             {"NAND": -1, "NOT": -1}]
        },
    },
    "Q1T2": {
        "ancestral": {
            "environments": [{"NAND": -1, "NOT": 1},
                             {"NAND": 1, "NOT": -1}]
        },
        "experimental": {
            "environments": [{"NAND": 1, "NOT": 1},
                             {"NAND": -1, "NOT": 1},
                             {"NAND": 1, "NOT": -1},
                             {"NAND": -1, "NOT": -1}]
        },
    },
    "Q1T3": {
        "ancestral": {
            "environments": [{"NAND": 1, "NOT": 1}]
        },
        "experimental": {
            "environments": [{"NAND": 1, "NOT": 1},
                             {"NAND": -1, "NOT": 1},
                             {"NAND": 1, "NOT": -1},
                             {"NAND": -1, "NOT": -1}]
        }
    },

    "Q2T1": {
        "ancestral": {
            "environments": [{"NAND": 1, "NOT": 1},
                             {"NAND": -1, "NOT": 1},
                             {"NAND": 1, "NOT": -1},
                             {"NAND": -1, "NOT": -1}]
        },
        "experimental": {
            "environments": [{"NAND": 1, "NOT": 1, "AND": 1, "ORN": 1, "OR": 1, "ANDN":1, "NOR": 1, "XOR": 1, "EQU": 1},
                              {"NAND": -1, "NOT": 1, "AND": 1, "ORN": 1, "OR": 1, "ANDN":1, "NOR": 1, "XOR": 1, "EQU": 1},
                              {"NAND": 1, "NOT": -1, "AND": 1, "ORN": 1, "OR": 1, "ANDN":1, "NOR": 1, "XOR": 1, "EQU": 1},
                              {"NAND": -1, "NOT": -1, "AND": 1, "ORN": 1, "OR": 1, "ANDN":1, "NOR": 1, "XOR": 1, "EQU": 1}]
        }
    },
    "Q2T2": {
        "ancestral": {
            "environments": [{"NAND": 1, "NOT": 1},
                             {"NAND": -1, "NOT": 1},
                             {"NAND": 1, "NOT": -1},
                             {"NAND": -1, "NOT": -1}]
        },
        "experimental": {
            "environments": [{"NAND": 1, "NOT": 1, "AND": 1, "ORN": 1, "OR": 1, "ANDN":1, "NOR": 1, "XOR": 1, "EQU": 1},
                             {"NAND": -1, "NOT": 1, "AND": 1, "ORN": 1, "OR": 1, "ANDN":1, "NOR": 1, "XOR": 1, "EQU": 1},
                             {"NAND": 1, "NOT": -1, "AND": 1, "ORN": 1, "OR": 1, "ANDN":1, "NOR": 1, "XOR": 1, "EQU": 1},
                             {"NAND": -1, "NOT": -1, "AND": 1, "ORN": 1, "OR": 1, "ANDN":1, "NOR": 1, "XOR": 1, "EQU": 1}]
        }
    },
    "Q2T3": {
        "ancestral": {
            "environments": [{"NAND": 1, "NOT": 1}]
        },
        "experimental": {
            "environments": [{"NAND": 1, "NOT": 1, "AND": 1, "ORN": 1, "OR": 1, "ANDN":1, "NOR": 1, "XOR": 1, "EQU": 1}]
        }
    },

    "Q3T1": {
        "ancestral": {
            "environments": [{"NAND": 1, "NOT": 1},
                             {"NAND": -1, "NOT": 1},
                             {"NAND": 1, "NOT": -1},
                             {"NAND": -1, "NOT": -1}]
        },
        "experimental": {
            "environments": [{"NAND": 1, "NOT": 1, "AND": 1, "ORN": 1, "OR": 1, "ANDN":1, "NOR": 1, "XOR": 1, "EQU": 1},
                              {"NAND": -1, "AND": -1, "ANDN": -1, "XOR": -1, "NOT": 1, "ORN": 1, "OR": 1, "NOR": 1, "EQU": 1},
                              {"NAND": 1, "AND": 1, "ANDN": 1, "XOR": 1, "NOT": -1, "ORN": -1, "OR": -1, "NOR": -1, "EQU": 1},
                              {"NAND": -1, "NOT": -1, "AND": -1, "ORN": -1, "OR": -1, "ANDN":-1, "NOR": -1, "XOR": -1, "EQU": 1}]
        }
    },
    "Q3T2": {
        "ancestral": {
            "environments": [{"NAND": 1, "NOT": 1},
                             {"NAND": -1, "NOT": 1},
                             {"NAND": 1, "NOT": -1},
                             {"NAND": -1, "NOT": -1}]
        },
        "experimental": {
            "environments": [{"NAND": 1, "NOT": 1, "AND": 1, "ORN": 1, "OR": 1, "ANDN":1, "NOR": 1, "XOR": 1, "EQU": 1},
                              {"NAND": -1, "AND": -1, "ANDN": -1, "XOR": -1, "NOT": 1, "ORN": 1, "OR": 1, "NOR": 1, "EQU": 1},
                              {"NAND": 1, "AND": 1, "ANDN": 1, "XOR": 1, "NOT": -1, "ORN": -1, "OR": -1, "NOR": -1, "EQU": 1},
                              {"NAND": -1, "NOT": -1, "AND": -1, "ORN": -1, "OR": -1, "ANDN":-1, "NOR": -1, "XOR": -1, "EQU": 1}]
        }
    },
    "Q3T3": {
        "ancestral": {
            "environments": [{"NAND": 1, "NOT": 1}]
        },
        "experimental": {
            "environments": [{"NAND": 1, "NOT": 1, "AND": 1, "ORN": 1, "OR": 1, "ANDN":1, "NOR": 1, "XOR": 1, "EQU": 1},
                              {"NAND": 1, "AND": -1, "ANDN": -1, "XOR": -1, "NOT": 1, "ORN": 1, "OR": 1, "NOR": 1, "EQU": 1},
                              {"NAND": 1, "AND": 1, "ANDN": 1, "XOR": 1, "NOT": 1, "ORN": -1, "OR": -1, "NOR": -1, "EQU": 1},
                              {"NAND": 1, "NOT": 1, "AND": -1, "ORN": -1, "OR": -1, "ANDN":-1, "NOR": -1, "XOR": -1, "EQU": 1}]
        }
    },

    "Q4T1": {
        "ancestral": {
            "environments": [{"NAND": 1, "NOT": 1}, {"NAND": -1, "NOT": 1}, {"NAND": 1, "NOT": -1}, {"NAND": -1, "NOT": -1}]
        },
        "experimental": {
            "environments": GenQ4T1Envs()
        }
    },
    "Q4T2": {
        "ancestral": {
            "environments": [{"NAND": 1, "NOT": 1}, {"NAND": -1, "NOT": 1}, {"NAND": 1, "NOT": -1}, {"NAND": -1, "NOT": -1}]
        },
        "experimental": {
            "environments": GenQ4T2Envs()
        }
    },
    "Q4T3": {
        "ancestral": {
            "environments": [{"NAND": 1, "NOT": 1}]
        },
        "experimental": {
            "environments": GenQ4T3Envs()
        }
    }
}

def EnvToString(env):
    """
    Given a dictionary that describes an environment, serialize it in a standard way.
    """
    return "__".join(["%s_%d" % (trait, env[trait]) for trait in trait_ordering if trait in env])


def GenSeedTests(treatment):
    """
    Generate analysis file code for each treatment.
    """
    tests = ""
    # For each environment, run tests.
    envs = treatment_info[treatment]["ancestral"]["environments"]
    tests += "ECHO\"BEGIN: SEED TESTS\"\n"
    tests += "###################\n# SEED ENV TESTS \n###################\n"
    tests += "SET_BATCH 0\n"
    for env in envs:
        env_str = EnvToString(env)
        tests += "# ENV: %s\n" % str(env)
        # Setup this environment.
        tests += "\n".join(["SetReactionValue %s %d" % (t, env[t]) for t in env]) + "\n"
        # Run tests.
        tests += "RECALC \n"
        tests += "DETAIL analysis/$t__rep_$i/seed/ENV___%s/seed_details.dat <args>\n" % (env_str, )
        tests += "TRACE analysis/$t__rep_$i/seed/ENV___%s/trace/\n" % (env_str, )
        tests += "PRINT analysis/$t__rep_$i/seed/ENV___%s/ seed_print.gen\n" % (env_str, )
    tests += "ECHO\"DONE: SEED TESTS\"\n"
    print tests
    return tests

def GenFDomTests(treatment):
    pass

def main():
    """
    Manage the runnign of Avida's analyze mode given the settings specified.

    # 1) Edit analysis config file, make temporary file.
    # 2) Run avida analysis mode with temporary file.
    # 3) Clean up temporary file.
    """

    # Settings
    exp_base_dir = "/Users/amlalejini/DataPlayground/plast_as_building_block"
    data_dir = os.path.join(exp_base_dir, "data")
    cfgs_dir = "/Users/amlalejini/devo_ws/plast_as_building_block/avida_configs"
    analysis_cfgs_dir = os.path.join(cfgs_dir, "analysis")
    exp_cfgs_dir = os.path.join(cfgs_dir, "exp_configs")

    start_rep = 1
    end_rep = 100
    final_update = 200000

    # Because avida commands for these runs are customized by replicate ID, pull commands directly from
    #  command.sh file for each run. This means I'll run avida analyze mode 1 rep at a time.
    # For efficiency's sake, though, I'll set this up to only gen 1 temp avida analyze file for each
    #  treatment to be reused per replicate.

    runs = [d for d in os.listdir(data_dir) if "__rep_" in d]
    treatments = list({t.split("__")[0] for t in runs})
    for treatment in treatments:
        print "Analyzing treatment: %s" % treatment
        # Generate analysis file.
        GenSeedTests(treatment)
        GenFDomTests(treatment)
        #GenFDomLineageTests(treatment)




if __name__ == "__main__":
    main()
