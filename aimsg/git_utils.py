import os
import subprocess
from typing import Optional, Tuple

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

def get_staged_diff() -> Optional[str]:
    """获取已暂存的更改"""
    # 检查是否有暂存的更改
    returncode, staged_files, _ = run_git_command(['git', 'diff', '--cached', '--name-only'])
    if returncode != 0 or not staged_files.strip():
        return None
    
    # 检查是否有依赖文件的更改
    dependency_changes = [f for f in staged_files.splitlines() if os.path.basename(f) in DEPENDENCY_FILES]
    
    # 获取所有文件的完整 diff
    returncode, full_diff, _ = run_git_command(['git', 'diff', '--cached'])
    if returncode != 0:
        return None
    
    if not full_diff:
        return None
    
    # 如果有依赖文件变更，在 diff 前面添加特殊标记
    if dependency_changes:
        files_changed = ', '.join(os.path.basename(f) for f in dependency_changes)
        return f"DEPENDENCY_UPDATE:{files_changed}\n{full_diff}"
    
    return full_diff

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
