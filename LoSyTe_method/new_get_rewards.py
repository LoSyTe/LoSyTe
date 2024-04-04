from case_feature import extract_features
from sklearn.metrics.pairwise import cosine_similarity
import os
from get_bugs_number import get_bug_number

def get_distance(feature_old,new_files_path):

    feature_old = feature_old
    feature_new = extract_features(new_files_path)

    cov = cosine_similarity([feature_new], [feature_old])[0, 0]
    distance = (1-cov)*50

    if distance > 1:
        distance = 1

    return distance,feature_new

def get_times(times):

    if times < 600:
        times_award = 0
    elif times >= 600 and times < 700:
        times_award = -0.1
    elif times >= 700 and times < 800:
        times_award = -0.2
    elif times >= 800 and times < 900:
        times_award = -0.3
    elif times >= 900 and times < 1000:
        times_award = -0.4
    elif times >= 1000:
        times_award = -0.5
    return times_award
    
def get_bugs_number(SOURCE_DIR,DEST_DIR):
    bugs_number = get_bug_number(SOURCE_DIR,DEST_DIR)
    bugs_number_award = 0.1 * bugs_number
    return bugs_number_award

def get_reward(case_folder, bug_folder,synth_time, episode):
    global global_feature_old
    new_files_path = case_folder
    SOURCE_DIR = case_folder
    DEST_DIR = bug_folder
    times = synth_time
    original_files_path ="./original_case"
    if episode == 0:
        feature_old = extract_features(original_files_path)
    else:
        feature_old = global_feature_old

    print("**********************************")
    print("feature_old:",feature_old)
    print("**********************************")
    distance_rewards,feature_new = get_distance(feature_old,new_files_path)
    global_feature_old = feature_new

    print("**********************************")
    print("global_feature_old:",global_feature_old)
    print("**********************************")

    times_rewards = get_times(times)
    bugs_number_rewards = get_bugs_number(SOURCE_DIR,DEST_DIR)
    rewards = distance_rewards + times_rewards + bugs_number_rewards
    print("**********************************")
    print("rewards:",rewards)
    print("distance_rewards:",distance_rewards)
    print("times_rewards:",times_rewards)
    print("bugs_number_rewards:",bugs_number_rewards)
    print("**********************************")
    return rewards

            

