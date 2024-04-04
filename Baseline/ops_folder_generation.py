import os

def create_case_folder(episode):
    case_base_path = './baseline_case_and_bug_generation'
    case_folder = f"{case_base_path}/PSO/case_generation/case_generation_{episode}"

    if not os.path.exists(case_folder):
        os.makedirs(case_folder)
        
    return case_folder

def create_bug_folder(episode):
    bug_base_path = './baseline_case_and_bug_generation'
    bug_folder = f"{bug_base_path}/PSO/bug_generation/bug_generation_{episode}"

    if not os.path.exists(bug_folder):
        os.makedirs(bug_folder)
        
    return bug_folder







