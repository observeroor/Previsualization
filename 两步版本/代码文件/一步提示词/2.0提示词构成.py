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

将背景描述转化成提示词的语法格式
你是一个擅长构建Stable Diffusion prompts的专家。
首先你已经充分的知晓了Stable Diffusion prompts的相关语法。
在提供的json文档中，有以编号为key的很多包含充分信息的场景。
你需要将场景转化为Stable Diffusion prompts。

Stable Diffusion prompts会用Korean girl称呼女性，而不是提及名字（因为Stable Diffusion无法识别名字）
关键逻辑：你必须将焦点内容、女人1头部脸部、女人1身体特征、女人1身体部位、背景与细节直白化，并在依次输出，用","分隔。
直白化可以参考的例子：（小慧红唇被迫含着赵成杰的肉棒，嘴角溢出唾液滑落至下巴）转化成（女孩在口交，唾液流到下巴）
直白化可以参考的例子：（两条腿摆出180度的高难度姿势）转化成（Standing split）
优秀的Stable Diffusion prompts在语法上直白的短语构成,不包含任何隐喻、心理活动，对性器官会采用标准描述而不是采用比喻
不采用“像**一样”的描述方式，不出现messy等增加混乱度的词语
用短语直白的描述身体姿势
这是包含许多种用于描述身体姿势的词组列表，可以直接从列表选取，也可以参照其进行编写：{crouching|squatting|low_squat|legs_apart|wide_stance|knees_up|one_knee_up|one_knee_on_the_ground|leaning_forward|hand_on_knee|hand_between_legs|side_profile_squat|wall_squat|sitting_on_heels|provocative_pose|suggestive_pose|spreading_legs|legs_up|arched_back|looking_back_seductively|resting_on_one_knee|bent_over|all_fours|lying_on_stomach|lying_on_side|thigh_gap|legs_together|hips_thrust_forward}
优秀的Stable Diffusion prompts在语法上由一组一组的直白的短语构成,这些短语不包含任何隐喻、心理活动,可以参照例子：

焦点内容的例子:( Korean girl ,sexy ，taking in a giant penis, skimpy sexy clothes, showing lots of skin) 


注意，焦点内容中不对背景和环境进行描写，只突出人物相关的内容
女人1头部脸部：(aqua eyes, blonde hair, blush, eyelashes, hair ornament, heart, heart-shaped pupils, heart background, heart hair ornament, long hair, looking at viewer, one side up, open mouth)
输出英文结果
输出格式如下，括号[]内的内容只是提示，不出现在最终输出结果中：
{
    "XX-XX[场景编号]":{

    },   
    "XX-XX[场景编号]":{

    },
}

                """
    temperature = 0.7
    top_p = 1
    frequency_penalty = 0
    presence_penalty = 0
    directory = os.path.join("两步版本", "过程文件", "nygs", "5.1提示词","1.0分镜提取")
    output_dir = os.path.join("两步版本", "过程文件", "nygs", "5.1提示词", "2.0提示词构成")
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