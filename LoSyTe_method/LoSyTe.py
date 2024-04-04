import numpy as np
# from get_rewards import get_reward
from new_get_rewards import get_reward
from folder_generation import create_case_folder, create_bug_folder
from config_update import config_update
from get_case import case_generate
import shutil
import random

class Bandit:
    def __init__(self, num_arms, arm_values=None):
        self.num_arms = num_arms

        if arm_values is not None:
            self.theta = np.zeros(num_arms)
            for i, arm_name in enumerate(arm_values.keys()):
                self.theta[i] = arm_values[arm_name]
        else:
            self.theta = np.ones(num_arms) / num_arms 

    def get_rewards(self, arms, case_folder, bug_folder,episode):
        self.arm_index_to_params = {
            0: "expr.binary=4",
            1: "expr.binary=5",
            2: "expr.binary=6",
            3: "expr.signed=4",
            4: "expr.signed=5",
            5: "expr.signed=6",
            6: "expr.unary=4",
            7: "expr.unary=5",
            8: "expr.unary=6",
            9: "expr.unsigned=4",
            10: "expr.unsigned=5",
            11: "expr.unsigned=6",
            12: "expr.variable=4",
            13: "expr.variable=5",
            14: "expr.variable=6",
            15: "moditem.assign=4",
            16: "moditem.assign=5",
            17: "moditem.assign=6",
            18: "moditem.combinational=2",
            19: "moditem.combinational=3",
            20: "moditem.combinational=4",
            21: "moditem.instantiation=2",
            22: "moditem.instantiation=3",
            23: "moditem.instantiation=4",
            24: "moditem.sequential=2",
            25: "moditem.sequential=3",
            26: "moditem.sequential=4",
            27: "statement.blocking=4",
            28: "statement.blocking=5",
            29: "statement.blocking=6",
            30: "statement.blocking=7",
            31: "statement.conditional=4",
            32: "statement.conditional=5",
            33: "statement.conditional=6",
            34: "statement.conditional=7",
            35: "statement.forloop=4",
            36: "statement.forloop=5",
            37: "statement.forloop=6",
            38: "statement.forloop=7",
            39: "statement.nonblocking=4",
            40: "statement.nonblocking=5",
            41: "statement.nonblocking=6",
            41: "statement.nonblocking=7",
            42: "module.depth=2",
            43: "module.depth=3",
            44: "module.depth=4",
            45: "module.max=4",
            46: "module.max=5",
            47: "module.max=6",
            48: "sample.size=10",
            49: "sample.size=12",
            50: "sample.size=14",
        }
        new_arms = [self.arm_index_to_params[arm] for arm in arms]
        # # print("############################")
        # # print("New Arms:", new_arms)
        # # print("Arms:", arms)
        # # print("############################")
        orginal_config_file_path = './config.toml'  
        shutil.copy(orginal_config_file_path, case_folder)
        config_file_path = f"{case_folder}/config.toml"

        config_update(config_file_path, new_arms)

        synth_time = case_generate(case_folder,config_file_path)

        try:
            rewards = get_reward(case_folder, bug_folder, synth_time, episode)

        except Exception as e:
            print(f"An error occurred while getting rewards: {e}")
            rewards = 0
        print("Rewards:", rewards)
        avg_reward = rewards/15
        return {arm: avg_reward for arm in arms}

class BanditAgent:
    def __init__(self, num_arms, num_selected_arms=3, epsilon=0.1, learning_rate=0.01):
        self.num_arms = num_arms
        self.num_selected_arms = num_selected_arms
        self.epsilon = epsilon
        self.learning_rate = learning_rate
        self.theta_hat = np.zeros((num_arms))
        self.arm_counts = np.zeros(num_arms)
        self.last_chosen_arms = None


        self.arm_index_to_params = {
            0: "expr.binary=4",
            1: "expr.binary=5",
            2: "expr.binary=6",
            3: "expr.signed=4",
            4: "expr.signed=5",
            5: "expr.signed=6",
            6: "expr.unary=4",
            7: "expr.unary=5",
            8: "expr.unary=6",
            9: "expr.unsigned=4",
            10: "expr.unsigned=5",
            11: "expr.unsigned=6",
            12: "expr.variable=4",
            13: "expr.variable=5",
            14: "expr.variable=6",
            15: "moditem.assign=4",
            16: "moditem.assign=5",
            17: "moditem.assign=6",
            18: "moditem.combinational=2",
            19: "moditem.combinational=3",
            20: "moditem.combinational=4",
            21: "moditem.instantiation=2",
            22: "moditem.instantiation=3",
            23: "moditem.instantiation=4",
            24: "moditem.sequential=2",
            25: "moditem.sequential=3",
            26: "moditem.sequential=4",
            27: "statement.blocking=4",
            28: "statement.blocking=5",
            29: "statement.blocking=6",
            30: "statement.blocking=7",
            31: "statement.conditional=4",
            32: "statement.conditional=5",
            33: "statement.conditional=6",
            34: "statement.conditional=7",
            35: "statement.forloop=4",
            36: "statement.forloop=5",
            37: "statement.forloop=6",
            38: "statement.forloop=7",
            39: "statement.nonblocking=4",
            40: "statement.nonblocking=5",
            41: "statement.nonblocking=6",
            41: "statement.nonblocking=7",
            42: "module.depth=2",
            43: "module.depth=3",
            44: "module.depth=4",
            45: "module.max=4",
            46: "module.max=5",
            47: "module.max=6",
            48: "sample.size=10",
            49: "sample.size=12",
            50: "sample.size=14",
        }
    def choose_arms(self, episode):
        chosen_arms = []
        for i in range(self.num_selected_arms):
            if i == 0:
                arm_candidates = [0, 1, 2]
            elif i == 1:
                arm_candidates = [3, 4, 5]
            elif i == 2:
                arm_candidates = [6, 7, 8]
            elif i == 3:
                arm_candidates = [9, 10, 11]
            elif i == 4:
                arm_candidates = [12, 13, 14]
            elif i == 5:
                arm_candidates = [15, 16, 17]
            elif i == 6:
                arm_candidates = [18, 19, 20]
            elif i == 7:
                arm_candidates = [21, 22, 23]
            elif i == 8:
                arm_candidates = [24, 25, 26]
            elif i == 9:
                arm_candidates = [27, 28, 29, 30]
            elif i == 10:
                arm_candidates = [31, 32, 33, 34]
            elif i == 11:
                arm_candidates = [35, 36, 37, 38]
            elif i == 12:
                arm_candidates = [39, 40, 41, 42]
            elif i == 13:
                arm_candidates = [43, 44, 45]
            elif i == 14:
                arm_candidates = [46, 47, 48]
            elif i == 15:
                arm_candidates = [49, 50, 51]

            print("self.epsilon:", self.epsilon)


            if episode <= 50:
                # Always explore for the first 50 episodes
                chosen_arm = np.random.choice(arm_candidates)
                chosen_arms.append(chosen_arm)

            else:
                # UCB exploration-exploitation strategy
                t = self.arm_counts[arm_candidates]  # Get the number of times each arm in arm_candidates has been selected
                print("t:", t)
                ucb_values = self.theta_hat[arm_candidates] + np.sqrt(2 * np.log(sum(self.arm_counts)) / (t + 1e-6))

                print(f"arm_candidates {arm_candidates}: ucb_values {ucb_values}")

                chosen_arm = arm_candidates[np.argmax(ucb_values)]

                chosen_arms.append(chosen_arm)


        self.last_chosen_arms = chosen_arms

        return chosen_arms

    def update_parameters(self, rewards, episode):
        for chosen_arm in self.last_chosen_arms:
            print("chosen_arm:", chosen_arm)
            if chosen_arm in rewards:
                # print(chosen_arm)
                self.arm_counts[chosen_arm] += 1
                print("self.theta_hat[chosen_arm]:", self.theta_hat[chosen_arm])
                self.theta_hat[chosen_arm] += self.learning_rate * (rewards[chosen_arm])
                print("self.theta_hat[chosen_arm]:", self.theta_hat[chosen_arm])
                true_probs = self.theta_hat[chosen_arm]
                # print("True Probs:", true_probs)

                print(f"Arm {chosen_arm}: chosen {self.arm_counts[chosen_arm]} times, reward {rewards[chosen_arm]}")

        for arm in range(self.num_arms):
            print(f"Arm {arm}: {self.theta_hat[arm]}: {self.arm_counts[arm]}")

    def get_optimal_arms(self, episode):
        # Choose the top arms based on estimated rewards
        estimated_rewards = self.theta_hat
        optimal_arms = np.argpartition(estimated_rewards, -self.num_selected_arms)[-self.num_selected_arms:]

        return optimal_arms

    def map_index_to_params(self, indices):
        return [self.arm_index_to_params[index] for index in indices]

num_arms = 50

num_selected_arms = 15
epsilon = 0.5
learning_rate = 0.01

bandit = Bandit(num_arms)
agent = BanditAgent(num_arms, num_selected_arms, epsilon, learning_rate)

num_episodes = 1000
for episode in range(num_episodes):
    case_folder = create_case_folder(episode)
    bug_folder = create_bug_folder(episode)
    chosen_arms = agent.choose_arms(episode)
    rewards = bandit.get_rewards(chosen_arms, case_folder, bug_folder, episode)
    agent.update_parameters(rewards, episode)

optimal_arms = agent.get_optimal_arms(episode)
optimal_params = agent.map_index_to_params(optimal_arms)
optimal_params = sorted(optimal_params)
print("Learned Optimal Parameters:", optimal_params)





