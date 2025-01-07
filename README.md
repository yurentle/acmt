# AI Message Generator for Git

[![PyPI version](https://badge.fury.io/py/aimsg.svg)](https://badge.fury.io/py/aimsg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

A CLI tool that generates commit messages using AI models based on your git repository changes. It analyzes the staged changes in your git repository and uses AI models to generate meaningful and descriptive commit messages.

## Features

- 🤖 Supports multiple AI models:
  - OpenAI GPT-3.5 Turbo
  - DeepSeek Chat
  - OpenAI GPT-4
  - Anthropic Claude-2
  - Google PaLM 2
  - Chinese Models:
    - Alibaba Qwen
    - iFlytek Spark
    - Baichuan
    - Zhipu ChatGLM
    - Baidu ERNIE
    - Moonshot AI KIMI
    - Tencent Hunyuan
    - ByteDance Doubao
  - Open Source Models (via hosted services):
    - Llama 2
    - Mistral
    - Mixtral
    - CodeLlama
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
- GPT-3.5 Turbo: `https://api.openai.com/v1`
- DeepSeek Chat: `https://api.deepseek.com`
- GPT-4: `https://api.openai.com/v1`
- Claude-2: `https://api.anthropic.com/v1`
- PaLM 2: `https://api.google.com/v1`

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

2. Select model interactively:
```bash
aimsg model select
```

3. Set default model directly:
```bash
# Use GPT-4 as default
aimsg model use gpt4

# Use Claude 2 as default
aimsg model use claude2

# Use custom model as default
aimsg model use my-model
```

4. Add a custom model:
```bash
aimsg model add my-model model-id https://api.example.com/v1
```

5. Remove a custom model:
```bash
aimsg model remove my-model
```

### Examples of Custom Model Configuration

1. Self-hosted Llama 2:
```bash
aimsg model add my-llama llama-2-70b-chat http://localhost:8000/v1
aimsg model use my-llama  # Set as default
```

2. Alternative OpenAI endpoint:
```bash
aimsg model add azure-gpt gpt-35-turbo https://your-azure-endpoint.com/v1
aimsg model use azure-gpt  # Set as default
```

3. Other provider's model:
```bash
aimsg model add claude-3 claude-3 https://api.anthropic.com/v1
aimsg model use claude-3  # Set as default
```

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key
- `OPENAI_API_BASE`: Custom API base URL (optional)

## Custom Models

You can add and manage custom models:

1. Add a custom model:
```bash
aimsg model add my-model model-id https://api.example.com/v1
```

2. Remove a custom model:
```bash
aimsg model remove my-model
```

3. Use a custom model:
```bash
aimsg commit --model my-model
```

## Supported Models

Here are some of the pre-configured models you can use:

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
- Alibaba Qwen: `qwen-turbo`, `qwen-plus`
- iFlytek Spark: `spark-v3`, `spark-v2`
- Baichuan: `baichuan-53b`
- Zhipu GLM: `chatglm-4`, `chatglm-turbo`
- Baidu ERNIE: `ernie-4.0`, `ernie-turbo`
- Moonshot KIMI: `kimi-v1`
- Tencent Hunyuan: `hunyuan`, `hunyuan-lite`
- ByteDance Doubao: `doubao-v1`, `doubao-turbo`

### Open Source Models (Hosted)
- `deepseek-chat`
- `llama-2-70b-chat` (via Replicate)
- `mistral-7b-instruct` (via Together AI)
- `mixtral-8x7b-instruct` (via Together AI)
- `codellama-34b-instruct` (via Replicate)

## Development

See [Development Guide](lib/dev.md) for instructions on setting up the development environment.

## License

MIT
