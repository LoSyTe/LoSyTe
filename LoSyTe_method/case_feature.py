import os
import shutil
from get_feature import main
import numpy as np

def extract_features(files_path):
    # Get the current timestamp
    # starttime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # print("start fuzzing...")

    # wrong_directory_path="./wrong/Wrong_case"
    # if os.path.exists(wrong_directory_path):
    #     shutil.rmtree(wrong_directory_path)
    #     os.mkdir(wrong_directory_path)
    # else:
    #     os.mkdir(wrong_directory_path)
    # print(wrong_directory_path)

    # files_path="./case/case_1"
    files = os.listdir(files_path)
    print(files)

    all_features = []
    for filename in files:
        rtl_path = f"{files_path}/{filename}/yosys/rtl.v"
        feature = main(rtl_path)
        # print(feature)
        all_features.append(feature)
        # print(all_features)

    # 计算平均 feature 向量
    if all_features:
        average_feature_vector = np.mean(all_features, axis=0)
        # print(average_feature_vector)
        return average_feature_vector
    else:
        print("get_feature error")
        return None














