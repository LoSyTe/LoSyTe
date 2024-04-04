import numpy as np
import random
import shutil
from config_update import config_update
from get_PSO_case import case_generate
from ops_folder_generation import create_case_folder, create_bug_folder
from new_get_rewards import get_reward

# 假设的适应度函数
def fitness_function(case_folder,bug_folder,synth_time,new_counter):
    episode = new_counter -1 
    fitness_value = get_reward(case_folder, bug_folder, synth_time, episode)
    
    return fitness_value

class Particle:
    def __init__(self, num_selected_arms):
        self.position = np.array([random.randint(0, len(arm_candidates[i])-1) for i in range(num_selected_arms)])
        self.pbest_position = self.position
        self.pbest_value = float('inf')
        self.velocity = np.array([random.random() for _ in range(num_selected_arms)])

    def update_velocity(self, gbest_position):
        w = 0.5  # 惯性权重
        c1 = 1  # 个体学习因子
        c2 = 2  # 社会学习因子

        for i in range(len(self.position)):
            r1, r2 = random.random(), random.random()
            cognitive_velocity = c1 * r1 * (self.pbest_position[i] - self.position[i])
            social_velocity = c2 * r2 * (gbest_position[i] - self.position[i])
            self.velocity[i] = w * self.velocity[i] + cognitive_velocity + social_velocity

    def update_position(self, arm_candidates):
        for i in range(len(self.position)):
            self.velocity[i] = max(min(self.velocity[i], len(arm_candidates[i]) - 1), -len(arm_candidates[i]) + 1)
            self.position[i] = int(max(0, min(len(arm_candidates[i])-1, self.position[i] + self.velocity[i])))

    def get_parameters(self, arm_index_to_params, arm_candidates):
        return [arm_index_to_params[arm_candidates[i][int(self.position[i])]] for i in range(len(self.position))]

class PSO:
    def __init__(self, fitness_function, num_selected_arms, num_particles):
        self.fitness_function = fitness_function
        self.gbest_value = float('inf')
        self.gbest_position = np.array([random.randint(0, len(arm_candidates[i])-1) for i in range(num_selected_arms)])
        self.particles = [Particle(num_selected_arms) for _ in range(num_particles)]

    def run(self, num_iterations, arm_index_to_params, arm_candidates):
        for iteration in range(num_iterations):
            print(f"Generation {iteration + 1}/{num_iterations}")
            counter = 0
            for particle in self.particles:

                #新增一个计数器，从1开始，每次循环加1，当计数器等于粒子数量时，说明已经遍历完所有粒子               
                counter += 1
                new_counter = counter + iteration * 10
                case_folder = create_case_folder(new_counter)
                bug_folder = create_bug_folder(new_counter)
                

                parameters = particle.get_parameters(arm_index_to_params, arm_candidates)

                orginal_config_file_path = './config.toml'  # 替换为实际路径
                shutil.copy(orginal_config_file_path, case_folder)
                config_file_path = f"{case_folder}/config.toml"
                config_update(config_file_path, parameters)
                synth_time = case_generate(case_folder,config_file_path)

                try:
                    fitness_candidate = self.fitness_function(case_folder,bug_folder,synth_time,new_counter)
                    print("##############################")
                    print("Rewards:", fitness_candidate)
                except Exception as e:
                    print(f"An error occurred while getting fitness_candidate: {e}")
                    fitness_candidate = 0

                # fitness_candidate = self.fitness_function(parameters)

                print(f"  Particle Position: {particle.position}")
                print(f"  Parameters: {parameters}")
                print(f"  Fitness: {fitness_candidate}")

                if particle.pbest_value > fitness_candidate:
                    particle.pbest_value = fitness_candidate
                    particle.pbest_position = particle.position

                if self.gbest_value > fitness_candidate:
                    self.gbest_value = fitness_candidate
                    self.gbest_position = particle.position

            for particle in self.particles:
                particle.update_velocity(self.gbest_position)
                particle.update_position(arm_candidates)

            print(f"Best position in this generation: {self.gbest_position}")
            print(f"Best fitness in this generation: {self.gbest_value}\n")

# 定义每组参数的可选项
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
    
    # [3, 4, 5],
    # [6, 7, 8],
    # [9, 10, 11],
    # [12, 13, 14],
    # [15, 16, 17],
    # [18, 19, 20],
    # [21, 22, 23],
    # [24, 25, 26],
    # [27, 28, 29, 30],
    # [31, 32, 33, 34],
    # [35, 36, 37, 38],
    # [39, 40, 41, 42],
    # [43, 44, 45, 46],
    # [47, 48, 49, 50],
    # ... [其他参数的可选项] ...
]

# 定义参数映射字典
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

def main():
    num_selected_arms = 15  # 总共需要选择的参数组数
    num_particles = 10  # 粒子数量
    num_iterations = 100  # 迭代次数

    pso = PSO(fitness_function, num_selected_arms, num_particles)
    pso.run(num_iterations, arm_index_to_params, arm_candidates)

    print("最优参数索引:", pso.gbest_position)
    optimal_params = [arm_index_to_params[arm_candidates[i][int(pso.gbest_position[i])]] for i in range(num_selected_arms)]
    print("映射后的最优参数:", optimal_params)

if __name__ == '__main__':
    main()
