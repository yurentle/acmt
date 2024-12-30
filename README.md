# AI Message Generator for Git

[![PyPI version](https://badge.fury.io/py/aimsg.svg)](https://badge.fury.io/py/aimsg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

A CLI tool that generates commit messages using AI models based on your git repository changes. It analyzes the staged changes in your git repository and uses AI models to generate meaningful and descriptive commit messages.

## Features

- 🤖 Supports multiple AI models:
  - OpenAI GPT-3.5 Turbo
  - DeepSeek Chat
- 🎯 Follows conventional commits format
- 🛠️ Customizable prompt templates
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

## Usage

Simply use the `aimsg` command in any git repository:

```bash
# Stage your changes first
git add .

# Generate commit message for staged changes
aimsg commit

# Show help
aimsg --help

# Configure custom prompt template
aimsg prompt

# Reset prompt template to default
aimsg reset_prompt

# Change the AI model or API endpoint
aimsg model
```

### Model Selection

You can choose or change the AI model:

```bash
$ aimsg model
```

The tool will show you:
- Available models with their default API endpoints
- Your current configuration
- Option to modify the API endpoint (when applicable)

Some models (like DeepSeek) require using their specific API endpoints, which will be automatically configured for you.

### Custom Prompt Template

You can customize the prompt template used for generating commit messages:

```bash
$ aimsg prompt
```

This will show the current prompt template and allow you to modify it. The template can use the following variables:
- `{diff}`: The git diff content

Example custom prompt template:
```
Based on this git diff, write a commit message:
{diff}

The commit message should:
1. Start with a type (feat/fix/docs/style/refactor/test/chore)
2. Include a scope in parentheses
3. Have a brief description
4. Be no longer than 72 characters
```

To reset the prompt template to default:
```bash
$ aimsg reset_prompt
```

## Example Output

```bash
$ git add .
$ aimsg commit

Generated commit message:
----------------------------------------
feat(cli): add AI-powered commit message generation
----------------------------------------

Do you want to commit with this message? [y/N]: y
Changes committed successfully!
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Troubleshooting

If you get "command not found: aimsg" after installation:
1. Make sure you've added the user-level bin directory to your PATH as shown in the installation section
2. Check if the aimsg command exists in the bin directory:
```bash
ls ~/Library/Python/3.12/bin/aimsg  # Adjust Python version as needed
```
3. If the command exists but still isn't found, try restarting your terminal
