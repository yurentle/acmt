import os
import subprocess
from typing import Optional, Tuple, List

DEPENDENCY_FILES = [
    'pnpm-lock.yaml',      # pnpm
    'package-lock.json',   # npm
    'yarn.lock',          # yarn
    'bun.lockb',          # bun
    'requirements.txt',    # Python
    'poetry.lock',        # Python Poetry
    'Pipfile.lock',       # Python Pipenv
    'pom.xml',           # Maven
    'build.gradle',      # Gradle
    'build.gradle.kts',  # Gradle Kotlin
    'gradle.lockfile',   # Gradle
    'composer.lock',     # PHP
    'Gemfile.lock',      # Ruby
    'cargo.lock',        # Rust
    'go.sum',           # Go
]

MAX_DIFF_LENGTH = 5000  # 设置一个合理的阈值，超过这个长度就认为是大规模依赖更新

def run_git_command(command: list[str]) -> Tuple[int, str, str]:
    """运行 git 命令"""
    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate()
        return process.returncode, stdout, stderr
    except Exception as e:
        return 1, "", str(e)

def get_staged_diff() -> tuple[Optional[str], Optional[List[str]]]:
    """Get the diff of staged changes and dependency files.
    
    Returns:
        A tuple of (diff_content, dependency_files), where:
        - diff_content: The diff content of non-dependency files, or None if no changes
        - dependency_files: List of dependency files changed, or None if no dependency updates
    """
    try:
        # 获取所有暂存的文件列表
        staged_files = subprocess.check_output(['git', 'diff', '--cached', '--name-only']).decode().strip().split('\n')
        if not staged_files or staged_files == ['']:
            return None, None

        # 分离依赖文件和非依赖文件
        dep_files = [f for f in staged_files if any(f.endswith(dep) for dep in DEPENDENCY_FILES)]
        non_dep_files = [f for f in staged_files if not any(f.endswith(dep) for dep in DEPENDENCY_FILES)]

        # 获取非依赖文件的 diff
        diff = None
        if non_dep_files:
            diff = subprocess.check_output(['git', 'diff', '--cached'] + non_dep_files).decode()

        return diff, dep_files if dep_files else None
    except subprocess.CalledProcessError:
        return None, None

def commit_with_message(message: str) -> bool:
    """使用指定的消息提交更改"""
    try:
        # 使用 -m 参数并正确转义消息
        returncode, _, stderr = run_git_command(['git', 'commit', '-m', message])
        if returncode != 0:
            print(f"Error committing changes: {stderr}")
            return False
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False
