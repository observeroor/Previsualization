import os
import json

def merge_json_files(folder1, folder2, output_folder):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 获取两个文件夹中所有的json文件
    files1 = [f for f in os.listdir(folder1) if f.endswith('.json')]
    files2 = [f for f in os.listdir(folder2) if f.endswith('.json')]

    # 找出两边都有相同的文件
    common_files = set(files1) & set(files2)

    for file in common_files:
        file_path1 = os.path.join(folder1, file)
        file_path2 = os.path.join(folder2, file)
        output_path = os.path.join(output_folder, file)

        # 读取JSON文件
        with open(file_path1, 'r', encoding='utf-8') as f1:
            json1 = json.load(f1)
        with open(file_path2, 'r', encoding='utf-8') as f2:
            json2 = json.load(f2)

        # 合并JSON内容
        merged_json = json1  # 以第一个文件为基础
        for key in json2.keys():
            if key in merged_json:
                # 如果键存在于两个文件中，则合并
                merged_json[key].update(json2[key])
            else:
                # 如果键只在第二个文件中存在，则直接添加
                merged_json[key] = json2[key]

        # 写入合并后的JSON文件
        with open(output_path, 'w', encoding='utf-8') as out_file:
            json.dump(merged_json, out_file, ensure_ascii=False, indent=4)
    
# 定义路径
folder1 = os.path.join("两步版本", "过程文件", "nygs", "6th提示词", "1.1中景")
folder2 = os.path.join("两步版本", "过程文件", "nygs", "5th分镜")
output_folder = os.path.join("两步版本", "过程文件", "nygs", "6th提示词", "1.5中景转化")

# 执行合并
merge_json_files(folder1, folder2, output_folder)
