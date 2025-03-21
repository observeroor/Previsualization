import sys
import os
import re

def clean_txt_file(input_file, output_file):
    """
    对txt文件进行清洗：
    1. 删除没有字母、数字、中文字符的行。
    2. 只保留中文、英文、数字、常见标点符号、换行符和空格，删除其他所有字符。
    3. 删除错误换行：如果一行换行后，下一行首个字符是中文、字母或数字，则拼接到上一行。
    4. 删除每一行开头的连续空格。
    5. 将文本中两个或以上的连续空格替换为一个换行符。

    :param input_file: 输入的txt文件路径
    :param output_file: 输出的清洗后txt文件路径
    """
    try:
        # 定义正则表达式
        valid_line_pattern = r'[a-zA-Z0-9\u4e00-\u9fa5]'  # 匹配包含字母、数字、中文的行
        valid_char_pattern = r'[^\u4e00-\u9fa5a-zA-Z0-9\u0020-\u007e\u3000-\u303f\uff00-\uffef\n]'  # 保留有效字符

        with open(input_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        cleaned_lines = []
        for line in lines:
            # 删除没有字母、数字、中文字符的行
            if not re.search(valid_line_pattern, line):
                continue

            # 清洗行内容，保留有效字符
            cleaned_line = re.sub(valid_char_pattern, '', line)
            cleaned_lines.append(cleaned_line)

        # 删除错误换行并拼接
        final_lines = []
        for line in cleaned_lines:
            if final_lines and re.match(r'^[\u4e00-\u9fa5a-zA-Z0-9]', line):  # 如果下一行以中文、字母或数字开头
                final_lines[-1] = final_lines[-1].rstrip('\n') + line.strip()  # 拼接到上一行
            else:
                final_lines.append(line)

        # 删除每一行开头的连续空格
        final_lines = [re.sub(r'^\s+', '', line) for line in final_lines]

        # 将两个或以上的连续空格替换为一个换行符
        final_text = ''.join(final_lines)
        final_text = re.sub(r' {2,}', '\n', final_text)

        # 将清洗后的内容写入输出文件
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(final_text)

        print(f"清洗完成！清洗后的文件已保存到: {output_file}")

    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    # 从命令行参数获取文件名
    if len(sys.argv) < 2:
        print("缺少文件名参数")
        sys.exit(1)

    name = sys.argv[1]

    # 根据文件名生成输入和输出路径
    base_path = os.path.join(os.getcwd(), "两步版本", "原始文件")  # 输入文件夹路径
    output_base_path = os.path.join(os.getcwd(), "两步版本", "过程文件")  # 输出文件夹基础路径
    output_path = os.path.join(output_base_path, name)  # 输出文件夹路径

    clean_folder_path = os.path.join(output_path, "1st清洗")
    if not os.path.exists(clean_folder_path):
        os.makedirs(clean_folder_path)
        print(f"已创建文件夹：{clean_folder_path}")
    else:
        print(f"文件夹已存在：{clean_folder_path}")



    input_file = os.path.join(base_path, f"{name}.txt")
    output_file = os.path.join(clean_folder_path, f"{name}.txt")

    if not os.path.exists(input_file):
        print(f"输入文件不存在：{input_file}")
        sys.exit(1)

    if not os.path.exists(clean_folder_path):
        os.makedirs(clean_folder_path)


clean_txt_file(input_file, output_file)
print(f"清洗完成，输出文件：{output_file}")