# langchain-test

一个基于 LangChain + FastAPI 的 AI 对话应用，支持文字聊天和文件上传（PDF、Word、TXT、Markdown）。

## 功能

- 💬 实时 AI 对话（带记忆，多轮对话上下文保持）
- 📎 文件上传分析（支持 .txt、.pdf、.docx、.md）
- 🌐 前端页面 + 后端 API 一体化部署

## 技术栈

- **后端**: FastAPI + LangChain + LangGraph
- **前端**: 原生 HTML/CSS/JavaScript
- **AI 模型**: DeepSeek

## 快速开始

1. 克隆仓库

```bash
git clone https://github.com/YCBRMSN-maker/langchain-test.git
cd langchain-test
```

2. 安装依赖（需要 [uv](https://github.com/astral-sh/uv)）

```bash
uv sync
```

3. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env，填入你的 API 密钥
```

4. 启动服务

```bash
python main.py
```

5. 打开浏览器访问 http://127.0.0.1:8000

## 项目结构

```
langchain-test/
├── main.py          # 后端：FastAPI 应用 + LangChain Agent
├── index.html       # 前端：聊天界面
├── pyproject.toml   # 项目依赖配置
├── uv.lock          # 依赖锁定文件
├── .env.example     # 环境变量模板
└── .gitignore       # Git 忽略规则
```

## License

MIT
