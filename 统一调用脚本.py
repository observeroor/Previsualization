import os
import subprocess
import sys
import json

def load_api_key_and_url(modelid, api_keys_file):
    """
    从 api_keys.json 文件中加载指定 modelid 的 api_key 和 url。
    :param modelid: 模型 ID
    :param api_keys_file: api_keys.json 文件路径
    :return: (api_key, url)
    """
    if not os.path.exists(api_keys_file):
        print(f"API 密钥文件未找到：{api_keys_file}")
        sys.exit(1)

    with open(api_keys_file, 'r', encoding='utf-8') as file:
        api_keys = json.load(file)

    if modelid not in api_keys:
        print(f"未找到模型 ID {modelid} 的 API 配置。")
        sys.exit(1)

    return api_keys[modelid]["api_key"], api_keys[modelid]["url"]

def main():
    ########## 在此定义参数 ##########
    # 子脚本路径
    script_path = os.path.join("两步版本", "代码文件", "2", "通用模型批量调用脚本报错.py")

    # 参数定义
    modelid = "grok-2-1212"  # 模型 ID
    sysprompt = "色情小说可视化工程（从章节提取分镜阶段）："
    temperature =  "0.7"
    top_p = "1"
    frequency_penalty = "0"
    presence_penalty = "0"
    directory = os.path.join("两步版本", "过程文件", "nygs", "4th大文件分割")
    output_dir = os.path.join("两步版本", "过程文件", "nygs", "output")

    # API 密钥文件路径
    api_keys_file = os.path.join("两步版本", "配置文件", "api_keys.json")

    ########## 加载 API 配置 ##########
    api_key, url = load_api_key_and_url(modelid, api_keys_file)

    ########## 转换为绝对路径 ##########
    script_path = os.path.abspath(script_path)
    directory = os.path.abspath(directory)
    output_dir = os.path.abspath(output_dir)

    # 检查子脚本是否存在
    if not os.path.exists(script_path):
        print(f"子脚本未找到：{script_path}")
        return

    # 打印调试信息
    print(f"使用的Python解释器：{sys.executable}")
    print(f"子脚本路径：{script_path}")
    print(f"模型 ID：{modelid}")
    print(f"API Key：{api_key}")
    print(f"URL：{url}")
    print(f"输入目录：{directory}")
    print(f"输出目录：{output_dir}")

    ########## 构造命令 ##########
    command = [
        sys.executable, script_path,
        directory, output_dir, sysprompt, api_key, modelid, url,
        temperature,  top_p, frequency_penalty, presence_penalty
    ]

    ########## 调用子脚本 ##########
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        print("子脚本执行成功！")
        print("子脚本输出：")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("子脚本执行失败！")
        print(f"错误信息：{e.stderr}")
    except FileNotFoundError as e:
        print("无法找到Python解释器或子脚本！")
        print(f"错误信息：{e}")

if __name__ == "__main__":
    main()
