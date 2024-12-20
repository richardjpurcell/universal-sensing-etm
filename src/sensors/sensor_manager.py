from typing import Dict, Tuple
import numpy as np

from .sensor import Sensor
from .station import Station
from ..utils.configuration_manager import ConfigurationManager

class SensorManager:
    """
    Manages multiple sensors and organizes them into stations.
    Stations are defined by their coordinates and contain multiple sensors.
    Implements a nearest-neighbor approach for coordinate matching if exact coords are not found.
    """

    def __init__(self, data_dict: dict, config_manager: ConfigurationManager):
        """
        :param data_dict: A dictionary mapping variable_name -> DataFrame.
        :param config_manager: An instance of ConfigurationManager to provide station info.
        """
        self.data_dict = data_dict
        self.config_manager = config_manager
        self.stations: Dict[Tuple[float, float], Station] = {}
        self._initialize_stations()

    def _initialize_stations(self):
        """
        Initialize stations based on configuration.
        If exact coordinates aren't found in the data, use nearest-neighbor coordinates.
        """

        stations_config = self.config_manager.get_stations_config()
        # We will pick one variable (e.g., the first listed variable) to derive the lat/lon grid.
        # Ideally, all variables should share the same coordinate system.
        if not self.data_dict:
            raise ValueError("data_dict is empty, cannot initialize stations.")

        # Pick a reference variable to extract coordinate sets
        reference_variable = next(iter(self.data_dict.keys()))
        ref_df = self.data_dict[reference_variable]

        unique_lats = np.sort(ref_df['latitude'].unique())
        unique_lons = np.sort(ref_df['longitude'].unique())

        for station_def in stations_config:
            desired_lat = station_def["latitude"]
            desired_lon = station_def["longitude"]
            variables = station_def["variables"]

            # Find nearest coordinates
            nearest_lat, nearest_lon = self._find_nearest_coordinates(desired_lat, desired_lon, unique_lats, unique_lons)

            sensors = {}
            for var in variables:
                if var in self.data_dict:
                    # Filter sensor_data to station coordinates using nearest lat/lon
                    sensor_data = self.data_dict[var]
                    sensor_data_for_station = sensor_data[
                        (sensor_data['latitude'] == nearest_lat) &
                        (sensor_data['longitude'] == nearest_lon)
                    ]
                    sensors[var] = Sensor(var, sensor_data_for_station)
                else:
                    raise ValueError(f"Variable '{var}' not found in provided data_dict.")

            station = Station(nearest_lat, nearest_lon, sensors)
            self.stations[(nearest_lat, nearest_lon)] = station

    def _find_nearest_coordinates(self, desired_lat: float, desired_lon: float,
                                  lat_array: np.ndarray, lon_array: np.ndarray) -> Tuple[float, float]:
        """
        Find the nearest available latitude and longitude to the desired coordinates.
        """
        nearest_lat = lat_array[np.argmin(np.abs(lat_array - desired_lat))]
        nearest_lon = lon_array[np.argmin(np.abs(lon_array - desired_lon))]
        return nearest_lat, nearest_lon

    def get_station(self, latitude: float, longitude: float) -> Station:
        """
        Retrieve a station by its coordinates. Note that this expects the *nearest matched* coordinates.
        If you originally requested (57.0, -111.0), but the nearest coordinates are (57.05, -111.05),
        you'll need to use those coordinates here, or implement a similar nearest-neighbor lookup.
        """
        return self.stations.get((latitude, longitude))

    def get_all_stations(self) -> Dict[Tuple[float, float], Station]:
        """
        Return all stations as a dictionary keyed by (lat, lon).
        """
        return self.stations
