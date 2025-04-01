# -*- coding: utf-8 -*-
import os
import sys
import json
import argparse
from openai import OpenAI
import traceback  # 用于捕获详细的错误信息

# 调用API的函数
def trasnfer_llm(text, sysprompt, api_key, modelid, url, temperature, top_p, frequency_penalty, presence_penalty):
    """
    调用 LLM 模型 API，将文本转化为分镜提示词。
    """
    try:
        client = OpenAI(base_url=url, api_key=api_key)

        response = client.chat.completions.create(
            model=modelid,
            messages=[
                {"role": "system", "content": f"{sysprompt}"},
                {"role": "user", "content": f"从下列文段中提取场景:{text}"}
            ],
            temperature=float(temperature),
            top_p=float(top_p),
            frequency_penalty=float(frequency_penalty),
            presence_penalty=float(presence_penalty),
        )

        return response.choices[0].message.content

    except Exception as e:
        # 捕获请求错误并返回详细信息
        error_message = f"调用 API 时发生错误: {str(e)}"
        print(error_message)
        traceback.print_exc()  # 打印详细的错误堆栈信息
        return f"API 调用失败: {error_message}"

# 读取txt文件内容的函数
def read_txt_file(file_path):
    """读取txt文件内容"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# 获取目录下所有txt文件的函数
def get_txt_files(directory):
    """获取指定目录下所有txt文件"""
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.txt')]

# 保存输出结果的函数
def save_output(output_dir, original_file, content):
    """
    保存API响应内容到指定输出目录。
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    base_name = os.path.basename(original_file)
    output_file = os.path.join(output_dir, base_name.replace('.txt', '_output.json'))

    try:
        json_content = json.loads(content)
        with open(output_file, 'w', encoding='utf-8') as out_file:
            json.dump(json_content, out_file, ensure_ascii=False, indent=2)
    except json.JSONDecodeError:
        output_file = output_file.replace('.json', '.txt')
        with open(output_file, 'w', encoding='utf-8') as out_file:
            out_file.write(content)
    print(f"完成处理: {original_file}, 结果已保存至 {output_file}")

# 主函数
def main(directory, output_dir, sysprompt, api_key, modelid, url, temperature, top_p, frequency_penalty, presence_penalty):
    """主函数,逐个处理txt文件并调用API"""
    txt_files = get_txt_files(directory)
    if not txt_files:
        print(f"目录 {directory} 中未找到任何txt文件。")
        return

    for file_path in txt_files:
        print(f"正在处理: {file_path}...")
        try:
            text = read_txt_file(file_path)
            result = trasnfer_llm(text, sysprompt, api_key, modelid, url, temperature, top_p, frequency_penalty, presence_penalty)
            save_output(output_dir, file_path, result)
        except Exception as e:
            # 捕获并打印详细错误信息
            print(f"处理 {file_path} 时出错: {e}")
            traceback.print_exc()  # 打印详细的错误堆栈信息
            continue

# 命令行参数处理
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="将小说章节txt文件转化为分镜提示词")
    parser.add_argument("directory", help="包含txt文件的目录路径")
    parser.add_argument("output_dir", help="输出文件保存目录")
    parser.add_argument("api_key", help="秘钥")
    parser.add_argument("modelid", help="模型ID")
    parser.add_argument("url", help="API URL")
    parser.add_argument("sysprompt", help="系统提示词")
    parser.add_argument("temperature", type=float, help="温度")
    parser.add_argument("top_p", type=float, help="top_p")
    parser.add_argument("frequency_penalty", type=float, help="频率惩罚")
    parser.add_argument("presence_penalty", type=float, help="出现惩罚")
    args = parser.parse_args()

    main(args.directory, args.output_dir, args.sysprompt, args.api_key, args.modelid, args.url, args.temperature, args.top_p, args.frequency_penalty, args.presence_penalty)