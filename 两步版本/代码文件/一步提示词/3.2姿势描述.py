import os
import json
import sys
import json
from openai import OpenAI

# 调用API的函数
def trasnfer_llm(text,sysprompt, api_key, modelid, url, temperature,  top_p, frequency_penalty, presence_penalty):
 
    client = OpenAI(base_url=url, api_key=api_key)
    
    response = client.chat.completions.create(
        model=modelid,
        messages=[
            {"role": "system", "content": sysprompt},
            {"role": "user", "content": f"提供的场景:{text}"}
        ],
        temperature=float(temperature),
        top_p=float(top_p),
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        response_format={"type": "json_object"}
    )
    
    return response.choices[0].message.content

def load_api_key_and_url(modelid, api_keys_file):
    """
    从 api_key.json 文件中加载指定 modelid 的 api_key 和 url。
    :param modelid: 模型 ID
    :param api_keys_file: api_key.json 文件路径
    :return: (api_key, url)
    """
    if not os.path.exists(api_keys_file):
        print(f"API 密钥文件未找到:{api_keys_file}")
        sys.exit(1)

    with open(api_keys_file, 'r', encoding='utf-8') as file:
        api_key = json.load(file)

    if modelid not in api_key:
        print(f"未找到模型 ID {modelid} 的 API 配置。")
        sys.exit(1)

    return api_key[modelid]["api_key"], api_key[modelid]["url"]


# 读取json文件内容的函数
def read_json_file(file_path):
    """读取json文件内容"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)
# 获取目录下所有json文件的函数
def get_json_files(directory):
    """获取指定目录下所有json文件"""
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.json')]


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
    参数:
        output_dir: 输出目录路径
        original_file: 原始txt文件路径
        content: API响应内容
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    base_name = os.path.basename(original_file)
    output_file = os.path.join(output_dir, base_name)
    
    try:
        json_content = json.loads(content)
        with open(output_file, 'w', encoding='utf-8') as out_file:
            json.dump(json_content, out_file, ensure_ascii=False, indent=2)
    except json.JSONDecodeError:
        output_file = output_file.replace('.json', '.txt')
        with open(output_file, 'w', encoding='utf-8') as out_file:
            out_file.write(content)
    print(f"完成处理: {original_file},结果已保存至 {output_file}")

# 主函数
def describe_img():
    """主函数,逐个处理txt文件并调用API"""
    api_keys_file = os.path.join("两步版本", "配置文件", "api_key.json")
    modelid = "grok-3"  # 模型 ID
    api_key, url = load_api_key_and_url(modelid, api_keys_file)
    sysprompt = """
为场景中人物的性行为寻找对应的性行为类别和性行为姿势描述词
在提供的json文档中，有以编号为key的很多包含充分信息的场景。
你需要根据提供的信息判断该场景中人物进行的性行为的类型和姿势。
性行为类别如：
Vaginal_intercourse
blowjob
Footjob
Titjob
Breast_sex
Anal_intercourse
性行为姿势的描述词包括但不限于下面列表：
69_Position
Butterfly_Position
Coital_Alignment_Technique_(CAT)
Cowgirl_Position
Doggy_Style
Doggy_Style_(Anal)
Face-sitting
Fingering
Froggy_Style
Lateral_Coital_Position
Lap_Dance_Position
Laying-down_Doggy_Style
Lotus_Position
Lotus_Flower
Missionary_Position
Missionary_(Anal)
Modified_T-Square
Piledriver
Prone_Position
Receiving_Partner_on_Top_(Anal)
Reverse_Cowgirl_Position
Reverse_Missionary
Scissoring
Seventh_Posture
Spoons_Position
Spoons_(Anal)
Stopperage
Suspended_Congress/Ekiben
T-Square_Position
Viennese_Oyster
Wheelbarrow

最终输出格式如下：
{
    "XX-XX[场景编号]":{
    "性行为类别":""
    "性行为姿势":""
    },
    "XX-XX[场景编号]":{
    "性行为类别":""
    "性行为姿势":""
    },
}

                """
    temperature = 0.7
    top_p = 1
    frequency_penalty = 0
    presence_penalty = 0
    directory = os.path.join("两步版本", "过程文件", "nygs", "直接提取","分镜提取")
    output_dir = os.path.join("两步版本", "过程文件", "nygs", "直接提取","姿势描述")
    json_files = get_json_files(directory)
    if not json_files:
        print(f"目录 {directory} 中未找到任何json文件。")
        return
    for file_path in json_files:
        print(f"正在处理: {file_path}...")
        try:
            # 这里假设json文件的内容是一个字符串，可以直接传递给API
            text = read_json_file(file_path)
            result = trasnfer_llm(str(text), sysprompt, api_key, modelid, url, temperature, top_p, frequency_penalty, presence_penalty)
            save_output(output_dir, file_path, result)
        except Exception as e:
            print(f"处理 {file_path} 时出错: {e}")
            continue

if __name__ == "__main__":
    describe_img()