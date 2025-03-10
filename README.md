# AI Message Generator for Git

[中文文档](./README_CN.md)

[![PyPI version](https://badge.fury.io/py/aimsg.svg)](https://badge.fury.io/py/aimsg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

A CLI tool that generates commit messages using AI models based on your git repository changes.

## Features

- 🤖 Wide Model Support: OpenAI, Anthropic, Google, Chinese models, and more
- 🔧 Custom Model Integration
- 📝 Conventional Commits Format
- 🎯 Customizable Prompt Templates
- 🔑 Secure Configuration Management

## Installation

### Using pipx (Recommended)

```bash
# Install pipx if you haven't
brew install pipx
pipx ensurepath

# Install aimsg
pipx install aimsg
```

### Using pip

```bash
pip install aimsg
```

## Quick Start

1. Initialize with your preferred model and API key:

```bash
aimsg init
```

2. Stage your changes and generate commit message:

```bash
git add .
aimsg commit
```

3. Get help or version information:

```bash
# Show version
aimsg --version

# Show all available commands
aimsg --help

# Show help for a specific command
aimsg model --help
aimsg commit --help

# Show current configuration
aimsg current
```

## Configuration

Configure `aimsg` in order of priority:

1. Project-level `.env` file (highest priority)

```bash
AIMSG_API_KEY=your_api_key
AIMSG_API_BASE=your_api_base
AIMSG_MODEL=your_model
AIMSG_PROMPT=your_prompt
```

2. Environment variables

```bash
export AIMSG_API_KEY=your_api_key
export AIMSG_API_BASE=your_api_base
export AIMSG_MODEL=your_model
export AIMSG_PROMPT=your_prompt
```

3. Global configuration via `aimsg init` (lowest priority, default)

```bash
# Creates ~/.config/aimsg/config.json with default settings:
# - model: gpt-3.5-turbo
# - api_base: https://api.openai.com/v1
# - api_key: your_api_key
# - prompt: default prompt template
# - custom_models: custom model list
aimsg init
```

## Model Management

```bash
# List available models
aimsg model list

# Add custom model
aimsg model add my-model model-id https://api.example.com/v1

# Remove custom model
aimsg model remove my-model
```

## Prompt Management

```bash
# Customize commit message prompt template
aimsg prompt

# Reset to default prompt template
aimsg reset-prompt
```

The default prompt template guides the AI to:

- Follow conventional commits format
- Focus on the "what" and "why" of changes
- Keep the first line under 72 characters
- Add detailed description when necessary

## Default API Endpoints

### Major Providers

- OpenAI: `https://api.openai.com/v1`
- Anthropic: `https://api.anthropic.com/v1`
- Google: `https://generativelanguage.googleapis.com/v1`

### Chinese Providers

- DeepSeek: `https://api.deepseek.com/v1`
- Aliyun: `https://dashscope.aliyuncs.com/api/v1`
- iFlytek: `https://spark-api.xf-yun.com/v3.1`
- Zhipu: `https://open.bigmodel.cn/api/v1`
- Baidu: `https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop`
- Moonshot: `https://api.moonshot.cn/v1`
- Tencent: `https://hunyuan.cloud.tencent.com/hyllm/v1`
- ByteDance: `https://api.doubao.com/v1`

### Hosted Services

- Replicate: `https://api.replicate.com/v1`
- Together AI: `https://api.together.xyz/v1`

## License

MIT
