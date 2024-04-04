import os
import shutil
from glob import glob

def get_bug_number(SOURCE_DIR,DEST_DIR): 
    # 判断目标目录是否存在，如果不存在则创建
    if not os.path.exists(DEST_DIR):
        os.makedirs(DEST_DIR, exist_ok=True)

    # 函数用于获取目录中文件及文件夹的数量
    def get_file_and_folder_count(folder_path):
        file_count = len([name for name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, name))])
        folder_count = len([name for name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, name))])
        return file_count + folder_count  # 减去1是因为目录本身也会被计算在内


    # 遍历源目录中的文件夹
    for folder in glob(os.path.join(SOURCE_DIR, "fuzz_*/")):
        total_count = get_file_and_folder_count(folder)

        # 如果 yosys 文件夹内文件数量不等于3，则复制当前文件夹到目标目录
        if total_count != 7:
            folder_name = os.path.basename(folder.rstrip('/'))
            shutil.copytree(folder, os.path.join(DEST_DIR, folder_name), dirs_exist_ok=True)
            # print(f"复制 {folder_name} 到 {DEST_DIR} (因为 yosys 文件夹不满足条件)")

    bug_number = get_file_and_folder_count(DEST_DIR)
    # print(f"目标目录中的文件数量为 {bug_numver}")
    return bug_number