import os
import subprocess
import sys

def main():
    # 子脚本路径（请根据实际路径修改）
    script_path = os.path.join("两步版本", "代码文件", "2", "grok1212场景提取.py")

    # 定义参数
    param1 = os.path.join("两步版本", "过程文件", "nygs", "4th大文件分割")
    param2 = "xai-JtSPb3Wz6e9FJ1J5pDh3OoMeOvK7aGntYVPF4MlD7YXeTUDgmCg9WP6Y5fPqK00LMsJzbuamd7R2jVWI"
    param3 = os.path.join("两步版本", "过程文件", "nygs", "output")
    """
    param1 directory
    param2 api_key
    param3 output_dir
    param4 temperature
    """

    # 转换为绝对路径
    script_path = os.path.abspath(script_path)
    param1 = os.path.abspath(param1)
    param3 = os.path.abspath(param3)

    # 检查子脚本是否存在
    if not os.path.exists(script_path):
        print(f"子脚本未找到：{script_path}")
        return

    # 打印调试信息
    print(f"使用的Python解释器：{sys.executable}")
    print(f"子脚本路径：{script_path}")
    print(f"参数1：{param1}")
    print(f"参数2：{param2}")
    print(f"参数3：{param3}")

    # 构造命令
    command = [sys.executable, script_path, param1, param2, param3]

    # 调用子脚本
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        print("子脚本执行成功！")
        print("子脚本输出：")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("子脚本执行失败！")
        print(f"错误信息：{e.stderr}")
    except FileNotFoundError as e:
        print("无法找到Python解释器或子脚本！")
        print(f"错误信息：{e}")

if __name__ == "__main__":
    main()
