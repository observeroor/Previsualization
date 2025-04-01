import os
import json
from openai import OpenAI


# 调用API的函数
def trasnfer_llm(text,sysprompt, api_keys, modelid, url, temperature,  top_p, frequency_penalty, presence_penalty):
 
    client = OpenAI(base_url=url, api_key=api_keys)
    
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
    modelid = "deepseek-v3-250324"  # 模型 ID
    sysprompt = """
                色情小说可视化工程（从章节提取分镜阶段）：
                目的：为了弥补文字阅读缺少的视觉冲击，需要为色情小说绘制香艳色情有冲击的插画
                方法：从色情小说情节中选取6-12个关键场景，并用文字对场景详细描述，提取场景应当可以在一帧定格画面中表述,避免复杂叙事
                要求：选取场景时确保叙事的连续性，能将色情故事的大体情节完整展示出来，并按最高水平提取原文中的要点要素，确保场景描述的完整性和准确性。
                格式：[
                [全部场景的出场人物]
                [章节/场景编号: 
                出场角色：
                场景描述:
                要点描写：]
                [章节/场景编号: 
                出场角色：
                场景描述:]]
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
                场景描述参考标准；
                [要用旁观者的视角描述出当前的画面，应当可以在一帧画面中展示,避免复杂叙事；按最高水平提取原文中的要点要素，确保场景描述的完整性和准确性；要有张力和表现力，能够激发读者性幻想、性冲动和情感共鸣；
                要有细节和层次感，能够让读者在脑海中形成清晰的画面；要有情感和氛围，能够让读者感受到场景的情感和氛围；要有动作和动态，能够让读者感受到场景的动作和动态；要有色彩和光影，能够让读者感受到场景的色彩和光影；要有声音和气味，能够让读者感受到场景的声音和气味；要有时间和空间，能够让读者感受到场景的时间和空间；要有人物和关系，能够让读者感受到场景的人物和关系；要有冲突和张力，能够让读者感受到场景的冲突和张力；要有象征和隐喻，能够让读者感受到场景的象征和隐喻。
                ]
                要点描写参考标准:
                [包括但不限于以下要素:
                背景、人物位置、人物互动、人物情绪、人物动作、人物穿着、身体、性器官的描写。
                场景描述中应当根据画面情况合理选择视角,并且明确出来,如16mm焦距视角,35mm焦距视角,50mm焦距视角,85mm焦距视角,135mm焦距视角，如平视、俯视、特写,
                ]"""
    temperature = "0.7"
    top_p = 1
    frequency_penalty = 0
    presence_penalty = 0
    directory = os.path.join("两步版本", "过程文件", "nygs", "4th大文件分割")
    output_dir = os.path.join("两步版本", "过程文件", "nygs", "output")
    api_keys = "09d01e0f-0a98-44d6-93c6-5088b4307f82"
    url = "https://ark.cn-beijing.volces.com/api/v3/"

    txt_files = get_txt_files(directory)
    if not txt_files:
        print(f"目录 {directory} 中未找到任何txt文件。")
        return

    for file_path in txt_files:
        print(f"正在处理: {file_path}...")
        try:
            text = read_txt_file(file_path)
            result =trasnfer_llm(text, sysprompt, api_keys, modelid, url, temperature,  top_p, frequency_penalty, presence_penalty)
            save_output(output_dir, file_path, result)
        except Exception as e:
            print(f"处理 {file_path} 时出错: {e}")
            continue

if __name__ == "__main__":
    main()