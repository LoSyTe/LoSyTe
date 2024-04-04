import os

def create_case_folder(episode):
    case_base_path = './case_generation'
    case_folder = f"{case_base_path}/case_generation_{episode}"

    # 检查文件夹是否存在，如果不存在则创建
    if not os.path.exists(case_folder):
        os.makedirs(case_folder)
        
    return case_folder

def create_bug_folder(episode):
    bug_base_path = './bug_generation'
    bug_folder = f"{bug_base_path}/bug_generation_{episode}"

    # 检查文件夹是否存在，如果不存在则创建
    if not os.path.exists(bug_folder):
        os.makedirs(bug_folder)
        
    return bug_folder







