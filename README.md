# Gemini MCP

基于 Gemini 2.5 Flash 的图片处理 MCP 服务器，支持与 Claude Desktop、Cursor 等 MCP 客户端集成。

## 快速开始

### 使用 uvx 运行（推荐）

```bash
# 无需安装，直接运行
GEMINI_API_KEY=your-api-key uvx gemini-mcp
```

### 通过 pip 安装

```bash
pip install gemini-mcp
GEMINI_API_KEY=your-api-key gemini-mcp
```

## 配置客户端

### Claude Desktop

编辑 `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "gemini": {
      "command": "uvx",
      "args": ["gemini-mcp"],
      "env": {
        "GEMINI_API_KEY": "your-api-key"
      }
    }
  }
}
```

### Cursor

编辑 `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "gemini": {
      "command": "uvx",
      "args": ["gemini-mcp"],
      "env": {
        "GEMINI_API_KEY": "your-api-key"
      }
    }
  }
}
```

## 功能

- 🖼️ 支持本地文件、URL 和 Base64 图片
- 🚀 使用 uvx 无需安装即可运行
- 🔄 流式响应处理
- 📦 自动保存生成的图片
- 🌐 支持 SOCKS5 代理

## 使用示例

在 Claude Desktop 中：

```
分析这张图片：/path/to/image.jpg
描述 https://example.com/image.png 的内容
```

## 环境变量

- `GEMINI_API_KEY`: Gemini API 密钥（必需）
- `OUTPUT_DIR`: 输出目录（默认：`./outputs`）
- `ALL_PROXY`: SOCKS5 代理（如：`socks5://127.0.0.1:1080`）

## 命令行参数

```bash
gemini-mcp --help              # 查看帮助
gemini-mcp --mode http         # HTTP 模式
gemini-mcp --debug             # 调试模式
```

## 许可证

MIT