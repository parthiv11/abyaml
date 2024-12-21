import logging
from abyaml.airbyte_api import AirbyteAPI

class ConnectionManager:
    def __init__(self, api_url, client_id, client_secret, workspace_id=None):
        """Initialize the ConnectionManager with API client."""
        self.api = AirbyteAPI(api_url, client_id, client_secret)
        self.workspace_id = workspace_id or self.api.get_workspace_id()

    def create_sources(self, sources):
        """Create sources and map names to their IDs."""
        source_id_map = {}
        for source in sources:
            try:
                payload = {
                    "name": source["name"],
                    "workspaceId": self.workspace_id,
                    "configuration": source.get("config", {})
                }

                # Check if the definition_id exists and add it
                if 'definition_id' in source["config"]:
                    payload['definitionId'] = source["config"].pop("definition_id")
                
                # Create source and store the sourceId in the map
                response = self.api.create_source(payload)
                source_id_map[source["name"]] = response["sourceId"]
                logging.info(f"✔ {source['name']} (ID: {response['sourceId']})")
            except Exception as e:
                logging.error(f"Failed to create source {source['name']}: {e}")
        return source_id_map
    
    def delete_sources(self, source_ids):
        """Delete sources by their IDs."""
        for source_id in source_ids:
            try:
                self.api.delete_source(source_id=source_id)
                logging.info(f"✔ Source (ID: {source_id}) deleted")
            except Exception as e:
                logging.error(f"Failed to delete source (ID: {source_id}): {e}")

    def create_destinations(self, destinations):
        """Create destinations and map names to their IDs."""
        destination_id_map = {}
        for destination in destinations:
            try:
                payload = {
                    "name": destination["name"],
                    "workspaceId": self.workspace_id,
                    "configuration": destination.get("config", {})
                }

                # Check if the definition_id exists and add it
                if 'definition_id' in destination["config"]:
                    payload['definitionId'] = destination["config"].pop("definition_id")
                
                # Create destination and store the destinationId in the map
                response = self.api.create_destination(payload)
                destination_id_map[destination["name"]] = response["destinationId"]
                logging.info(f"✔ {destination['name']} (ID: {response['destinationId']})")
            except Exception as e:
                logging.error(f"Failed to create destination {destination['name']}: {e}")
        return destination_id_map
    
    def delete_destinations(self, destination_ids):
        """Delete destinations by their IDs."""
        for destination_id in destination_ids:
            try:
                self.api.delete_destination(destination_id=destination_id)
                logging.info(f"✔ Destination (ID: {destination_id}) deleted")
            except Exception as e:
                logging.error(f"Failed to delete destination (ID: {destination_id}): {e}")

    def create_connections(self, connections, source_id_map, destination_id_map):
        """Create connections using mapped source and destination IDs, or use direct IDs."""
        connection_id_map = {}
        for connection in connections:
            try:
                # Use provided source_id and destination_id directly if available, otherwise map from names
                source_id = connection.get("source_id", source_id_map.get(connection.get("source")))
                destination_id = connection.get("destination_id", destination_id_map.get(connection.get("destination")))

                if not source_id or not destination_id:
                    raise ValueError(f"Invalid source or destination for connection {connection['name']}")

                payload = {
                    "name": connection["name"],
                    "sourceId": source_id,
                    "destinationId": destination_id,
                }

                # Include streams and mappers if provided
                if "streams" in connection:
                    payload["configurations"] = {"streams": connection["streams"]}
                
                if "mappers" in connection:
                    payload["configurations"] = {"mappers": connection["mappers"]}

                if "schedule" in connection:
                    payload["schedule"] = connection["schedule"]

                # Create connection and store the connectionId in the map
                response = self.api.create_connection(payload)
                connection_id_map[connection["name"]] = response['connectionId']
                logging.info(f"✔ {connection['name']} (ID: {response['connectionId']})")
            except Exception as e:
                logging.error(f"Failed to create connection {connection['name']}: {e}")
        return connection_id_map

    def delete_connections(self, connection_ids):
        """Delete connections by their IDs."""
        for connection_id in connection_ids:
            try:
                self.api.delete_connection(connection_id=connection_id)
                logging.info(f"✔ Connection (ID: {connection_id}) deleted")
            except Exception as e:
                logging.error(f"Failed to delete connection (ID: {connection_id}): {e}")
