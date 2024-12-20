import pandas as pd
from datetime import datetime

class Sensor:
    """
    Represents a single sensor, holding data for one modality (e.g., temperature, u_wind, v_wind).
    Provides methods for filtering and basic analysis.
    """
    def __init__(self, variable_name: str, data: pd.DataFrame):
        """
        Initialize a Sensor instance.

        :param variable_name: Name of the sensor variable (e.g., "temperature", "u_wind")
        :param data: A pandas DataFrame containing sensor data.
                     Expected columns: ['latitude', 'longitude', 'valid_time', 'value', 'variable']
        """
        self.variable_name = variable_name
        self.data = data.copy()  # store a copy to avoid modifying the original DataFrame
        self._validate_data()

    def _validate_data(self):
        """Validate that the DataFrame has expected columns."""
        required_columns = {"latitude", "longitude", "valid_time", "value", "variable"}
        if not required_columns.issubset(self.data.columns):
            missing = required_columns - set(self.data.columns)
            raise ValueError(f"The following required columns are missing from the data: {missing}")

    def get_data(self) -> pd.DataFrame:
        """Return the sensor's entire DataFrame."""
        return self.data

    def filter_by_time(self, start: datetime, end: datetime) -> pd.DataFrame:
        """
        Return a subset of the sensor data between start and end times (inclusive).

        :param start: Start datetime
        :param end: End datetime
        :return: A filtered DataFrame
        """
        mask = (self.data['valid_time'] >= start) & (self.data['valid_time'] <= end)
        return self.data.loc[mask].copy()

    def calculate_statistics(self) -> dict:
        """
        Calculate basic statistics on the 'value' column.

        :return: A dictionary with keys: 'mean', 'min', 'max', 'std', 'count'
        """
        stats = self.data['value'].agg(['mean', 'min', 'max', 'std', 'count'])
        return stats.to_dict()
