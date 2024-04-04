import numpy as np
import random
from collections import deque
import tensorflow as tf

from config_update import config_update
from get_DDQN_case import case_generate
from ops_folder_generation import create_case_folder, create_bug_folder
from new_get_rewards import get_reward
import shutil

class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95  # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()
        self.target_model = self._build_model()
        self.update_target_model()
    
    def _build_model(self):
        model = tf.keras.models.Sequential()
        model.add(tf.keras.layers.Dense(128, input_dim=self.state_size, activation='relu'))
        model.add(tf.keras.layers.Dense(128, activation='relu'))
        model.add(tf.keras.layers.Dense(128, activation='relu'))
        model.add(tf.keras.layers.Dense(128, activation='relu'))
        model.add(tf.keras.layers.Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(learning_rate=self.learning_rate))
        return model


    def update_target_model(self):
        self.target_model.set_weights(self.model.get_weights())

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.target_model.predict(next_state)[0])
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)
 
class SimpleEnv:
    def __init__(self):
        self.binary_param_settings = {0: 3, 1: 4, 2: 5, 3: 6, 4: 7}
        self.signed_param_settings = {5: 3, 6: 4, 7: 5, 8: 6, 9: 7}
        self.unary_param_settings = {10: 3, 11: 4, 12: 5, 13: 6, 14: 7}
        self.unsigned_param_settings = {15: 3, 16: 4, 17: 5, 18: 6, 19: 7}
        self.variable_param_settings = {20: 3, 21: 4, 22: 5, 23: 6, 24: 7}
        self.assign_param_settings = {25: 3, 26: 4, 27: 5, 28: 6, 29: 7}
        self.combinational_param_settings = {30: 2, 31: 3, 32: 4, 33: 5, 34: 6}
        self.instantiation_param_settings = {35: 2, 36: 3, 37: 4, 38: 5, 39: 6}
        self.sequential_param_settings = {40: 2, 41: 3, 42: 4, 43: 5, 44: 6}
        self.blocking_param_settings = {45: 2, 46: 3, 47: 4, 48: 5, 49: 6}
        self.conditional_param_settings = {50: 2, 51: 3, 32: 4, 53: 5, 54: 6}
        self.forloop_param_settings = {55: 2, 56: 3, 57: 4, 58: 5, 59: 6}
        self.nonblocking_param_settings = {60: 2, 61: 3, 62: 4, 63: 5, 64: 6}
        self.depth_param_settings = {65: 1, 66: 2, 67: 3, 68: 4, 69: 5}
        self.max_param_settings = {70: 1, 71: 2, 72: 3, 73: 4, 74: 5}
        # self.size_param_settings = {45: 10, 46: 12, 47: 14}
        self.state = None

    def reset(self):
        self.state = [random.choice(list(self.binary_param_settings.keys())),
                      random.choice(list(self.signed_param_settings.keys())),
                      random.choice(list(self.unary_param_settings.keys())),
                      random.choice(list(self.unsigned_param_settings.keys())),
                      random.choice(list(self.variable_param_settings.keys())),
                      random.choice(list(self.assign_param_settings.keys())),
                      random.choice(list(self.combinational_param_settings.keys())),
                      random.choice(list(self.instantiation_param_settings.keys())),
                      random.choice(list(self.sequential_param_settings.keys())),
                      random.choice(list(self.blocking_param_settings.keys())),
                      random.choice(list(self.conditional_param_settings.keys())),
                      random.choice(list(self.forloop_param_settings.keys())),
                      random.choice(list(self.nonblocking_param_settings.keys())),
                      random.choice(list(self.depth_param_settings.keys())),
                      random.choice(list(self.max_param_settings.keys()))]
        
        return np.array(self.state).reshape(1, 15)

    def step(self, action):

        super_new_state = [
            f"expr.binary={self.binary_param_settings[self.state[0]]}",
            f"expr.signed={self.signed_param_settings[self.state[1]]}",
            f"expr.unary={self.unary_param_settings[self.state[2]]}",
            f"expr.unsigned={self.unsigned_param_settings[self.state[3]]}",
            f"expr.variable={self.variable_param_settings[self.state[4]]}",
            f"moditem.assign={self.assign_param_settings[self.state[5]]}",
            f"moditem.combinational={self.combinational_param_settings[self.state[6]]}",
            f"moditem.instantiation={self.instantiation_param_settings[self.state[7]]}",
            f"moditem.sequential={self.sequential_param_settings[self.state[8]]}",
            f"statement.blocking={self.blocking_param_settings[self.state[9]]}",
            f"statement.conditional={self.conditional_param_settings[self.state[10]]}",
            f"statement.forloop={self.forloop_param_settings[self.state[11]]}",
            f"statement.nonblocking={self.nonblocking_param_settings[self.state[12]]}",
            f"module.depth={self.depth_param_settings[self.state[13]]}",
            f"module.max={self.max_param_settings[self.state[14]]}",

        ]
        orginal_config_file_path = './config.toml'  
        shutil.copy(orginal_config_file_path, case_folder)
        config_file_path = f"{case_folder}/config.toml"
        config_update(config_file_path, super_new_state)
        synth_time = case_generate(case_folder,config_file_path)

        # reward = get_reward(self.state)

        try:
            reward = get_reward(case_folder,bug_folder,synth_time,new_counter)
            print("##############################")
            print("Rewards:", reward)
        except Exception as e:
            print(f"An error occurred while getting fitness_candidate: {e}")
            reward = 0

        print("########################################")
        print(reward)
        print(self.state)
        print(super_new_state)
        print(action)
        print("########################################")
        done = False  # Assuming task is not episodic
        return np.array(self.state).reshape(1, 15), reward, done

if __name__ == '__main__':
    env = SimpleEnv()
    state_size = 15  # Binary and Signed parameters
    action_size = 5**15  # 3 options for expr.binary * 3 options for expr.signed
    agent = DQNAgent(state_size, action_size)
    batch_size = 15

    EPISODES = 100  # Adjust this value as needed
    for e in range(EPISODES):

        state = env.reset()

        for time in range(10):  # Adjust the maximum number of steps as needed
            new_counter = time + e * 10
            case_folder = create_case_folder(new_counter)
            bug_folder = create_bug_folder(new_counter)
            print("new_counter: ",new_counter)

            action = agent.act(state)
            next_state, reward, done = env.step(action)
            reward = float(reward)
            agent.remember(state, action, reward, next_state, done)
            state = next_state
            if done:
                break
            if len(agent.memory) > batch_size:
                agent.replay(batch_size)

    print("Training finished.")
