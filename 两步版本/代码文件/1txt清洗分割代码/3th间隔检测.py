import sys
import os
import re
import shutil  # 用于复制文件

def split_txt_files_in_folder(folder_path, output_folder):
    """
    遍历文件夹中的所有 .txt 文件，按连续的 "---" 分割内容。
    分割后的文件保存在指定的输出文件夹中，原始文件不删除。
    未分割的文件也直接复制到输出文件夹中。

    :param folder_path: 原始文件所在的文件夹路径
    :param output_folder: 分割后文件的输出文件夹路径
    """
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        # 检查文件是否为 .txt 文件
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)

            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # 检查是否存在连续的 "---"
            if "---" in content:
                # 按连续的 "---" 分割内容
                sub_contents = re.split(r'-{3,}', content)

                # 保存分割后的子文件
                base_name = os.path.splitext(filename)[0]  # 获取文件名（不含扩展名）
                for i, sub_content in enumerate(sub_contents):
                    # 子文件命名为原文件名加顺序数字
                    new_file_name = f"{base_name}_{i+1}.txt"
                    new_file_path = os.path.join(output_folder, new_file_name)

                    # 写入子文件内容（去掉多余的空白）
                    with open(new_file_path, 'w', encoding='utf-8') as new_file:
                        new_file.write(sub_content.strip())
                    print(f"已保存: {new_file_path}")

            else:
                # 如果未找到分割标记，将原文件复制到输出文件夹
                new_file_path = os.path.join(output_folder, filename)
                shutil.copy(file_path, new_file_path)
                print(f"未找到分割标记，已复制原文件到: {new_file_path}")

if __name__ == "__main__":
    # 从命令行参数获取文件名
    if len(sys.argv) < 2:
        print("缺少文件名参数")
        sys.exit(1)

    name = sys.argv[1]

    # 根据文件名生成输入和输出路径
    base_path = os.path.join(os.getcwd(), "两步版本", "过程文件", name)  # 文件夹路径
    input_path = os.path.join(base_path, "2rd分段")  # 输入文件夹路径
    output_path = os.path.join(base_path, "3th间隔检测")  # 输出文件夹基础路径

    # 确保输出文件夹存在
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        print(f"已创建文件夹：{output_path}")
    else:
        print(f"文件夹已存在：{output_path}")

    # 调用分割函数
    split_txt_files_in_folder(input_path, output_path)