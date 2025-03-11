# Git Commit Message Generator with AI

[中文文档](./README_CN.md)

[![PyPI version](https://badge.fury.io/py/aimsg.svg)](https://badge.fury.io/py/aimsg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

A CLI tool that generates commit messages using AI models based on your git repository changes.

## Features

- 🤖 Wide Model Support: 
  - OpenAI
  - Anthropic
  - Google
  - DeepSeek
  - Aliyun
  - iFlytek
  - Zhipu
  - Baidu
  - Moonshot
  - Tencent
  - ByteDance
  - Replicate
  - Together AI
- 🔧 Custom API base
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

# Upgrade aimsg
pipx upgrade aimsg
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

2. Environment variables（Secondary priority）

```bash
export AIMSG_API_KEY=your_api_key
export AIMSG_API_BASE=your_api_base
export AIMSG_MODEL=your_model
export AIMSG_PROMPT=your_prompt
```

3. Global configuration via `aimsg init` (lowest priority, default)

```bash
aimsg init

# Creates ~/.config/aimsg/config.json with default settings:
# - model: your_model
# - api_base: your_api_base
# - api_key: your_api_key
# - prompt: default prompt template
# - custom_models: custom model list
```

## Model Management

```bash
# List available models
aimsg model list

# Add custom model
aimsg model add my-model https://api.example.com/v1

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

Default prompt template:

```
Based on the following git diff, generate a concise and descriptive commit message that follows conventional commits format.
Focus on the "what" and "why" of the changes.
Start with a type (feat, fix, docs, style, refactor, perf, test, build, ci, chore).
Do not include scope.
Limit the first line to 72 characters.
Add a blank line followed by a more detailed description if necessary.
```

The default prompt template guides the AI to:

- Follow conventional commits format
- Focus on the "what" and "why" of changes
- Keep the first line under 72 characters
- Add detailed description when necessary

## Default API Providers

- OpenAI: `https://api.openai.com/v1`
- Anthropic: `https://api.anthropic.com/v1`
- Google: `https://generativelanguage.googleapis.com/v1`
- DeepSeek: `https://api.deepseek.com/v1`
- Aliyun: `https://dashscope.aliyuncs.com/api/v1`
- iFlytek: `https://spark-api.xf-yun.com/v3.1`
- Zhipu: `https://open.bigmodel.cn/api/v1`
- Baidu: `https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop`
- Moonshot: `https://api.moonshot.cn/v1`
- Tencent: `https://hunyuan.cloud.tencent.com/hyllm/v1`
- ByteDance: `https://api.doubao.com/v1`
- Replicate: `https://api.replicate.com/v1`
- Together AI: `https://api.together.xyz/v1`

## License

MIT
