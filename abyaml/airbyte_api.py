import requests
from .utils import retry_request

class AirbyteAPI:
    def __init__(self, api_url, client_id, client_secret):
        self.api_url = api_url
        self.client_id = client_id
        self.client_secret = client_secret

    def generate_token(self):
        """Generate a new access token."""
        url = f"{self.api_url}/applications/token"
        payload = {
            "grant-type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()
        token_data = response.json()
        return token_data['access_token']
    
    def _make_request(self, method, endpoint, **kwargs):
        """Helper method to handle HTTP requests with Bearer Auth."""
        access_token = self.generate_token()
        headers = {
            "authorization": f"Bearer {access_token}",
            "Accept": "application/json",
        }
        url = f"{self.api_url}/{endpoint}"
        response = requests.request(method, url, headers=headers, **kwargs)
        response.raise_for_status()
        if response.status_code != 204:
            return response.json()

    @retry_request
    def get_workspace_id(self):
        """Fetch workspace ID."""
        workspaces = self._make_request("GET", "workspaces")["workspaces"]
        if not workspaces:
            raise ValueError("No workspaces found.")
        return workspaces[0]["workspaceId"]

    @retry_request
    def create_source(self, payload):
        """Create a source."""
        return self._make_request("POST", "sources", json=payload)
    
    @retry_request
    def delete_source(self, source_id):
        """Delete a source."""
        return self._make_request("DELETE", f"sources/{source_id}")

    @retry_request
    def create_destination(self, payload):
        """Create a destination."""
        return self._make_request("POST", "destinations", json=payload)
    
    @retry_request
    def delete_destination(self, destination_id):
        """Delete a destinations."""
        return self._make_request("DELETE", f"destinations/{destination_id}")

    @retry_request
    def create_connection(self, payload):
        """Create a connection."""
        return self._make_request("POST", "connections", json=payload)

    @retry_request
    def delete_connection(self, connection_id):
        """Delete a connection."""
        return self._make_request("DELETE", f"connection/{connection_id}")
