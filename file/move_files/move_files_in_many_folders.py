# 一个目录下有多个文件夹，每个文件夹都有一个文件，想把每个文件夹中的文件提取出来
# input: 文件夹路径
# output: 父级路径名为"clean_files"文件夹，包含了所有文件
# run: 1. 修改source_directory 2. Build

import os
import shutil

def move_files(source_directory):

    # 设置目标目录（所有文件将被移动到这里）
    target_directory = f"{os.path.dirname(source_directory)}/clean_files"

    # 确保目标目录存在
    os.makedirs(target_directory, exist_ok=True)

    # 遍历源目录及其所有子目录
    for root, _, files in os.walk(source_directory):
        for file in files:
            # 构造完整的文件路径
            file_path = os.path.join(root, file)
            # 目标路径
            target_path = os.path.join(target_directory, file)

            # 如果目标文件已存在，避免覆盖，改名添加后缀
            count = 1
            while os.path.exists(target_path):
                file_name, file_ext = os.path.splitext(file)
                target_path = os.path.join(target_directory, f"{file_name}_{count}{file_ext}")
                count += 1

            # 移动文件
            shutil.copy(file_path, target_path)
            print(f"copy: {file_path} -> {target_path}")

# 设置源目录（包含多个子文件夹）
source_directory = "/Users/lanting/Project/MAPK12/data"  # 替换为你的源目录路径
move_files(source_directory)

print("所有文件已成功移动！")