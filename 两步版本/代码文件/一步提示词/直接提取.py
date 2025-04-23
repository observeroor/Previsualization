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
                客观视觉描述直白、用语简单，不包含任何隐喻、比喻、心理活动，对身体部位、衣服等采用标准描述而不是采用比喻（例如：penis而不是肉棒）；不采用“像**一样”的描述方式
                将提供的小说描述成8到12个画面，以展现小说的连续情节，必须要视觉化表述出一些具有性行为、性暗示、性张力的画面
                客观视觉化描述的要求
                [
                1.要以画面中的女性角色为视觉中心（主要就是为了让读者以客观视觉的词语欣赏场景中女性的淫荡表现）
                2.可以选择从旁观者视角描述女性角色与男性角色的行为画面，也可以从小说中的男性角色的眼睛视角描述看到的女性角色的淫荡画面，也可以用色情摄影作品中会用到视角描述画面
                3.要突出色情细节（如沾上精液的短裙）、美丽青春、纸醉金迷（金色、亮色、粉色等色彩）、上瘾、沉溺（药物痕迹）、性欲（高潮脸）、肉体荷尔蒙(男性肌肉线条，女生身体线条，女性光滑洁白的皮肤)等，避免恐惧、恐怖；
                4.不使用解释说明，不包含抽象的解释、心理活动。
                ]
                描述条目：
                前景人物姿势动作：用精准的短语描述出当前人物的身体姿势和行为动作
                前景人物身体要点：突出描写当前人物行为、身体姿势中与性行为最密切相关的部分，如短裙底下暴露的阴户等
                前景人物脸部细节：详细的描述当前人物的表情细节，包括脸部、眉毛、嘴巴、眼睛、发型（注意同一角色在所有场景中要保持一致）、特殊状态（如被射精在脸上）、头发上的装饰、脸部表情（要根据当前角色心理状态进行推测，主要表现出女性的柔弱、欲拒还拒、妩媚淫荡、背德感等让男性产生性欲、爱欲的表情，不要出现会影响人物美的描述词）、眼睛表情、嘴巴表情（如：因做爱而微微张开）、脸部的特殊状态（如：因性高潮而微红）、脸部的装饰物（如：小巧的黑色耳钉）]
                    在描述人物脸部细节的时候，要尽量减少会造成画面混乱、影响美感的描写；一定不能出现如：乱糟糟的头发、散乱的头发、乌青的眼眶等相似的描写
                前景人物身体细节：描述身体没有穿着服装的裸露部位；如果是裸露则要说明处于裸露状态，如果不是裸露则直接描述服装[一定要判断身体部位是否裸露，如果裸露则要强调裸露，并且突出性张力、性暗示地描写裸露的部位，身体部位参考顺序：躯干、颈部、胸部、背部，屁股、阴部、胳膊、手、大腿、小腿]
                前景人物服装细节：描述身体、四肢各个部位的服装细节和特殊状态，服装描述要包括服装设计、穿着状态（eg：三角镂空露出乳沟的苹果绿Ｔ恤，卡其色鹿皮绒短裤，大腿大部分裸露），如果没有服装，就要描述裸露的部位和皮肤状态（eg：粉色丝绸上衣半脱到胸部,裸露的屁股上有的微微的红色掌印,黑色网状蕾丝丝袜褪到膝盖被淫液沾湿））。
                    [服装描述参考顺序:上半身(如裸露or轻薄的白色蕾丝绑带内衣，近乎全裸or乳白色贴身挂脖旗袍，高开叉旗袍)、手部(如：裸露或白色蕾丝手套)、下半身(如：全裸或超短百褶裙)、脚(鞋、指甲油等)，]
                中景内容包含4条物品要点，选取场景物品、细节，如家具、装饰、道具、衣物、食物、饮品等的描写，物品描写要突出状态、材质、位置（如桌子上打翻的水杯，床底下用过的安全套，刻有willan名字的震动棒，撕开网袜）
                背景内容包含描写当前场景发生的地点和环境描述
                背景中场所地点只需直白指出当前的场所地点（电影院、阁楼的房间、户外草坪、警察局门口等），无需额外的形容词描述（不出现昏暗、黑暗等）
                最终输出格式（以json格式输出）：
{
    "全部场景的出场人物":{"人名":"简单描述","人名":"简单描述"},
    "XX-XX(场景编号)":{
        "出场角色":"人名,人名"
        "前景人物姿势动作"："*"
        "前景人物身体要点"："*"
        "前景人物脸部细节"："*"
        "前景人物身体细节"："*"
        "前景人物服装细节"："*"
        "中景物品要点"："*"
        "背景场所"："*"
        "背景描述"："*"
    },
    "XX-XX(场景编号)":{
        "出场角色":"人名,人名"
        "前景人物姿势动作"："*"
        "前景人物身体要点"："*"
        "前景人物脸部细节"："*"
        "前景人物身体细节"："*"
        "前景人物服装细节"："*"
        "背景场所地点"："*"
        "背景描述"："*"
    },
}
                """
    temperature = 1.1
    top_p = 1
    frequency_penalty = 0
    presence_penalty = 0
    directory = os.path.join("两步版本", "过程文件", "nygs", "4th大文件分割")
    output_dir = os.path.join("两步版本", "过程文件", "nygs", "直接提取", "分镜提取")


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
