from typing import Dict
from .sensor import Sensor

class Station:
    """
    Represents a station, which is a collection of Sensor objects at a specific (lat, lon).
    """

    def __init__(self, latitude: float, longitude: float, sensors: Dict[str, Sensor]):
        """
        :param latitude: Latitude of the station
        :param longitude: Longitude of the station
        :param sensors: Dictionary of variable_name -> Sensor object
        """
        self.latitude = latitude
        self.longitude = longitude
        self.sensors = sensors

    def get_sensor(self, variable_name: str) -> Sensor:
        """
        Retrieve a sensor object by variable name.
        """
        return self.sensors.get(variable_name)

    def get_all_sensors(self) -> Dict[str, Sensor]:
        """
        Return all sensors as a dictionary of variable_name -> Sensor.
        """
        return self.sensors

    def get_coordinates(self) -> (float, float):
        """
        Return the coordinates (lat, lon) of the station.
        """
        return self.latitude, self.longitude
