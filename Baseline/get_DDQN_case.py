import os
import time
import subprocess
import shutil

def case_generate(super_case_path, config_path):
    case_path_1 = './baseline_case_and_bug_generation/DDQN_case/case_1'
    case_path_2 = './baseline_case_and_bug_generation/DDQN_case/case_2'
    case_path_3 = './baseline_case_and_bug_generation/DDQN_case/case_3'
    case_path_4 = './baseline_case_and_bug_generation/DDQN_case/case_4'
    case_path_5 = './baseline_case_and_bug_generation/DDQN_case/case_5'
    case_path_6 = './baseline_case_and_bug_generation/DDQN_case/case_6'
    # case_path_7 = './baseline_case_and_bug_generation/DDQN_case/case_7'
    # case_path_8 = './baseline_case_and_bug_generation/DDQN_case/case_8'
    # case_path_9 = './baseline_case_and_bug_generation/DDQN_case/case_9'
    # case_path_10 = './baseline_case_and_bug_generation/DDQN_case/case_10'
    # super_case_path = './new_case/case'
    # config_path = '/home/zou/software/verismith-master/examples/config_5.toml'

    start = time.time()

    process1 = subprocess.Popen(f'verismith fuzz -c {config_path} -n 20 -o {case_path_1} -k --no-equiv --no-reduction', shell=True)
    process2 = subprocess.Popen(f'verismith fuzz -c {config_path} -n 20 -o {case_path_2} -k --no-equiv --no-reduction', shell=True)
    process3 = subprocess.Popen(f'verismith fuzz -c {config_path} -n 20 -o {case_path_3} -k --no-equiv --no-reduction', shell=True)
    process4 = subprocess.Popen(f'verismith fuzz -c {config_path} -n 20 -o {case_path_4} -k --no-equiv --no-reduction', shell=True)
    process5 = subprocess.Popen(f'verismith fuzz -c {config_path} -n 20 -o {case_path_5} -k --no-equiv --no-reduction', shell=True)
    process6 = subprocess.Popen(f'verismith fuzz -c {config_path} -n 20 -o {case_path_6} -k --no-equiv --no-reduction', shell=True)
    # process7 = subprocess.Popen(f'verismith fuzz -c {config_path} -n 20 -o {case_path_7} -k --no-equiv --no-reduction', shell=True)
    # process8 = subprocess.Popen(f'verismith fuzz -c {config_path} -n 20 -o {case_path_8} -k --no-equiv --no-reduction', shell=True)
    # process9 = subprocess.Popen(f'verismith fuzz -c {config_path} -n 20 -o {case_path_9} -k --no-equiv --no-reduction', shell=True)
    # process10 = subprocess.Popen(f'verismith fuzz -c {config_path} -n 20 -o {case_path_10} -k --no-equiv --no-reduction', shell=True)


    # 等待两个进程执行完毕
    process1.wait()
    process2.wait()
    process3.wait()
    process4.wait()
    process5.wait()
    process6.wait()
    # process7.wait()
    # process8.wait()
    # process9.wait()
    # process10.wait()

    process_remove1 = subprocess.Popen(f'rm -rf {case_path_1}/*.html', shell=True)
    process_remove2 = subprocess.Popen(f'rm -rf {case_path_2}/*.html', shell=True)
    process_remove3 = subprocess.Popen(f'rm -rf {case_path_3}/*.html', shell=True)
    process_remove4 = subprocess.Popen(f'rm -rf {case_path_4}/*.html', shell=True)
    process_remove5 = subprocess.Popen(f'rm -rf {case_path_5}/*.html', shell=True)
    process_remove6 = subprocess.Popen(f'rm -rf {case_path_6}/*.html', shell=True)
    # process_remove7 = subprocess.Popen(f'rm -rf {case_path_7}/*.html', shell=True)
    # process_remove8 = subprocess.Popen(f'rm -rf {case_path_8}/*.html', shell=True)
    # process_remove9 = subprocess.Popen(f'rm -rf {case_path_9}/*.html', shell=True)
    # process_remove10 = subprocess.Popen(f'rm -rf {case_path_10}/*.html', shell=True)
    process_remove1.wait()
    process_remove2.wait()
    process_remove3.wait()
    process_remove4.wait()
    process_remove5.wait()
    process_remove6.wait()
    # process_remove7.wait()
    # process_remove8.wait()
    # process_remove9.wait()
    # process_remove10.wait()

    end = time.time()
    synth_time = end - start

    def move_files(src_path, dst_path):
        files = os.listdir(src_path)
        for file in files:
            base, extension = os.path.splitext(file)
            new_file = base + "_duplicate" + extension
            counter = 1
            src = os.path.join(src_path, file)
            dst = os.path.join(dst_path, new_file)
            while os.path.exists(dst):
                new_file = base + f"_duplicate_{counter}" + extension
                counter += 1
                dst = os.path.join(dst_path, new_file)
            shutil.move(src, dst)

    move_files(case_path_1, super_case_path)
    move_files(case_path_2, super_case_path)
    move_files(case_path_3, super_case_path)
    move_files(case_path_4, super_case_path)
    move_files(case_path_5, super_case_path)
    move_files(case_path_6, super_case_path)
    # move_files(case_path_7, super_case_path)
    # move_files(case_path_8, super_case_path)
    # move_files(case_path_9, super_case_path)
    # move_files(case_path_10, super_case_path)

    process_remove_config = subprocess.Popen(f'rm -rf {super_case_path}/*.toml', shell=True)
    process_remove_config.wait()
    print("process_remove_config success")

    return  synth_time
