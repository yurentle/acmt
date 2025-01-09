# AI Message Generator for Git

[![PyPI version](https://badge.fury.io/py/aimsg.svg)](https://badge.fury.io/py/aimsg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

A CLI tool that generates commit messages using AI models based on your git repository changes. It analyzes the staged changes in your git repository and uses AI models to generate meaningful and descriptive commit messages.

## Features

- 🤖 Supports multiple AI models:
  - DeepSeek Chat
  - OpenAI GPT-3.5 Turbo
  - OpenAI GPT-4
  - Anthropic Claude-2
  - Google PaLM 2
  - Alibaba Qwen
  - iFlytek Spark
  - Baichuan
  - Zhipu ChatGLM
  - Baidu ERNIE
  - Moonshot AI KIMI
  - Tencent Hunyuan
  - ByteDance Doubao
  - Third-party Hosted Models:
    - Llama 2 (by Replicate)
    - Mistral (by Together AI)
    - Mixtral (by Together AI)
    - CodeLlama (by Replicate)
- 🔧 Supports custom models and API endpoints
- 📝 Follows conventional commits format
- 🔄 Handles dependency updates gracefully
- 🎯 Customizable prompt templates
- 🔑 Secure API key storage
- 🌐 Smart API endpoint management
- 📝 Clear and concise commit messages

## Installation

```bash
pip install aimsg
```

## Setup

Initialize the tool with your API key and preferred model:

```bash
aimsg init
```

This will guide you through:
1. Selecting an AI model
2. Entering your API key
3. Configuring the API endpoint (if needed)

Each model has its default API endpoint:

### OpenAI Models
- OpenAI GPT Models: `https://api.openai.com/v1`

### Anthropic Models
- Claude Models: `https://api.anthropic.com/v1`

### Google Models
- PaLM & Gemini: `https://generativelanguage.googleapis.com/v1`

### Chinese Models
- DeepSeek: `https://api.deepseek.com/v1`
- Aliyun Qwen: `https://dashscope.aliyuncs.com/api/v1`
- iFlytek Spark: `https://spark-api.xf-yun.com/v3.1`
- Zhipu GLM: `https://open.bigmodel.cn/api/v1`
- Baidu ERNIE: `https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop`
- Moonshot KIMI: `https://api.moonshot.cn/v1`
- Tencent Hunyuan: `https://hunyuan.cloud.tencent.com/hyllm/v1`
- ByteDance Doubao: `https://api.doubao.com/v1`

### Third-party Hosted Models
- Replicate: `https://api.replicate.com/v1`
- Together AI: `https://api.together.xyz/v1`

You can customize these endpoints during initialization or by using environment variables.

## Usage

1. Stage your changes:
```bash
git add .
```

2. Generate commit message:
```bash
# Using default model (GPT-3.5)
aimsg commit

# Using a specific model
aimsg commit --model gpt4
aimsg commit --model claude2
aimsg commit --model qwen-turbo

# Using custom API base URL
aimsg commit --api-base https://your-api-endpoint.com/v1

# List all available models
aimsg model list
```

## Model Management

1. List all available models:
```bash
aimsg model list
```

2. Add a custom model:
```bash
aimsg model add my-model model-id https://api.example.com/v1
```

3. Remove a custom model:
```bash
aimsg model remove my-model
```

### Examples of Custom Model Configuration

1. Self-hosted Llama 2:
```bash
aimsg model add my-llama llama-2-70b-chat http://localhost:8000/v1
aimsg init  # Then select my-llama from the list
```

2. Alternative OpenAI endpoint:
```bash
aimsg model add azure-gpt gpt-35-turbo https://your-azure-endpoint.com/v1
aimsg init  # Then select azure-gpt from the list
```

3. Other provider's model:
```bash
aimsg model add claude-3 claude-3 https://api.anthropic.com/v1
aimsg init  # Then select claude-3 from the list
```

## Supported Models

Here are all the pre-configured models you can use:

### OpenAI Models
- `gpt-3.5-turbo`
- `gpt-3.5-turbo-16k`
- `gpt-4`
- `gpt-4-32k`
- `gpt-4-1106-preview`

### Anthropic Models
- `claude-2`
- `claude-instant-1`

### Google Models
- `palm-2`
- `gemini-pro`

### Chinese Models
- Aliyun
  - `qwen-turbo`
  - `qwen-plus`
- iFlytek
  - `spark-v3`
  - `spark-v2`
- Zhipu
  - `chatglm-4`
  - `chatglm-turbo`
- Baidu
  - `ernie-4.0`
  - `ernie-turbo`
- Moonshot
  - `kimi-v1`
- Tencent
  - `hunyuan`
  - `hunyuan-lite`
- ByteDance
  - `doubao-v1`
  - `doubao-turbo`

### Open Source Models (Hosted)
- DeepSeek
  - `deepseek-chat`
- Replicate (提供托管服务)
  - `meta-llama/llama-2-70b-chat`
  - `meta-llama/codellama-34b-instruct`
- Together AI (提供托管服务)
  - `mistralai/mistral-7b-instruct`
  - `mistralai/mixtral-8x7b-instruct`

## Environment Variables

The following environment variables can be used to configure the tool:

- `AIMSG_API_KEY`: Your API key for the AI service
- `AIMSG_API_BASE`: Base URL for the API service (optional)

You can set these in your shell:

```bash
export AIMSG_API_KEY=your-api-key
export AIMSG_API_BASE=https://api.example.com/v1
```

Or use a `.env` file in your project:

```env
AIMSG_API_KEY=your-api-key
AIMSG_API_BASE=https://api.example.com/v1
```

## License

MIT
