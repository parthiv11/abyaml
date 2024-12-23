
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
  - name: "postgres_source"
    config:
      sourceType: "postgres"        # Source type or definition_id is supported
      host: "demo-kelenson-3824.i.aivencloud.com"
      port: 14770
      database: "defaultdb"
      username: "avnadmin"
      password: "AVNS_MCKJ9yE3YcIhs7d-BNs"
      ssl_mode:
        mode: "require"             # SSL mode is required for secure connections

destinations:
  - name: "postgres_destination"
    config:
      destinationType: "postgres"   # Destination type
      host: "destination-ronete-b4e3.i.aivencloud.com"
      port: 22607
      database: "defaultdb"
      username: "avnadmin"
      password: "AVNS_5SLkItN2ulRZXSfJfwg"
      schema: "public"              # Destination schema
      ssl_mode:
        mode: "require"             # SSL mode is required for secure connections

connections:
- name: "p2p_connection"
  source: "postgres_source"         # Source name or source_id is supported
  destination: "postgres_destination" # Destination name or destination_id is supported
  streams:
    - name: "employees"
      syncMode: "full_refresh_overwrite" # Syncs all data by overwriting the target
      # cursorField:
        # - "<cursorField>"                      # Field used to track changes
      # primaryKey:
        # - ["id"]                    # Primary key fields
      # selectedFields:               # Fields to include in the sync
        # - fieldPath: 
            # - "<fieldPath>"
        # - fieldPath: 
            # - "<fieldPath>"
      # mappers:                      # Transformations applied to fields
        # - type: "hashing"
          # mapperConfiguration:
            # fieldNameSuffix: "<fieldNameSuffix>"    # Adds a suffix to the field name
            # method: "MD5"           # Hashing method used
            # targetField: "ii"       # Target field for the transformed data
  # schedule:
    # scheduleType: "manual"          # Sync is triggered manually
    # cronExpression: "0 0 * * *"     # Example: Sync daily at midnight
  # dataResidency: "auto"             # Automatically determines data residency
  # namespaceDefinition: "custom_format" # Custom namespace format for organizing data
  # namespaceFormat: "<namespaceFormat>"             #  namespace
  # prefix: "<prefix>"                      # Prefix added to table names
  # nonBreakingSchemaUpdatesBehavior: "propagate_columns" # Auto-add new columns
  # status: "active"                  # Connection is active

```


## Troubleshooting

- Ensure that your Airbyte instance is running and accessible at the provided `api_url`.
- Verify that the `client_id` and `client_secret` are valid for authentication.
