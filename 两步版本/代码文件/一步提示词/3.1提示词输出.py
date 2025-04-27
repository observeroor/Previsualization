import os
import json

def restructure_json(input_file, output_file):
    """
    重构 JSON 文件中一级 key 下的 value 内容。
    选取二级 key 为 "焦点内容"、"性行为姿势" 和 "女人1头部脸部" 的值，生成新的 JSON 文件。
    
    :param input_file: 输入 JSON 文件路径
    :param output_file: 输出 JSON 文件路径
    """
    try:
        # 读取输入 JSON 文件
        with open(input_file, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # 初始化结果字典
        result = {}

        # 遍历 JSON 数据中的每个一级 key
        for key, value in data.items():
            # 检查 value 是否是字典
            if isinstance(value, dict):
                # 提取需要的字段
                focus_content = value.get("焦点内容", "")
                sexual_position = value.get("性行为姿势", "")
                woman_face_details = value.get("女人1头部脸部", "")

                # 构造新的内容
                new_content = f"({focus_content}:1.1),({sexual_position}：1.4),{woman_face_details}"
                result[key] = new_content

        output_folder = os.path.dirname(output_file)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # 将结果写入输出 JSON 文件
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(result, file, ensure_ascii=False, indent=4)

        print(f"重构完成，结果已保存到: {output_file}")

    except Exception as e:
        print(f"处理文件时出错: {e}")

if __name__ == "__main__":
    # 输入 JSON 文件路径
    input_file = r"c:\Git\Previsualization\两步版本\过程文件\nygs\5.1提示词\3.0合并\chapter_7_output.json"
    # 输出 JSON 文件路径
    output_file = r"c:\Git\Previsualization\两步版本\过程文件\nygs\5.1提示词\3.1合并\chapter_7_restructured.json"

    # 调用重构函数
    restructure_json(input_file, output_file)


"""
编写一个python脚本，用于重构 JSON 文件中一级key下的value内容。重构的一级key的value内容并选取二级key为 "焦点内容"、"性行为姿势" 和 "女人1头部脸部" 的值，按照指定格式生成新的 JSON 文件。
输出结果:
{
"07-01": "([焦点内容]:1.2),([性行为姿势]:1.4),女人1头部脸部"
    },
"""