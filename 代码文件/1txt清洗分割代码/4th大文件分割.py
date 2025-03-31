import sys
import os
import re
import shutil  # 用于复制文件

def split_large_txt_files(folder_path, output_folder, max_lines=300, split_lines=200, overlap=40):
    """
    遍历文件夹内所有txt文件，对超过指定行数的文件进行分割。
    未分割的文件也直接复制到输出文件夹中。

    :param folder_path: 原始文件夹路径
    :param output_folder: 分割后文件的输出文件夹路径
    :param max_lines: 超过该行数的文件将被分割
    :param split_lines: 每个子文件保留的行数
    :param overlap: 子文件之间的重叠行数
    """
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):  # 只处理 .txt 文件
            file_path = os.path.join(folder_path, filename)

            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            # 如果文件行数超过 max_lines，则进行分割
            if len(lines) > max_lines:
                print(f"正在分割文件: {filename}")
                base_name, ext = os.path.splitext(filename)  # 获取文件名和扩展名
                start = 0
                part = 1

                # 按行数分割文件
                while start < len(lines):
                    end = start + split_lines
                    sub_lines = lines[start:end]

                    # 构造子文件名
                    sub_filename = f"{base_name}_{part}{ext}"
                    sub_file_path = os.path.join(output_folder, sub_filename)

                    # 写入子文件
                    with open(sub_file_path, 'w', encoding='utf-8') as sub_file:
                        sub_file.writelines(sub_lines)

                    print(f"已生成子文件: {sub_filename}")
                    part += 1
                    start += split_lines - overlap  # 移动起始行，考虑重叠部分

            else:
                # 如果文件未超过 max_lines，将原文件复制到输出文件夹
                new_file_path = os.path.join(output_folder, filename)
                shutil.copy(file_path, new_file_path)
                print(f"文件未超过 {max_lines} 行，已复制原文件到: {new_file_path}")

# 使用示例

if __name__ == "__main__":
    # 从命令行参数获取文件名
    if len(sys.argv) < 2:
        print("缺少文件名参数")
        sys.exit(1)

    name = sys.argv[1]

    # 根据文件名生成输入和输出路径
    base_path = os.path.join(os.getcwd(), "两步版本", "过程文件", name)  # 文件夹路径
    input_path = os.path.join(base_path, "3th间隔检测")  # 输入文件夹路径
    output_path = os.path.join(base_path, "4th大文件分割")  # 输出文件夹基础路径

    # 确保输出文件夹存在
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        print(f"已创建文件夹：{output_path}")
    else:
        print(f"文件夹已存在：{output_path}")

    # 调用分割函数
    split_large_txt_files(input_path, output_path)