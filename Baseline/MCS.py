import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
import os
from config_update import config_update
from get_A2C_case import case_generate
import shutil
from new_get_rewards import get_reward
import time

class MultiAgentA2C:
    def __init__(self, num_agents, num_actions, state_dim, actor_lr=0.001, critic_lr=0.005, gamma=0.99):
        self.num_agents = num_agents
        self.num_actions = num_actions
        self.gamma = gamma

        # Actor and Critic networks for each agent
        self.actors = [self.build_actor(state_dim, num_actions) for _ in range(num_agents)]
        self.critics = [self.build_critic(state_dim) for _ in range(num_agents)]

        self.actor_optimizer = Adam(learning_rate=actor_lr)
        self.critic_optimizer = Adam(learning_rate=critic_lr)

    def build_actor(self, state_dim, action_dim):
        inputs = Input(shape=(state_dim,))
        x = Dense(1024, activation='relu')(inputs)
        x = Dense(1024, activation='relu')(x)
        x = Dense(1024, activation='relu')(x)
        x = Dense(1024, activation='relu')(x)
        outputs = Dense(action_dim, activation='softmax')(x)
        model = Model(inputs, outputs)
        return model

    def build_critic(self, state_dim):
        inputs = Input(shape=(state_dim,))
        x = Dense(1024, activation='relu')(inputs)
        x = Dense(1024, activation='relu')(x)
        x = Dense(1024, activation='relu')(x)
        x = Dense(1024, activation='relu')(x)
        outputs = Dense(1)(x)
        model = Model(inputs, outputs)
        return model

    def choose_action(self, state):
        actions = []    
        for index, actor in enumerate(self.actors):
            prob = actor.predict(state)[0]
            print(f"Agent {index} action probabilities: {prob}")
            action = np.random.choice(self.num_actions, p=prob)
            actions.append(action)
            print(f"Agent {index} chose action: {action}")
        return actions

    
    def get_trainable_variables(self):
        trainable_variables = []
        for actor, critic in zip(self.actors, self.critics):
            trainable_variables += actor.trainable_variables
            trainable_variables += critic.trainable_variables
        return trainable_variables

    def train(self, state, action, shared_reward, next_state, done):
        for i, (actor, critic) in enumerate(zip(self.actors, self.critics)):
            with tf.GradientTape() as actor_tape, tf.GradientTape() as critic_tape:
                critic_value = critic(state)
                critic_value_next = critic(next_state)
                target = shared_reward + self.gamma * critic_value_next * (1 - int(done))
                delta = target - critic_value

                actor_probs = actor(state)
                action_probs = actor_probs[0, action[i]]
                actor_loss = -tf.math.log(action_probs) * delta
                critic_loss = tf.keras.losses.MSE(critic_value, target)

            actor_grads = actor_tape.gradient(actor_loss, actor.trainable_variables)
            critic_grads = critic_tape.gradient(critic_loss, critic.trainable_variables)

            actor_grads = [tf.clip_by_value(g, -1.0, 1.0) for g in actor_grads if g is not None]
            critic_grads = [tf.clip_by_value(g, -1.0, 1.0) for g in critic_grads if g is not None]

            if actor_grads and critic_grads:
                self.actor_optimizer.apply_gradients(zip(actor_grads, actor.trainable_variables))
                self.critic_optimizer.apply_gradients(zip(critic_grads, critic.trainable_variables))


class ConfigEnvironment:
    def __init__(self):
        self.param_options = {
            "expr.binary": [3, 4, 5, 6, 7],
            "expr.signed": [3, 4, 5, 6, 7],
            "expr.unary": [3, 4, 5, 6, 7],
            "expr.unsigned": [3, 4, 5, 6, 7],
            "expr.variable": [3, 4, 5, 6, 7],
            "moditem.assign": [3, 4, 5, 6, 7],
            "moditem.combinational": [2, 3, 4, 5, 6],
            "moditem.instantiation": [2, 3, 4, 5, 6],
            "moditem.sequential": [2, 3, 4, 5, 6],
            "statement.blocking": [2, 3, 4, 5, 6],
            "statement.conditional": [2, 3, 4, 5, 6],
            "statement.forloop": [2, 3, 4, 5, 6],
            "statement.nonblocking": [2, 3, 4, 5, 6],
            "module.depth": [1, 2, 3, 4, 5],
            "module.max": [1, 2, 3, 4, 5],
            "sample.size": [6, 8, 10, 12, 14],
        }

        self.state = {param: np.random.choice(options) for param, options in self.param_options.items()}

    def step(self, actions):
        print(f"Current state: {self.state}, actions: {actions}")

        for param, action in actions.items():
            self.state[param] = self.param_options[param][action]


        next_state = self.state

        state_values = [f"{key}={value}" for key, value in next_state.items()]
        print(f"state_values: {state_values}")

        orginal_config_file_path = './config.toml'  
        shutil.copy(orginal_config_file_path, case_folder)
        config_file_path = f"{case_folder}/config.toml"
        config_update(config_file_path, state_values)
        synth_time = case_generate(case_folder,config_file_path)

        time.sleep(10) 

        try:
            reward = get_reward(case_folder,bug_folder,synth_time,new_counter)
            print("##############################")
            print("Rewards:", reward)
        except Exception as e:
            print(f"An error occurred while getting fitness_candidate: {e}")
            reward = 0
        print(f"Next state: {next_state}, reward: {reward}")

        return next_state, reward

    def reset(self):
        self.state = {param: np.random.choice(options) for param, options in self.param_options.items()}
        return self.state

    def get_state_vector(self):
        return np.array(list(self.state.values())).reshape(1, -1)

num_parameters = len(ConfigEnvironment().param_options)
num_actions = 5  
state_dim = num_parameters 

actor_lr = 0.001     
critic_lr = 0.005    
gamma = 0.99         

a2c_agents = MultiAgentA2C(num_parameters, num_actions, state_dim, actor_lr, critic_lr, gamma)
env = ConfigEnvironment()
trainable_variables = a2c_agents.get_trainable_variables()
a2c_agents.actor_optimizer.build(trainable_variables)
a2c_agents.critic_optimizer.build(trainable_variables)

def create_case_folder(episode):
    case_base_path = './baseline_case_and_bug_generation'
    case_folder = f"{case_base_path}/A2C/case_generation/case_generation_{episode}"

    if not os.path.exists(case_folder):
        os.makedirs(case_folder)
        
    return case_folder

def create_bug_folder(episode):
    bug_base_path = './baseline_case_and_bug_generation'
    bug_folder = f"{bug_base_path}/A2C/bug_generation/bug_generation_{episode}"

    if not os.path.exists(bug_folder):
        os.makedirs(bug_folder)
        
    return bug_folder

for episode in range(100):
    state = env.reset()
    state_vector = env.get_state_vector()
    total_reward = 0

    for step in range(10):
        
        new_counter = step + episode * 10    
        case_folder = create_case_folder(new_counter)
        bug_folder = create_bug_folder(new_counter)
        print("new_counter: ",new_counter)

        actions = a2c_agents.choose_action(state_vector)
        actions_dict = {param: action for param, action in zip(env.param_options.keys(), actions)}
        next_state, reward = env.step(actions_dict)
        next_state_vector = env.get_state_vector()
        total_reward += reward

        time.sleep(10) 
        done = False  
        a2c_agents.train(state_vector, actions, total_reward, next_state_vector, done)
        state_vector = next_state_vector

    print(f"Episode {episode} - Total Reward: {total_reward}")