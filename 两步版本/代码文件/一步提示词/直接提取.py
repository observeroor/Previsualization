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
                客观视觉描述工程。
                你需要代入小说中旁观者的眼睛，或者男性角色的眼睛，对你在小说中看到的性感、刺激、血脉喷张的画面进行客观视觉描述。
                要将中文里一些比喻的表现手法要转化为简单、不引起歧义的描述
                客观视觉描述直白、用语简单，不包含任何隐喻、比喻、心理活动，对身体部位、衣服等采用标准描述而不是采用比喻（例如：penis而不是肉棒）
                将提供的小说描述成8到12个画面，以展现小说的连续情节，必须要视觉化表述出一些具有性行为、性暗示、性张力的画面
                客观视觉化描述的要求
                [
                1.要以画面中的女性角色为视觉中心（主要就是为了让读者以客观视觉的词语欣赏场景中女性的淫荡表现）
                2.可以选择从旁观者视角描述女性角色与男性角色的行为画面，也可以从小说中的男性角色的眼睛视角描述看到的女性角色的淫荡画面，也可以用色情摄影作品中会用到视角描述画面
                3.要突出色情细节（如沾上精液的短裙）、美丽青春、纸醉金迷（金色、亮色、粉色等色彩）、上瘾、沉溺（药物痕迹）、性欲（高潮脸）、肉体荷尔蒙(男性肌肉线条，女生身体线条，女性光滑洁白的皮肤)等，避免恐惧、恐怖；
                ]
                描述条目：
                前景包含人物动作、人物脸部细节、人物身体细节
                    人物动作：
                    人物脸部细节：
                    人物身体细节：
                中景内容包含4条物品要点，选取场景物品、细节，如家具、装饰、道具、衣物、食物、饮品等的描写，物品描写要突出状态、材质、位置（如桌子上打翻的水杯，床底下用过的安全套，刻有willan名字的震动棒，撕开网袜）
                背景内容包含描写当前场景发生的环境
                

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
