import random
from config_update import config_update
from get_swarm_case import case_generate
import os
import shutil
from glob import glob

def get_bug_number(SOURCE_DIR,DEST_DIR): 

    if not os.path.exists(DEST_DIR):
        os.makedirs(DEST_DIR, exist_ok=True)


    def get_file_and_folder_count(folder_path):
        file_count = len([name for name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, name))])
        folder_count = len([name for name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, name))])
        return file_count + folder_count  

    for folder in glob(os.path.join(SOURCE_DIR, "fuzz_*/")):
        total_count = get_file_and_folder_count(folder)

        if total_count != 7:
            folder_name = os.path.basename(folder.rstrip('/'))
            shutil.copytree(folder, os.path.join(DEST_DIR, folder_name), dirs_exist_ok=True)

    bug_number = get_file_and_folder_count(DEST_DIR)
    return bug_number

def create_case_folder(episode):
    case_base_path = './baseline_case_and_bug_generation'
    case_folder = f"{case_base_path}/Swarm/case_generation/case_generation_{episode}"

    if not os.path.exists(case_folder):
        os.makedirs(case_folder)
        
    return case_folder

def create_bug_folder(episode):
    bug_base_path = './baseline_case_and_bug_generation'
    bug_folder = f"{bug_base_path}/Swarm/bug_generation/bug_generation_{episode}"

    if not os.path.exists(bug_folder):
        os.makedirs(bug_folder)
        
    return bug_folder


def choose_arms(num_selected_arms):
    arm_candidates = [
        [0, 1, 2, 3 ,4],
        [5, 6, 7, 8, 9],
        [10, 11, 12, 13 ,14],
        [15, 16, 17, 18, 19],
        [20, 21, 22, 23 ,24],
        [25, 26, 27, 28, 29],
        [30, 31, 32, 33 ,34],
        [35, 36, 37, 38, 39],
        [40, 41, 42, 43 ,44],
        [45, 46, 47, 48, 49],
        [50, 51, 52, 53 ,54],
        [55, 56, 57, 58, 59],
        [60, 61, 62, 63 ,64],
        [65, 66, 67, 68, 69],
        [70, 71, 72, 73 ,74],
    ]

    chosen_arms = []
    for i in range(num_selected_arms):
        chosen_arm = random.choice(arm_candidates[i])
        chosen_arms.append(chosen_arm)

    return chosen_arms

def perform_swarm_test(num_tests, num_selected_arms, arm_index_to_params):
    for test_num in range(num_tests):
        case_folder = create_case_folder(test_num)
        bug_folder = create_bug_folder(test_num)

        selected_arms = choose_arms(num_selected_arms)

        selected_params = [arm_index_to_params[arm] for arm in selected_arms]
        print(f"Test {test_num}: Selected Parameters: {selected_params}")

        orginal_config_file_path = './config.toml' 
        shutil.copy(orginal_config_file_path, case_folder)
        config_file_path = f"{case_folder}/config.toml"
        config_update(config_file_path, selected_params)
        try:
            synth_time = case_generate(case_folder,config_file_path)
            bug_number = get_bug_number(case_folder,bug_folder)
            print("##############################")
            print("bug_number:", bug_number)
        except Exception as e:
            print(f"An error occurred : {e}")

arm_index_to_params = {
        0: "expr.binary=3",
        1: "expr.binary=4",
        2: "expr.binary=5",
        3: "expr.binary=6",
        4: "expr.binary=7",
        5: "expr.signed=3",
        6: "expr.signed=4",
        7: "expr.signed=5",
        8: "expr.signed=6",
        9: "expr.signed=7",
        10: "expr.unary=3",
        11: "expr.unary=4",
        12: "expr.unary=5",
        13: "expr.unary=6",
        14: "expr.unary=7",
        15: "expr.unsigned=3",
        16: "expr.unsigned=4",
        17: "expr.unsigned=5",
        18: "expr.unsigned=6",
        19: "expr.unsigned=7",
        20: "expr.variable=3",
        21: "expr.variable=4",
        22: "expr.variable=5",
        23: "expr.variable=6",
        24: "expr.variable=7",
        25: "moditem.assign=3",
        26: "moditem.assign=4",
        27: "moditem.assign=5",
        28: "moditem.assign=6",
        29: "moditem.assign=7",
        30: "moditem.combinational=2",
        31: "moditem.combinational=3",
        32: "moditem.combinational=4",
        33: "moditem.combinational=5",
        34: "moditem.combinational=6",
        35: "moditem.instantiation=2",
        36: "moditem.instantiation=3",
        37: "moditem.instantiation=4",
        38: "moditem.instantiation=5",
        39: "moditem.instantiation=6",
        40: "moditem.sequential=2",
        41: "moditem.sequential=3",
        42: "moditem.sequential=4",
        43: "moditem.sequential=5",
        44: "moditem.sequential=6",
        45: "statement.blocking=2",
        46: "statement.blocking=3",
        47: "statement.blocking=4",
        48: "statement.blocking=5",
        49: "statement.blocking=6",
        50: "statement.conditional=2",
        51: "statement.conditional=3",
        52: "statement.conditional=4",
        53: "statement.conditional=5",
        54: "statement.conditional=6",
        55: "statement.forloop=2",
        56: "statement.forloop=3",
        57: "statement.forloop=4",
        58: "statement.forloop=5",
        59: "statement.forloop=6",
        60: "statement.nonblocking=2",
        61: "statement.nonblocking=3",
        62: "statement.nonblocking=4",
        63: "statement.nonblocking=5",
        64: "statement.nonblocking=6",
        65: "module.depth=1",
        66: "module.depth=2",
        67: "module.depth=3",
        68: "module.depth=4",
        69: "module.depth=5",
        70: "module.max=1",
        71: "module.max=2",
        72: "module.max=3",
        73: "module.max=4",
        74: "module.max=5",
    }

num_tests = 1000  
num_selected_arms = 15  
perform_swarm_test(num_tests, num_selected_arms, arm_index_to_params)
