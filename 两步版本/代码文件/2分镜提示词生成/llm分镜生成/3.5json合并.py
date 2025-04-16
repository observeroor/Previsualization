import os
import json

def merge_json_files(input_folder, output_file):
    """
    将指定文件夹中的所有 JSON 文件的每个 key 下的具体内容直接合并，并不保留具体内容的名称。
    :param input_folder: 包含 JSON 文件的文件夹路径
    :param output_file: 合并后的输出文件路径
    """
    merged_content = []

    # 遍历文件夹中的所有 JSON 文件
    for filename in os.listdir(input_folder):
        if filename.endswith('.json'):
            file_path = os.path.join(input_folder, filename)
            try:
                # 读取 JSON 文件内容
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    # 遍历每个 key，将其内容直接合并到列表中
                    for key, value in data.items():
                        if isinstance(value, list):
                            merged_content.extend(value)  # 如果内容是列表，直接扩展
                        elif isinstance(value, dict):
                            merged_content.append(value)  # 如果内容是字典，直接添加
                        else:
                            merged_content.append(value)  # 其他类型直接添加
            except Exception as e:
                print(f"处理文件 {filename} 时出错: {e}")

    # 将合并后的内容写入输出文件
    try:
        with open(output_file, 'w', encoding='utf-8') as output:
            json.dump(merged_content, output, ensure_ascii=False, indent=4)
        print(f"合并完成，结果已保存到: {output_file}")
    except Exception as e:
        print(f"保存合并结果时出错: {e}")

if __name__ == "__main__":
    # 输入文件夹路径
    input_folder = r"c:\Git\Previsualization\两步版本\过程文件\json文件夹"
    # 输出文件路径
    output_file = r"c:\Git\Previsualization\两步版本\过程文件\合并结果.json"

    # 调用合并函数
    merge_json_files(input_folder, output_file)