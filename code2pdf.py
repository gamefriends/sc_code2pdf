# Usage: python code2pdf.py -i /xx/path/code [-o /path/doc_path]
# Description: 将代码目录生成PDF文件，每页50行代码，支持中文

import os
import subprocess
import sys
import time


# 检查依赖是否已安装
def is_installed(pip_executable, package):
    try:
        subprocess.check_call(
            [pip_executable, "show", package],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
    except subprocess.CalledProcessError:
        return False


# 安装依赖
def install_requirements():
    venv_path = os.path.join(os.path.dirname(__file__), "venv")
    if not os.path.exists(venv_path):
        subprocess.check_call([sys.executable, "-m", "venv", venv_path])
    pip_executable = os.path.join(venv_path, "bin", "pip")
    requirements_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
    if os.path.isfile(requirements_path):
        with open(requirements_path, "r") as f:
            packages = f.read().splitlines()
            for package in packages:
                if not is_installed(pip_executable, package):
                    print(f"-> 安装依赖: {package}")
                    subprocess.check_call(
                        [pip_executable, "install", package],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
    else:
        print("-> 未找到requirements.txt文件，无法检查、安装依赖。")
        exit(1)


install_requirements()

# 修改sys.path以包含虚拟环境的site-packages目录
venv_site_packages = os.path.join(
    os.path.dirname(__file__),
    "venv",
    "lib",
    f"python{sys.version_info.major}.{sys.version_info.minor}",
    "site-packages",
)
sys.path.insert(0, venv_site_packages)

try:
    import argparse

    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfgen import canvas

    # 解析命令行参数
    parser = argparse.ArgumentParser(
        description="将代码目录生成PDF文件，每页50行代码，支持中文"
    )
    parser.add_argument("-i", "--input", required=True, help="源代码目录路径")
    parser.add_argument("-o", "--output", help="保存PDF文件的路径")
    args = parser.parse_args()

    source_directory = args.input
    if not os.path.isdir(source_directory):
        print(f"-> 输入的源代码目录路径无效: {source_directory}")
        sys.exit(1)

    code_name = os.path.basename(source_directory)
    output_path = (
        args.output if args.output else f"{code_name}_{time.strftime('%Y%m%d')}.pdf"
    )

    font_path = os.path.join(os.path.dirname(__file__), "fonts", "SimSun.ttf")
    if not os.path.exists(font_path):
        print(f"-> 未找到中文字体文件: {font_path}")
        sys.exit(1)

    # 设置支持中文的系统字体
    pdfmetrics.registerFont(TTFont("SimSun", font_path))

    # 创建PDF对象
    c = canvas.Canvas(output_path)

    # 读取所有代码文件
    all_lines = []
    for root, _, files in os.walk(source_directory):
        for file in files:
            if file.endswith(
                (
                    ".java",
                    ".py",
                    ".ts",
                    ".js",
                    ".html",
                    ".css",
                    ".xml",
                    ".sql",
                    ".sh",
                    ".properties",
                    ".yml",
                    ".yaml",
                    ".json",
                )
            ):
                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    lines = [line for line in lines if line.strip() != ""]
                    all_lines.extend(lines)

    # 每页50行
    lines_per_page = 50
    total_pages = (len(all_lines) + lines_per_page - 1) // lines_per_page

    print(f"-> 总共有{len(all_lines)}行代码，共{total_pages}页。")

    # 处理超过60页的情况
    if total_pages > 60:
        all_lines = all_lines[: 30 * lines_per_page] + all_lines[-30 * lines_per_page :]

    # 添加内容到PDF
    c.setFont("SimSun", 10)
    for i in range(0, len(all_lines), lines_per_page):
        if i != 0:
            c.showPage()
            c.setFont("SimSun", 10)
        for j, line in enumerate(all_lines[i : i + lines_per_page]):
            c.drawString(10, 800 - 15 * j, line)

    # 保存PDF
    c.save()

    # 实际生成的页数
    actual_pages = (len(all_lines) + lines_per_page - 1) // lines_per_page
    print(f"-> 实际生成{actual_pages}页。")

    print("-> PDF[" + code_name + "]生成成功！")

finally:
    # 移除虚拟环境的site-packages目录
    if venv_site_packages in sys.path:
        sys.path.remove(venv_site_packages)
