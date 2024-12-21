import yaml

def load_yaml(file_path):
    """Load and validate YAML configuration."""
    with open(file_path, "r") as file:
        return yaml.safe_load(file)
