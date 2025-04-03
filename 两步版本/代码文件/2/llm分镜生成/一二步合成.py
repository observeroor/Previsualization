import os

def read_file(file_path):
    """读取文件内容并返回每一行的列表"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()

def write_file(file_path, content):
    """将内容写入文件"""
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(content)

def split_lines_into_chunks(lines, chunk_size):
    """将行列表按指定大小分割为多个块"""
    return [lines[i:i + chunk_size] for i in range(0, len(lines), chunk_size)]

def merge_files(folder1, folder2, output_folder):
    """
    合并两个文件夹中名字相同的txt文件内容。
    以folder2中的文件为母本，将folder1中的内容分割后插入到母本文件的指定位置。
    :param folder1: 第一个文件夹路径（如 "6th提示词\中景"）
    :param folder2: 第二个文件夹路径（如 "5th分镜"）
    :param output_folder: 输出文件夹路径
    """
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历第二个文件夹中的所有txt文件
    for filename in os.listdir(folder2):
        if filename.endswith('.txt'):
            file1_path = os.path.join(folder1, filename)
            file2_path = os.path.join(folder2, filename)

            # 如果第一个文件夹中不存在对应的文件，则跳过
            if not os.path.exists(file1_path):
                print(f"文件 {filename} 在 {folder1} 中不存在，跳过。")
                continue

            # 读取两个文件的内容
            file1_lines = read_file(file1_path)
            file2_lines = read_file(file2_path)

            # 将第一个文件的内容分割为每7行一组
            chunks = split_lines_into_chunks(file1_lines, 7)

            # 合并内容
            merged_lines = []
            chunk_index = 0
            for i, line in enumerate(file2_lines):
                merged_lines.append(line)
                # 在第7n+2行后插入一块内容
                if (i - 1) % 7 == 0 and chunk_index < len(chunks):
                    merged_lines.extend(chunks[chunk_index])
                    merged_lines.append("\n")  # 添加一个空行分隔
                    chunk_index += 1

            # 保存合并后的内容到输出文件夹
            output_file_path = os.path.join(output_folder, filename)
            write_file(output_file_path, merged_lines)
            print(f"已合并文件: {filename}")

if __name__ == "__main__":
    # 文件夹路径
    folder1 = r"c:\Git\Previsualization\两步版本\过程文件\nygs\6th提示词\中景"
    folder2 = r"c:\Git\Previsualization\两步版本\过程文件\nygs\5th分镜"
    output_folder = r"c:\Git\Previsualization\两步版本\过程文件\nygs\6th提示词\原始合并中景"

    # 调用合并函数
    merge_files(folder1, folder2, output_folder)