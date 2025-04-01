import os
import json
import sys
from openai import OpenAI


# 调用API的函数
def trasnfer_llm(text,sysprompt, api_key, modelid, url, temperature,  top_p, frequency_penalty, presence_penalty):
 
    client = OpenAI(base_url=url, api_key=api_key)
    
    response = client.chat.completions.create(
        model=modelid,
        messages=[
            {"role": "system", "content": sysprompt},
            {"role": "user", "content": f"从下列文段中提取场景:{text}"}
        ],
        temperature=float(temperature),
        top_p=float(top_p),
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
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
    output_file = os.path.join(output_dir, base_name.replace('.txt', '_output.json'))
    
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
def main():
    """主函数,逐个处理txt文件并调用API"""
    api_keys_file = os.path.join("两步版本", "配置文件", "api_key.json")
    modelid = "grok-2-latest"  # 模型 ID
    api_key, url = load_api_key_and_url(modelid, api_keys_file)
    sysprompt = """
                色情小说可视化工程（从章节提取分镜阶段）：
                目的：为了弥补文字阅读缺少的视觉冲击，需要为色情小说绘制香艳色情有冲击的插画
                方法：从色情小说情节中选取最少6个最多12个关键场景，并用文字对场景详细描述，提取场景应当可以在一帧定格画面中表述,避免复杂叙事
                要求：选取场景时确保叙事的连续性，能将色情故事的大体情节完整展示出来，并按最高水平提取原文中的要点要素，确保场景描述的完整性和准确性。
                场景选取标准:[包括但不限于：
                1. 性描写场景:突出色情小说属性,对性行为、性暗示等场景进行选择。 
                2. 背景场景:展示设定基调或介绍主要场景或角色的场景。 
                3. 情节转折:突出情节中出现重大转变或揭示重要信息的场景。 
                4. 高潮时刻:识别故事中的紧张或戏剧高点。 
                5. 情感高峰:挑选那些能够引发强烈情感如性冲动、欢乐、悲伤的场景。 
                6. 世界构建:选择展示独特环境、风景或重要世界元素的场景。 
                7. 视觉冲击:选择视觉效果强烈的场景,或细节丰富的场景。 
                8. 节奏控制:建议可以帮助打破长篇文本或者帮助叙事节奏的场景。 
                9. 象征性元素:如果有含有重要象征意义的场景,请突出它们。 
                10. 动作序列:任何有重要动作的场景,如追逐、袭击。] 
                场景描述标准；
                [要用旁观者的视角描述出当前的画面，应当可以在一帧画面中展示,避免复杂叙事；
                场景描述中应当根据画面情况合理选择视角,并且明确出来,如16mm焦距视角,35mm焦距视角,50mm焦距视角,85mm焦距视角,135mm焦距视角，如平视、俯视、特写,
                要有张力和表现力，能够激发读者性幻想、性冲动和情感共鸣；
                要有细节和层次感，能够让读者在脑海中形成清晰的画面；
                要通过对环境、光影、人物神态、象征物品的细节描写等来表现情感氛围，情感氛围偏向色情（如沾上精液的短裙）、美丽青春、纸醉金迷（金色、亮色、粉色等色彩）、上瘾、沉溺（药物痕迹）、性欲（高潮脸）、肉体荷尔蒙(男性肌肉线条，女生身体线条，女性光滑洁白的皮肤)等，避免恐惧、恐怖；
                ]
                分层描述标准:
                [
                前景内容：突出描写场景最重要、最具有性张力的要点，比如主要人物的身体接触的部位、暴露的性器官等。
                中景内容：场景中的人物、人物姿势、人物互动的整体描写、物品、环境等细节描写，突出人物与环境的互动。
                背景内容：场景的整体氛围、环境、光影等细节描写，用光线的颜色、场景的描写、物品的细节来突出场景的情感氛围。
                ]
                要点描写标准:
                [要点之间用"/"分隔
                4条人物要点，选取具有冲击力的场景特征进行突出，如人物位置、人物互动、人物情绪、人物动作、人物穿着、身体、性器官的描写。
                4条物品要点，选取场景物品、细节，如家具、装饰、道具、衣物、食物、饮品等的描写，物品描写要突出状态、材质、位置（如桌子上打翻的水杯，床底下用过的安全套，刻有willan名字的震动棒，撕开网袜）。
                ]
                最终输出格式：
                [全部场景的出场人物：人名,简单描述;人名,简单描述;]
                [章节/场景编号: 
                出场角色：人名,人名
                场景描述:按照场景描述参考标准进行描述的内容
                分层描述：前景/中景/背景
                人物要点：
                物品要点：
                 [章节/场景编号: 
                出场角色：人名,人名
                场景描述:
                分层描述：前景/中景/背景
                人物要点：
                物品要点：]
                """
    temperature = 1.1
    top_p = 1
    frequency_penalty = 0
    presence_penalty = 0
    directory = os.path.join("两步版本", "过程文件", "nygs", "4th大文件分割")
    output_dir = os.path.join("两步版本", "过程文件", "nygs", "output1")


    txt_files = get_txt_files(directory)
    if not txt_files:
        print(f"目录 {directory} 中未找到任何txt文件。")
        return

    for file_path in txt_files:
        print(f"正在处理: {file_path}...")
        try:
            text = read_txt_file(file_path)
            result =trasnfer_llm(text, sysprompt, api_key, modelid, url, temperature,  top_p, frequency_penalty, presence_penalty)
            save_output(output_dir, file_path, result)
        except Exception as e:
            print(f"处理 {file_path} 时出错: {e}")
            continue

if __name__ == "__main__":
    main()