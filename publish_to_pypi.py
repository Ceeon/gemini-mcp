#!/usr/bin/env python3
"""
发布 gemini-mcp 到 PyPI

使用方法：
1. 首先获取PyPI token: https://pypi.org/manage/account/token/
2. 运行: python publish_to_pypi.py
3. 输入token（或设置环境变量 PYPI_TOKEN）
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def clean_build():
    """清理构建文件"""
    print("🧹 清理旧的构建文件...")
    dirs_to_clean = ['dist', 'build', '*.egg-info', 'gemini_mcp.egg-info']
    for dir_pattern in dirs_to_clean:
        for path in Path('.').glob(dir_pattern):
            if path.is_dir():
                shutil.rmtree(path)
                print(f"  删除 {path}")

def build_package():
    """构建包"""
    print("\n📦 构建包...")
    result = subprocess.run(
        [sys.executable, "-m", "build"],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"❌ 构建失败: {result.stderr}")
        return False
    
    print("✅ 构建成功！")
    
    # 列出构建的文件
    dist_files = list(Path('dist').glob('*'))
    print("\n📋 构建的文件：")
    for file in dist_files:
        print(f"  - {file.name}")
    
    return True

def upload_to_pypi(use_test=False):
    """上传到PyPI"""
    # 获取token
    token = os.environ.get('PYPI_TOKEN')
    if not token:
        print("\n🔑 请输入PyPI Token")
        print("  (可以在 https://pypi.org/manage/account/token/ 创建)")
        token = input("Token: ").strip()
    
    if not token or token == "pypi-你的token这里":
        print("❌ 需要有效的PyPI token")
        return False
    
    # 设置上传目标
    if use_test:
        print("\n📤 上传到 TestPyPI...")
        repo_url = ["--repository-url", "https://test.pypi.org/legacy/"]
    else:
        print("\n📤 上传到 PyPI...")
        repo_url = []
    
    # 构建twine命令
    cmd = [
        sys.executable, "-m", "twine", "upload",
        *repo_url,
        "--username", "__token__",
        "--password", token,
        "dist/*"
    ]
    
    # 执行上传
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ 上传失败: {result.stderr}")
        return False
    
    print("✅ 上传成功！")
    
    if use_test:
        print("\n测试安装命令：")
        print("  pip install -i https://test.pypi.org/simple/ gemini-mcp")
    else:
        print("\n安装命令：")
        print("  pip install gemini-mcp")
        print("\n或使用uvx：")
        print("  uvx gemini-mcp")
    
    return True

def check_version():
    """检查版本号"""
    pyproject = Path('pyproject.toml')
    if not pyproject.exists():
        print("❌ 找不到 pyproject.toml")
        return None
    
    content = pyproject.read_text()
    for line in content.split('\n'):
        if 'version' in line and '=' in line:
            version = line.split('=')[1].strip().strip('"')
            return version
    
    return None

def main():
    print("🚀 Gemini MCP 发布工具")
    print("="*50)
    
    # 检查版本
    version = check_version()
    if version:
        print(f"📌 当前版本: {version}")
    else:
        print("❌ 无法读取版本号")
        return 1
    
    # 确认发布
    print(f"\n准备发布版本 {version} 到 PyPI")
    confirm = input("确认继续? (y/n): ").strip().lower()
    if confirm != 'y':
        print("取消发布")
        return 0
    
    # 清理旧文件
    clean_build()
    
    # 构建
    if not build_package():
        return 1
    
    # 询问是否先发布到测试服务器
    use_test = input("\n是否先发布到TestPyPI测试? (y/n): ").strip().lower() == 'y'
    
    # 上传
    if not upload_to_pypi(use_test):
        return 1
    
    if use_test:
        # 如果是测试，询问是否继续发布到正式服务器
        confirm_prod = input("\n测试成功，是否发布到正式PyPI? (y/n): ").strip().lower()
        if confirm_prod == 'y':
            if not upload_to_pypi(use_test=False):
                return 1
    
    print("\n🎉 发布完成！")
    print("\n更新本地安装：")
    print("  pip install --upgrade gemini-mcp")
    print("\n更新uvx缓存：")
    print("  uvx --refresh gemini-mcp")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())