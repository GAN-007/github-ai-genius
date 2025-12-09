import os
import time
import jwt
import requests
from typing import Optional, Dict

class GitHubAuthService:
    """
    Handles authentication via GitHub Apps and HashiCorp Vault integration.
    Implements the 'User-on-Behalf-Of' (UOB) flow and token lifecycle management.
    """
    
    def __init__(self, app_id: str, private_key_path: str, vault_url: str):
        self.app_id = app_id
        self.private_key = self._load_private_key(private_key_path)
        self.vault_url = vault_url
        self.current_token: Optional[str] = None
        self.token_expires_at: float = 0

    def _load_private_key(self, path: str) -> str:
        # In production, this might fetch from a secure volume
        with open(path, 'r') as f:
            return f.read()

    def generate_jwt(self) -> str:
        """Generates a JWT for authenticating as the GitHub App."""
        payload = {
            'iat': int(time.time()),
            'exp': int(time.time()) + (10 * 60),
            'iss': self.app_id
        }
        return jwt.encode(payload, self.private_key, algorithm='RS256')

    def get_installation_token(self, installation_id: str) -> str:
        """Retrieves an installation access token, potentially from Vault."""
        # Check if valid token exists in memory
        if self.current_token and time.time() < self.token_expires_at:
            return self.current_token

        # Logic to fetch from Vault would go here
        # For scaffolding, we simulate a direct GitHub API call
        jwt_token = self.generate_jwt()
        headers = {
            'Authorization': f'Bearer {jwt_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        url = f'https://api.github.com/app/installations/{installation_id}/access_tokens'
        
        # Mock response for scaffolding
        # response = requests.post(url, headers=headers)
        # data = response.json()
        
        print(f"[Auth] Refreshing token for installation {installation_id} via GitHub App flow")
        self.current_token = "ghs_mock_token_scaffold"
        self.token_expires_at = time.time() + 3600
        
        return self.current_token

    def validate_user_identity(self, user_token: str) -> bool:
        """
        Crucial security step: Revalidates user identity to prevent token confusion.
        """
        headers = {'Authorization': f'Bearer {user_token}'}
        response = requests.get('https://api.github.com/user', headers=headers)
        if response.status_code == 200:
            print(f"[Auth] User identity validated: {response.json().get('login')}")
            return True
        return False
