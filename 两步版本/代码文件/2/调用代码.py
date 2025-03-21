import os
import requests

def convert_chapter_to_storyboard(api_url, api_key, chapter_text):
    """
    调用 Grok 的 LLM 模型 API，将小说章节转化为分镜提示词。

    :param api_url: Grok LLM 模型的 API URL
    :param api_key: API 密钥
    :param chapter_text: 小说章节内容
    :return: 分镜提示词
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "input": chapter_text,
        "model": "storyboard-generator"  # 假设模型名称为 storyboard-generator
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()  # 如果响应状态码不是 200，抛出异常
        result = response.json()
        return result.get("storyboard", "未生成分镜提示词")
    except requests.exceptions.RequestException as e:
        print(f"调用 API 时发生错误: {e}")
        return None

def process_txt_files(input_folder, output_folder, api_url, api_key):
    """
    遍历文件夹中的所有 txt 文件，将每个章节转化为分镜提示词，并保存到输出文件夹。

    :param input_folder: 包含小说章节的 txt 文件夹路径
    :param output_folder: 输出分镜提示词的文件夹路径
    :param api_url: Grok LLM 模型的 API URL
    :param api_key: API 密钥
    """
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历输入文件夹中的所有 txt 文件
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            input_file_path = os.path.join(input_folder, filename)
            output_file_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_storyboard.txt")

            # 读取章节内容
            with open(input_file_path, "r", encoding="utf-8") as file:
                chapter_text = file.read()

            # 调用 API 转化为分镜提示词
            print(f"正在处理文件: {filename}")
            storyboard = convert_chapter_to_storyboard(api_url, api_key, chapter_text)

            # 保存分镜提示词到输出文件
            if storyboard:
                with open(output_file_path, "w", encoding="utf-8") as output_file:
                    output_file.write(storyboard)
                print(f"分镜提示词已保存到: {output_file_path}")
            else:
                print(f"文件 {filename} 的分镜提示词生成失败。")

if __name__ == "__main__":
    # 配置参数
    input_folder = r"c:\Git\Previsualization\两步版本\小说章节"  # 输入文件夹路径
    output_folder = r"c:\Git\Previsualization\两步版本\分镜提示词"  # 输出文件夹路径
    api_url = "https://api.grok.com/v1/storyboard"  # Grok LLM 模型的 API URL
    api_key = "your_api_key_here"  # 替换为你的 API 密钥

    # 调用处理函数
    process_txt_files(input_folder, output_folder, api_url, api_key)