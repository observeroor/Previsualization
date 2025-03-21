import os
import subprocess

def main():
    # 设置子脚本的路径（可以自由修改）
    scripts_path = r"两步版本\代码文件\1txt清洗分割代码"

    # 提示用户输入指令
    user_input = input("请输入指令（格式：split name）：").strip()
    if not user_input.startswith("split "):
        print("输入格式错误，请使用格式：split name")
        return

    # 获取文件名
    _, name = user_input.split(" ", 1)
    name = name.strip()
    if not name:
        print("文件名不能为空！")
        return

    # 固定路径
    base_path = r"两步版本\过程文件"
    folder_path = os.path.join(base_path, name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"已创建文件夹：{folder_path}")
    else:
        print(f"文件夹已存在：{folder_path}")

    # 子脚本列表（按顺序执行）
    scripts = [
        "1st清洗.py",  # 清洗脚本
        "2rd分段.py",  # 分段脚本
        "3th间隔检测.py",
        "4th大文件分割.py"
    ]

    # 依次执行子脚本
    for script in scripts:
        script_path = os.path.join(scripts_path, script)
        if not os.path.exists(script_path):
            print(f"子脚本未找到：{script_path}")
            continue

        # 调用子脚本并传递参数
        try:
            subprocess.run(["python", script_path, name], check=True)
            print(f"成功执行子脚本：{script}")
        except subprocess.CalledProcessError as e:
            print(f"执行子脚本失败：{script}，错误：{e}")
            break

if __name__ == "__main__":
    main()