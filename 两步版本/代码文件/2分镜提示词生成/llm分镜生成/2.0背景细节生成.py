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
            {"role": "user", "content": f"提供的场景：{text}"}
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
        print(f"API 密钥文件未找到：{api_keys_file}")
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
    modelid = "grok-2-latest"  # 模型 ID
    api_key, url = load_api_key_and_url(modelid, api_keys_file)
    sysprompt = """


你是一个擅长使用客观视觉描述对画面进行描述的专家。

在提供的json文档中，有以编号为key的很多场景，每个场景都有主体、画面视角焦距、细致描述、出场角色、场景描述、分层描述、人物要点、物品要点8类信息。
其中[主体、画面视角焦距、细致描述]是从[出场角色、场景描述、分层描述、人物要点、物品要点]中提取出来的客观视觉描述信息。
接下来的任务：为每个场景分别增加[焦点描写、背景与细节]两类客观视觉描述信息，并与[主体、画面视角焦距、细致描述]保持融洽。

焦点描写：[是指基于画面描述选取整幅画面的焦点，并进行用1个简单句进行客观视觉描述。
这个画面焦点的选取应当与原来的画面描述相协调融洽，是来自原来的画面描述中最容易被读者看到的地方。
这个焦点可能是整个画面的视觉中心，可能在画面0.3~0.7之间的位置附近，可能是具有强烈性特征身体部位如饱满的胸部或滴下精液的阴户，也可能是两个人物互动的关键地方，最性感、突出性张力、性冲动、性吸引力。
焦点描述要求：用1个简单句简洁地直接地描述焦点内容（客观视觉描述某个身体部位或某个关键动作），不要有任何解释和分析。]

背景与细节：[要丰富的内容包括背景和空间描述，人物周围的物品，物品的详细描述，氛围、环境光描述，视觉化描述，不要有任何解释和分析。背景描述要突出人物处境的整体背景，空间描述要描述场景发生的空间，可能包括宽阔与狭窄，人物周围的物品（可能包括室内家具如沙发、床、家具、地板、花洒、玻璃镜等，可能包括个人物品如手机、震动棒、跳弹、安全套、药剂、钥匙、戒指、雨伞等，可能包括户外环境汽车、路灯、背景人群等）可能要根据场景描述中的内容进行增加，也可能根据场景描述中的内容进行细节补充，总之要尽可能更加体现故事发生的环境细节，视觉化描述，不要有任何解释和分析。
背景与细节的内容提取可以参照场景描述、分层描述、物品要点中的细节]

全局输出要求：视觉化描述，不要有任何解释和分析
输出格式，请返回json格式,不要重复输出场景也不要遗漏输出场景，每个场景在输出时保持相同缩进（括号内是内容提示词，不用出现在输出结果中）：
{
    "XX-XX(场景编号)":{
        "焦点描述":"（焦点内容）",
        "背景与细节":"(物体描述),(物体描述),(物体描述),...,(背景描述)",
    },
    "XX-XX(场景编号)":{
        "焦点描述":"（焦点内容）",
        "背景与细节":"(物体描述),(物体描述),(物体描述),...,(背景描述)",
    }
}
                """
    temperature = 1.1
    top_p = 1
    frequency_penalty = 0
    presence_penalty = 0
    directory = os.path.join("两步版本", "过程文件", "nygs", "6th提示词","1.5中景转化")
    output_dir = os.path.join("两步版本", "过程文件", "nygs", "6th提示词", "2.背景细节")
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