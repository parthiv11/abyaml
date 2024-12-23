
# abyaml

This script automates the creation of sources, destinations, and connections in Airbyte based on a provided YAML configuration file. It allows users to interact with the Airbyte API by passing necessary credentials and workspace details.

Install the fom source:

```bash
git clone https://github.com/parthiv11/abyaml/
cd abyaml
pip install -e .
```

## Usage

### Command-Line Arguments

- `config_file`: Path to the YAML configuration file containing the necessary details for sources, destinations, and connections.
- `--api_url`: (Optional) Airbyte API URL (defaults to `http://localhost:8000/api/public/v1`).
- `--client_id`: Client ID for authentication (required).
- `--client_secret`: Client Secret for authentication (required).

### Example

To run the script, execute the following command:

```bash
python airbyte_connection_manager.py /path/to/config.yaml --client_id YOUR_CLIENT_ID --client_secret YOUR_CLIENT_SECRET
```

### Configuration File (`config.yaml`)

The configuration YAML file should contain the following structure:

```yaml
workspaceId: YOUR_WORKSPACE_ID
sources:
  - name: "source1"
    type: "mysql"
    config:
      host: "localhost"
      port: 3306
      user: "user"
      password: "password"
      database: "source_db"
destinations:
  - name: "destination1"
    type: "postgres"
    config:
      host: "localhost"
      port: 5432
      user: "user"
      password: "password"
      database: "destination_db"
connections:
  - source: "source1"
    destination: "destination1"
    sync_mode: "full_refresh"
```


## Troubleshooting

- Ensure that your Airbyte instance is running and accessible at the provided `api_url`.
- Verify that the `client_id` and `client_secret` are valid for authentication.
