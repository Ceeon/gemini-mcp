# 发布到 PyPI 指南

## 步骤 1: 注册 PyPI 账号

1. 访问 https://pypi.org/account/register/
2. 创建账号并验证邮箱

## 步骤 2: 获取 API Token

1. 登录 PyPI 后访问: https://pypi.org/manage/account/token/
2. 创建新的 API token:
   - Token name: gemini-mcp
   - Scope: Entire account (首次发布) 或 Project: gemini-mcp (后续更新)
3. 复制 token (以 `pypi-` 开头的长字符串)

## 步骤 3: 配置认证

### 方法 A: 使用环境变量（推荐）

```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-YOUR_TOKEN_HERE
```

### 方法 B: 使用 .pypirc 文件

创建 `~/.pypirc` 文件：

```ini
[pypi]
username = __token__
password = pypi-YOUR_TOKEN_HERE
```

设置权限：
```bash
chmod 600 ~/.pypirc
```

## 步骤 4: 发布包

### 首次发布到 TestPyPI（可选，用于测试）

```bash
# 发布到测试服务器
python -m twine upload -r testpypi dist/*

# 测试安装
pip install -i https://test.pypi.org/simple/ gemini-mcp
```

### 正式发布到 PyPI

```bash
# 使用环境变量方式
TWINE_USERNAME=__token__ TWINE_PASSWORD=pypi-YOUR_TOKEN python -m twine upload dist/*

# 或者如果配置了 .pypirc
python -m twine upload dist/*
```

## 步骤 5: 验证发布

1. 访问: https://pypi.org/project/gemini-mcp/
2. 测试安装:
   ```bash
   pip install gemini-mcp
   # 或使用 uvx
   uvx gemini-mcp --help
   ```

## 更新版本

1. 修改 `pyproject.toml` 中的 `version`
2. 重新构建:
   ```bash
   rm -rf dist/
   python -m build
   ```
3. 上传新版本:
   ```bash
   python -m twine upload dist/*
   ```

## 常见问题

### 包名已存在

如果 `gemini-mcp` 已被占用，需要在 `pyproject.toml` 中修改包名，例如：
- `gemini-mcp-server`
- `gemini-image-mcp`
- `gemini-flash-mcp`

### 上传失败

检查：
1. Token 是否正确
2. 网络连接是否正常
3. 包名是否可用

## 自动化发布（GitHub Actions）

可以配置 GitHub Actions 自动发布：

`.github/workflows/publish.yml`:
```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    - name: Build and publish
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: |
        pip install build twine
        python -m build
        python -m twine upload dist/*
```

需要在 GitHub 仓库的 Settings > Secrets 中添加 `PYPI_API_TOKEN`。