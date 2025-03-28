import os
import sys  
import json
import argparse
from openai import OpenAI

# 调用API的函数
def call_grok_api(text, api_key):
    """
    调用Grok beta模型API，将小说章节文本转化为分镜提示词。
    参数:
        text: 小说章节的文本内容
        api_key: xAI API密钥
        temperature: 模型温度（默认0.7）
        max_tokens: 最大令牌数（默认1024）
    返回:
        API响应内容（字符串）
    """
    client = OpenAI(base_url="https://api.x.ai/v1", api_key=api_key)
    
    response = client.chat.completions.create(
        model="grok-2-1212",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that converts novel chapters into storyboarding prompts，将每一幅场景转化为Flux提示词。/n在转化过程中，必须做到：1.提示词的细节满足要求。2.如果场景是连贯的，要保持角色服装特征的一致性（比如：第三场景和第四场景是连续的，那么人物的服装除了穿着状态外应当保持大体一致，同时对发生变化的地方要着重突出，如（毛衣已经被扯下露出粉嫩的乳头）/n提示词分细节描述和相机设置两个部分，细节描述又分为前景、中景、背景三个部分，其中前景是最重要的部分【描述篇幅占用大】，相机设置在前景中焦背景确定之后，根据中景背景描述的视角宽广程度进行选择确定。/n前景：关于人物的描述（/n人数与相对位置：描述画面中有几个男生，几个女生，分别是谁，分别处在什么位置/n服装：根据原文文段获取详细的服装信息，包括服装样式，衣物状态，然后根据场景进行完善补全，补全后包括但不限于下列要素【服装类型，材质，颜色，服装特殊设计，服装穿在身上的状态（例如：把全身紧紧包裹凸显出身材\宽松的露出一些乳沟\脱下一半\……），服装状态（\撕裂\完整\湿透…………）】/n人物外貌：对女性角色，要/n姿态和互动：描述人物当前的身体姿态（包括人物相互的位置关系，脸朝向，身体朝向，腿部姿势，手臂姿势，两个人物接触的地方的身体描写（如手紧紧揉着屁股））/n神态：（害羞、嗔怒、阿黑颜、红润、调皮，注意：可以使用凸显性张力、在快感中堕落等的描写，但不要使用惊悚、血腥的描写）/n性特征描写：女性：胸部特征、屁股、阴部的形状、状态描写（大小、形状、是否裸露、湿润\红肿\滴下精液\……））/n中景：人物周围其他物体、环境的描述/n背景：关于人物所处地点的描述，要根据文段内容带有场景的氛围描述和情绪/n相机设置（主要包括镜头焦距 如16mm超广角、24广角、50中焦、85长焦，光圈大小 如f/1.8光圈、f8光圈，要根据场景是狭窄、还是宽广进行合适的选择）"},
            {"role": "user", "content": f"Convert the following novel chapter into storyboarding prompts in JSON format:\n\n{text}"}
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
    print(f"完成处理: {original_file}，结果已保存至 {output_file}")

# 主函数
def main(directory, api_key, output_dir):
    """主函数，逐个处理txt文件并调用API"""
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