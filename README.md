# AI Message Generator for Git

[![PyPI version](https://badge.fury.io/py/aimsg.svg)](https://badge.fury.io/py/aimsg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

A CLI tool that generates commit messages using OpenAI based on your git repository changes. It analyzes the staged changes in your git repository and uses OpenAI's GPT model to generate meaningful and descriptive commit messages.

## Features

- 🤖 AI-powered commit message generation
- 🔄 Automatically analyzes git diff of staged changes
- 🌐 Supports custom OpenAI API base URL for users behind firewalls
- 🚀 Easy to use with simple command line interface
- 🌍 Global configuration that works across all repositories
- 📦 Available system-wide without virtual environment
- ✨ Generates conventional commit format messages

## Installation

1. Install the package globally:
```bash
# Install globally with pip (user install - recommended)
pip3 install --user . --break-system-packages

# Or if you want to install it system-wide (might need sudo)
sudo pip3 install . --break-system-packages
```

2. Add the user-level bin directory to your PATH:

For macOS/Linux with zsh (add to ~/.zshrc):
```bash
# Add this line to your ~/.zshrc
export PATH="$HOME/Library/Python/3.12/bin:$PATH"  # Adjust Python version as needed

# Then reload your shell configuration
source ~/.zshrc
```

For macOS/Linux with bash (add to ~/.bashrc or ~/.bash_profile):
```bash
# Add this line to your ~/.bashrc or ~/.bash_profile
export PATH="$HOME/Library/Python/3.12/bin:$PATH"  # Adjust Python version as needed

# Then reload your shell configuration
source ~/.bashrc  # or source ~/.bash_profile
```

## Configuration

Initialize the tool with your OpenAI API key:
```bash
aimsg init
```

This will prompt you to:
1. Enter your OpenAI API key
2. Choose whether to use a custom API base URL (proxy)
3. If yes, enter the custom API base URL

The configuration will be saved in your user's configuration directory:
- macOS: `~/Library/Application Support/aimsg/config.env`
- Linux: `~/.config/aimsg/config.env`

## Usage

Simply use the `aimsg` command in any git repository:

```bash
# Stage your changes first
git add .

# Generate commit message for staged changes
aimsg commit

# Show help
aimsg --help
```

## Example Output

```bash
$ git add .
$ aimsg commit

Generated commit message:
----------------------------------------
feat(cli): add OpenAI-powered commit message generation
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
