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
def Scene_extraction():
    """主函数,逐个处理txt文件并调用API"""
    api_keys_file = os.path.join("两步版本", "配置文件", "api_key.json")
    modelid = "grok-3"  # 模型 ID
    api_key, url = load_api_key_and_url(modelid, api_keys_file)
    sysprompt = """
                色情小说可视化工程（从章节提取分镜阶段）：
                目的：为了弥补文字阅读缺少的视觉冲击，需要为色情小说绘制香艳色情有冲击的插画
                方法：从色情小说情节中选取最少6个最多12个关键场景，并用文字对场景详细描述，提取场景应当可以在一帧定格画面中表述,避免复杂叙事
                要求：按各种标准进行生成，按格式要求进行输出。
                场景选取标准:[
                像改编成漫画一样选取场景，确保叙事的连续性，能将色情故事的情节完整展示出来
                突出性描写场景，强调色情小说属性,对性行为、性暗示等场景必须进行选择
                ] 
                场景描述标准；
                [要视觉化描述的方法描述出当前的画面，应当可以在一帧画面中展示,避免复杂叙事；
                要以画面中的女性角色为视觉中心，可以选择从旁观者视角描述画面、也可以从小说中的“可反”的视角会看到的画面场景描述画面、其他电影摄影中会用到视角描述画面
                场景描述中应当根据画面情况合理选择远近，远近描述词：medium_shot,long_shot,establishing_shot,point-of-view_shot,cowboy_shot,medium_full_shot,full_shot,upper_body_shot,full_body_shot
                要有张力和表现力，能够激发读者性幻想、性冲动和情感共鸣；
                要有细节和层次感，能够让读者在脑海中形成清晰的画面；
                要通过对环境、光影、人物神态、象征物品的细节描写等来表现情感氛围，情感氛围偏向色情（如沾上精液的短裙）、美丽青春、纸醉金迷（金色、亮色、粉色等色彩）、上瘾、沉溺（药物痕迹）、性欲（高潮脸）、肉体荷尔蒙(男性肌肉线条，女生身体线条，女性光滑洁白的皮肤)等，避免恐惧、恐怖；
                ]
                分层描述标准:
                [
                前景内容：突出描写场景最重要、最具有性张力的要点，比如主要人物的身体接触的部位、暴露的性器官等。
                中景内容：场景中的人物、人物姿势、人物互动的整体描写、物品、环境等细节描写，突出人物与环境的互动。
                背景内容：描写独特环境、风景或重要世界元素。场景的整体氛围、环境、光影等细节描写，用光线的颜色、场景的描写、物品的细节来突出场景的情感氛围。
                ]
                要点描写标准:
                [要点之间用"/"分隔
                4条人物要点，选取具有冲击力的场景特征进行突出，如人物位置、人物互动、人物情绪、人物动作、人物穿着、身体、性器官的描写。
                4条物品要点，选取场景物品、细节，如家具、装饰、道具、衣物、食物、饮品等的描写，物品描写要突出状态、材质、位置（如桌子上打翻的水杯，床底下用过的安全套，刻有willan名字的震动棒，撕开网袜）。
                ]
                最终输出格式（以json格式输出）：
{
    "全部场景的出场人物":{"人名":"简单描述","人名":"简单描述"},
    "XX-XX(场景编号)":{
        "出场角色":"人名,人名"
        "远近描述"："xxxx_shot"
        "场景描述":"内容"
        "分层描述":"前景/中景/背景"
        "人物要点":"要点1/要点2/要点3/要点4"
        "物品要点":"要点1/要点2/要点3/要点4"
    },
    "XX-XX(场景编号)":{
        "出场角色":"人名,人名"
        "远近描述"："xxxx_shot"
        "场景描述":"内容"
        "分层描述":"前景/中景/背景"
        "人物要点":"要点1/要点2/要点3/要点4"
        "物品要点":"要点1/要点2/要点3/要点4"
    }
}
                """
    temperature = 1.1
    top_p = 1
    frequency_penalty = 0
    presence_penalty = 0
    directory = os.path.join("两步版本", "过程文件", "nygs", "4th大文件分割")
    output_dir = os.path.join("两步版本", "过程文件", "nygs", "grok-3", "分镜提取")


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
    Scene_extraction()