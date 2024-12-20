import pandas as pd
from ..encoding.universal_encoder import UniversalEncoder
from ..encoding.hierarchical_encoder import HierarchicalEncoder
from ..controllers.state_aware_precision_controller import StateAwarePrecisionController


class Sensor:
    def __init__(self, variable_name: str, data: pd.DataFrame):
        self.variable_name = variable_name
        self.data = data
        self.encoder = UniversalEncoder(levels=10)  # Default 10 levels
        self.precision_controller = StateAwarePrecisionController()  # Add this line

    def get_data(self):
        """Return raw sensor data."""
        return self.data

    def calculate_statistics(self):
        """Calculate basic statistics for the sensor data."""
        stats = {
            "mean": self.data["value"].mean(),
            "min": self.data["value"].min(),
            "max": self.data["value"].max(),
            "std": self.data["value"].std(),
            "count": self.data["value"].count(),
        }
        return stats

    def encode_data(self):
        """Apply the Universal Encoder to the sensor's data."""
        encoded_values = self.encoder.encode(self.data["value"])
        self.data["encoded_value"] = encoded_values
        return self.data

    def encode_hierarchically(self, resolutions: list = [10, 20, 50]):
        """Apply Hierarchical Encoder."""
        hierarchical_encoder = HierarchicalEncoder(resolutions=resolutions)
        return hierarchical_encoder.encode_hierarchically(self.data["value"])
    
    def encode_with_dynamic_precision(self):
        """
        Apply state-aware precision control on the sensor data.
        """
        # Calculate variability
        variability = self.precision_controller.calculate_variability(self.data["value"])

        # Adjust precision levels based on variability
        precision_levels = self.precision_controller.adjust_precision(variability)

        # Encode values dynamically
        encoded_values = self.precision_controller.encode_with_dynamic_precision(self.data["value"], precision_levels)

        # Add variability, precision levels, and encoded values to the DataFrame
        self.data["variability"] = variability
        self.data["precision_levels"] = precision_levels
        self.data["encoded_value_dynamic"] = encoded_values

        return self.data


    
    
