import yaml
import os

class ConfigurationManager:
    """
    Loads and provides configuration parameters from a YAML file.
    """

    def __init__(self, config_path: str = "../config/default_config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self) -> dict:
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Configuration file not found at {self.config_path}")

        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)

    def get_stations_config(self) -> list:
        """
        Returns a list of station definitions from the configuration file.
        Each definition includes latitude, longitude, and a list of variables.

        Example:
        [
          {
            "latitude": 45.0,
            "longitude": -120.0,
            "variables": ["temperature", "u_wind", "v_wind"]
          },
          ...
        ]
        """
        return self.config.get("stations", [])
