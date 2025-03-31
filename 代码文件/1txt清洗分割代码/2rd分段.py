import sys
import os
import re

def split_novel_by_chapters(input_file, output_dir):
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 读取整个小说文本
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # 使用正则表达式匹配章节标题，例如“第1章”或“第十章”
    chapters = re.split(r'(第[一二三四五六七八九十百千0-9]+章)', content)

    # 如果分割后的列表长度小于 3，说明没有匹配到章节
    if len(chapters) < 3:
        print("未找到章节分隔符，请检查输入文件格式。")
        return

    # 合并章节标题和内容
    chapters = ["".join(chapters[i:i+2]) for i in range(1, len(chapters), 2)]

    # 保存每一章到单独的文件
    for i, chapter in enumerate(chapters):
        chapter_title = chapter.split('\n', 1)[0].strip()  # 获取章节标题
        output_file = os.path.join(output_dir, f"chapter_{i+1}.txt")
        with open(output_file, 'w', encoding='utf-8') as out_file:
            out_file.write(chapter)
        print(f"已保存: {output_file}")


if __name__ == "__main__":
    # 从命令行参数获取文件名
    if len(sys.argv) < 2:
        print("缺少文件名参数")
        sys.exit(1)

    name = sys.argv[1]

    # 根据文件名生成输入和输出路径
    base_path = os.path.join(os.getcwd(), "两步版本", "过程文件", name)  # 文件夹路径
    input_path = os.path.join(base_path, "1st清洗")  # 输入文件夹路径
    output_path = os.path.join(base_path, "2rd分段")  # 输出文件夹基础路径

    work_folder_path = os.path.join(base_path, "2rd分段")
    if not os.path.exists(work_folder_path):
        os.makedirs(work_folder_path)
        print(f"已创建文件夹：{work_folder_path}")
    else:
        print(f"文件夹已存在：{work_folder_path}")

    input_file = os.path.join(input_path, f"{name}.txt")
    output_dir = work_folder_path

    if not os.path.exists(input_file):
        print(f"输入文件不存在：{input_file}")
        sys.exit(1)

    if not os.path.exists(work_folder_path):
        os.makedirs(work_folder_path)

split_novel_by_chapters(input_file, output_dir)