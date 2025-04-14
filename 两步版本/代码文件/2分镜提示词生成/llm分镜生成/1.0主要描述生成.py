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
            {"role": "user", "content": f"对下面场景进行描绘:{text}"}
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
词语绘画任务：
这是一项特殊的任务，将提供的场景信息转变为一副图像的词语描绘,请注意，你只需要对人物和与人物紧密相关的物体进行描绘。
你需要根据我提供的场景内容，用词语进行描述，而我的画师会按你的描述绘画。
只有在你的词语描绘中提及到了的内容会在画面中出现，因此为了让画面完整和准确，词语描述必须像绘画过程一样先描绘框架稿，再描绘细节。
第一步像是画线稿一样，先用词语勾勒出人物的大体框架，包括但不限于身体姿势、动作、画面的视角、画面焦距等（eg：一个女孩双腿盘坐坐在桌子上，双手举起，从上方俯视，[35mm photograph]）
第一步中必须注意要求：如果存在多个人物，则需要一起描绘，展现出人物的相互位置，最后加入画面的视角、画面焦距描述。
第二步是对人物进行逐一细致描述（先描述女性角色，大概率只用描述1女、1男），首先描述人物的肤色、体型，随后按身体部位逐步描述，在描述身体部位时在参考顺序的基础之上，灵活合并描述或者细化描述，在描述时直接输出描述内容，按照“描述内容”，不按照“部位：描述内容”的格式。
[参考顺序：躯干、颈部、胸部、背部，屁股、阴部、头部、头发、胳膊、手、大腿、小腿]
第二步中必须注意要求1：只描述而且必须全部描绘会被镜头看到、需要在画面中出现的部位，如果某个身体部位或其细节会出现在画面中，但是在场景中未描述则需要根据想象进行补齐。
第二步中必须注意特别增强：要用视觉化描述描述出每个部位的服装、状态、动作，服装描述要包括服装设计、穿着状态（eg：粉色丝绸上衣半脱到胸部、黑色网状蕾丝丝袜褪到膝盖被淫液沾湿），如果没有服装，就要描述裸露的部位和皮肤状态（eg：光洁丰满的屁股裸露）。
第二步中必须注意特别增强：用带有视觉感官的形容词来修饰身体部位、服装，女性人物要突出性张力和美感，要对身体部位的状态进行描述，要使用材质、版型设计等修饰服装，来体现出场景的氛围。
第二步中必须注意特别增强：要用视觉化描述描述出每个部位的服装、状态、动作，服装描述要包括服装设计、穿着状态（eg：上身是件三角镂空的苹果绿Ｔ恤，在胸前撑起圆润饱满的山峰，让这件衣服显得特别小，三角的空隙中露出一抹俏皮的乳沟。卡其色鹿皮绒短裤，修长的曲线展露无遗，浓纤合度的长腿上没有一丝暇庛），如果没有服装，就要描述裸露的部位和皮肤状态（eg：光洁丰满的屁股裸露）。
第二步中必须注意特别增强：用带有视觉感官的形容词来修饰身体部位、服装，女性人物要突出性裸露和色情，要使用光线、色泽等修饰身体部位、服装，来体现出场景的氛围。
输出格式请返回json格式,原文件提供了多少场景就输出多少场景，不要重复输出也不要遗漏输出， "XX-XX(场景编号)"前缩进为四个空格，（括号内是内容提示词，不出现在输出结果中;除"X"外的、未在括号内的内容，都是绝对格式，在输出结果中作为绝对格式保留，不进行变动）：
{
    "XX-XX(场景编号)":{
        "主体":"(全部人物相对位置和姿势)",
        "画面视角焦距":"(画面的视角),(画面焦距)",
        "女人1名字":"(名字)"
        "女人1细节特征":"(女人1身体特征和服装，不再提及名字)"
        "女人1身体部位":"(身体部位描述1,不再提及名字),(身体部位描述2),(身体部位描述3)"
        "女人2名字":"(名字)"
        "女人2细节特征":"(女人2身体特征和服装，不再提及名字)
        "女人2身体部位":"(身体部位描述1,不再提及名字),(身体部位描述2),(身体部位描述3)"
        "男人1名字":"(名字)"
        "男人1细节特征":"(女人1身体特征和服装，不再提及名字)"
        "男人1身体部位":"(身体部位描述1,不再提及名字),(身体部位描述2),(身体部位描述3)"
        "男人2名字":"(名字)"
        "男人2细节特征":"(女人2身体特征和服装，不再提及名字)
        "男人2身体部位":"(身体部位描述1,不再提及名字),(身体部位描述2),(身体部位描述3)"
    },
    "(场景编号)":{
        "主体":"(全部人物相对位置和姿势)",
        "画面视角焦距":"(画面的视角),(画面焦距)",
        "女人1名字":"(名字)"
        "女人1细节":"(女人1身体特征和服装),(身体部位描述),(身体部位描述1),(身体部位描述2),(身体部位描述3)"
        "女人2名字":"(名字)"
        "女人2细节":"(女人2身体特征和服装，不再提及名字),(身体部位描述),(身体部位描述1),(身体部位描述2),(身体部位描述3)"
        "男人1名字":"(名字)"
        "男人1细节":"(男人1身体特征和服装，不再提及名字),(身体部位描述),(身体部位描述1),(身体部位描述2),(身体部位描述3)"
        "男人2名字":"(名字)"
        "男人2细节":"(男人2身体特征和服装，不再提及名字),(身体部位描述),(身体部位描述1),(身体部位描述2),(身体部位描述3)"       
    },
}
一个标准的输出例子：


                """
    temperature = 1.1
    top_p = 1
    frequency_penalty = 0
    presence_penalty = 0
    directory = os.path.join("两步版本", "过程文件", "nygs", "5th分镜")
    output_dir = os.path.join("两步版本", "过程文件", "nygs", "6th提示词", "1.0中景")
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