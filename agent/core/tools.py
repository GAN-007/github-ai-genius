from langchain.tools import tool
from github import Github, Auth
from services.vault import vault
from typing import List, Dict, Optional
import os

class GitHubTools:
    
    @staticmethod
    def _get_client():
        token = vault.get_secret("GITHUB_TOKEN")
        if not token:
            raise ValueError("GitHub Token not found in Vault")
        auth = Auth.Token(token)
        return Github(auth=auth)

    @tool
    def search_repositories(query: str, limit: int = 5) -> List[Dict[str, str]]:
        """
        Searches GitHub for repositories matching the query.
        Returns a list of repositories with name, description, and url.
        """
        g = GitHubTools._get_client()
        repos = g.search_repositories(query=query)[:limit]
        return [{"name": r.full_name, "description": r.description, "url": r.html_url} for r in repos]

    @tool
    def read_file_content(repo_name: str, file_path: str) -> str:
        """
        Reads the content of a specific file in a repository.
        """
        g = GitHubTools._get_client()
        repo = g.get_repo(repo_name)
        try:
            content = repo.get_contents(file_path)
            return content.decoded_content.decode('utf-8')
        except Exception as e:
            return f"Error reading file: {str(e)}"

    @tool
    def fork_repository(repo_name: str) -> str:
        """
        Forks a repository to the authenticated user's account.
        """
        g = GitHubTools._get_client()
        user = g.get_user()
        repo = g.get_repo(repo_name)
        fork = user.create_fork(repo)
        return f"Successfully forked to {fork.html_url}"

    @tool
    def create_pull_request(repo_name: str, title: str, body: str, head: str, base: str = "main") -> str:
        """
        Creates a pull request in the specified repository.
        """
        g = GitHubTools._get_client()
        repo = g.get_repo(repo_name)
        pr = repo.create_pull(title=title, body=body, head=head, base=base)
        return f"PR Created: {pr.html_url}"

    @tool
    def create_file(repo_name: str, file_path: str, content: str, message: str, branch: str = "main") -> str:
        """
        Creates or updates a file in the repository.
        """
        g = GitHubTools._get_client()
        repo = g.get_repo(repo_name)
        try:
            # Check if file exists to update
            contents = repo.get_contents(file_path, ref=branch)
            repo.update_file(contents.path, message, content, contents.sha, branch=branch)
            return f"Updated {file_path}"
        except:
            # Create new file
            repo.create_file(file_path, message, content, branch=branch)
            return f"Created {file_path}"

github_tools = [
    GitHubTools.search_repositories,
    GitHubTools.read_file_content,
    GitHubTools.fork_repository,
    GitHubTools.create_pull_request,
    GitHubTools.create_file
]
