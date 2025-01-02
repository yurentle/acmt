import os
import git
from git import Repo

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

def get_staged_diff():
    """Get the diff of staged changes."""
    try:
        repo = Repo(".", search_parent_directories=True)
    except git.exc.InvalidGitRepositoryError:
        raise Exception("Not a git repository")

    staged_files = [item.a_path for item in repo.index.diff("HEAD")]
    
    # 检查是否有依赖文件的变更
    dependency_changes = [f for f in staged_files if os.path.basename(f) in DEPENDENCY_FILES]
    
    # 获取所有文件的完整 diff
    full_diff = repo.git.diff("--cached")
    
    if not full_diff:
        return None
    
    # 如果有依赖文件变更，在 diff 前面添加特殊标记
    if dependency_changes:
        files_changed = ', '.join(os.path.basename(f) for f in dependency_changes)
        return f"DEPENDENCY_UPDATE:{files_changed}\n{full_diff}"
    
    return full_diff
