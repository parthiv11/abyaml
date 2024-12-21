import argparse
from abyaml.config_parser import load_yaml
from abyaml.connection_manager import ConnectionManager
import logging

logging.basicConfig(level=logging.INFO)

def main():
    parser = argparse.ArgumentParser(description="Airbyte Connection Manager")
    parser.add_argument("config_file", help="Path to the YAML configuration file")
    parser.add_argument("--api_url", default="http://localhost:8000/api/public/v1", help="Airbyte API URL")
    parser.add_argument("--client_id", required=True, help="Client ID")
    parser.add_argument("--client_secret", required=True, help="Client Secret")
    args = parser.parse_args()

    # Load configuration
    config = load_yaml(args.config_file)
    manager = ConnectionManager(args.api_url, args.client_id, args.client_secret, config.get("workspaceId"))

    try:
        logging.info("Creating sources...")
        source_id_map = manager.create_sources(config.get("sources", []))

        logging.info("Creating destinations...")
        destination_id_map = manager.create_destinations(config.get("destinations", []))

        logging.info("Creating connections...")
        connection_id_map = manager.create_connections(config.get("connections", []), source_id_map, destination_id_map)
        
        logging.info("✔ All operations completed successfully.")
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        logging.info("Rolling back...")
        manager.delete_connections(connection_id_map.values())
        manager.delete_sources(source_id_map.values())
        manager.delete_destinations(destination_id_map.values())
        logging.error("Rollback completed.")

if __name__ == "__main__":
    main()
