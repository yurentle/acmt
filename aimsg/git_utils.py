import git

def get_staged_diff():
    """Get the diff of staged changes."""
    try:
        repo = git.Repo(".", search_parent_directories=True)
    except git.exc.InvalidGitRepositoryError:
        raise Exception("Not a git repository")

    # Get diff of staged changes
    diff = repo.git.diff("--cached")
    
    if not diff:
        return None
        
    return diff
