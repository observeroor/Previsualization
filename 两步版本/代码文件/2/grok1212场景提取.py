import os
import sys  
import json
import argparse
from openai import OpenAI

# 调用API的函数
def call_grok_api(text, api_key):
    """
    调用Grok beta模型API,将小说章节文本转化为分镜提示词。
    参数:
        text: 小说章节的文本内容
        api_key: xAI API密钥
        temperature: 模型温度(默认0.7)
        max_tokens: 最大令牌数(默认1024)
    返回:
        API响应内容(字符串)
    """
    client = OpenAI(base_url="https://api.x.ai/v1", api_key=api_key)
    
    response = client.chat.completions.create(
        model="grok-2-1212",
        messages=[
            {"role": "system", "content": "将色情小说可视化,从小说文段中选取6-12个关键场景,并用文字详细描述场景。场景选取时,既要参考关键场景选取的标准,也要注意色情故事叙事的连续性,要确保选取的场景能将色情故事的大体情节完整展示出来。 关键场景选取参考标准: [根据以下参考分析文本并选取包括但不限于符合下面条件场景,: 1. 性描写场景:要考虑到色情小说的特殊性,更有针对性地生产分镜 2. 开场场景:选择一个设定基调或介绍主要场景或角色的场景。 3. 情节转折:突出情节中出现重大转变或揭示重要信息的场景。 4. 高潮时刻:识别故事中的紧张或戏剧高点。 5. 角色介绍:当一个关键角色首次亮相时,建议将其作为插图。 6. 情感高峰:挑选那些能够引发强烈情感如欢乐、悲伤或恐惧的场景。 7. 世界构建:选择展示独特环境、风景或重要世界元素的场景。 8. 视觉冲击:选择视觉效果强烈的场景,或细节丰富的场景。 9. 节奏控制:建议可以帮助打破长篇文本或者帮助叙事节奏的场景。 10. 象征性元素:如果有含有重要象征意义的场景,请突出它们。 11. 动作序列:任何有重要动作的场景,如战斗或追逐。] 场景的文字描述要求: 按照以下格式提供您的建议: [章节/场景编号: 场景描述:(（场景描述应当可以在一帧画面中展示,避免复杂叙事；应当尽可能的从小说原文中抓取要点要素,丰富画面描述的各方面要素,充分展现小说的情景,特别是背景、人物位置、人物互动、人物情绪、人物动作、人物穿着、身体、性器官的描写。场景描述中应当根据画面情况合理选择视角,并且明确出来,(（(（如16mm焦距视角,35mm焦距视角,50mm焦距视角,85mm焦距视角,135mm焦距视角)(（如平视(（提高比例)、俯视、特写,)))]"},
            {"role": "user", "content": f"从下列文段中提取场景:\n\n{text}"}
        ],

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
def main(directory, api_key, output_dir):
    """主函数,逐个处理txt文件并调用API"""
    txt_files = get_txt_files(directory)
    if not txt_files:
        print(f"目录 {directory} 中未找到任何txt文件。")
        return

    for file_path in txt_files:
        print(f"正在处理: {file_path}...")
        try:
            text = read_txt_file(file_path)
            result = call_grok_api(text, api_key)
            save_output(output_dir, file_path, result)
        except Exception as e:
            print(f"处理 {file_path} 时出错: {e}")
            continue

# 命令行参数处理
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="将小说章节txt文件转化为分镜提示词")
    parser.add_argument("directory", help="包含txt文件的目录路径")
    parser.add_argument("api_key", help="xAI API密钥")
    parser.add_argument("output_dir", help="输出文件保存目录")
    args = parser.parse_args()

    main(args.directory, args.api_key, args.output_dir)