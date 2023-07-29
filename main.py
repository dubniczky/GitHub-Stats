import os
import sys
import shutil
import git
from github import Github


tempdir = "./temp"


# Delete all files in tempdir
def delete_dir_recursive(path):
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def clone_repositories(user_repositories):
    line_insertions = 0
    for repo in user_repositories:
        root = f'./temp/{repo.full_name}'
        print(f"Cloning {repo.full_name} -> {root}")
        
        try:
            git.Repo.clone_from(repo.ssh_url, root)
        except Exception as e:
            print(f"Failed to clone {repo.full_name}: {e}")
        
        current = count_line_insertions(root)
        print(f"Repo: {repo.full_name}: {current} lines")
        line_insertions += current
    print(f"Total: {line_insertions} lines")
    

def count_line_insertions(repo_path):
    repo = git.Repo(repo_path)
    line_insertions = 0

    for commit in repo.iter_commits():
        diff = commit.diff(commit.parents[0], create_patch=True) if commit.parents else commit.diff(create_patch=True)
        for file_diff in diff:
            diff_str = file_diff.diff.decode('utf-8')
            for line in diff_str.split('\n'):
                if line.startswith('+') and not line.startswith('+++'):
                    line_insertions += 1


    return line_insertions


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python main.py <username>")
        sys.exit(0)
    
    username = sys.argv[1]
    
    gh = Github()
    user = gh.get_user(username)
    user_repositories = list(user.get_repos())

    os.makedirs(tempdir, exist_ok=True)

    delete_dir_recursive(tempdir)
    clone_repositories(user_repositories)
