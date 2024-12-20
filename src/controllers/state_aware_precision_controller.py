import numpy as np
import pandas as pd
from ..encoding.universal_encoder import UniversalEncoder

class StateAwarePrecisionController:
    """
    Adjusts encoding precision dynamically based on data variability.
    """
    def __init__(self, base_levels: int = 10, high_variability_levels: int = 50, threshold: float = 1.0):
        """
        :param base_levels: Default number of encoding levels.
        :param high_variability_levels: Number of levels when variability is high.
        :param threshold: Standard deviation threshold to trigger precision changes.
        """
        self.base_levels = base_levels
        self.high_variability_levels = high_variability_levels
        self.threshold = threshold
        self.encoder = UniversalEncoder(levels=self.base_levels)

    def calculate_variability(self, data: pd.Series, window: int = 10) -> pd.Series:
        """
        Calculate smoothed rolling variability (standard deviation) using an EWMA.
        """
        rolling_std = data.rolling(window=window).std()
        smoothed_variability = rolling_std.ewm(span=window).mean()
        return smoothed_variability.fillna(0.0)


    def adjust_precision(self, variability: pd.Series) -> pd.Series:
        """
        Adjust encoding precision smoothly based on variability.
        Intermediate precision levels are used for soft transitions.
        """
        def map_variability_to_levels(var):
            if var > self.threshold * 1.5:  # High variability
                return self.high_variability_levels
            elif var > self.threshold:  # Medium variability
                return (self.base_levels + self.high_variability_levels) // 2
            else:  # Low variability
                return self.base_levels

        precision_levels = variability.apply(map_variability_to_levels)
        return precision_levels


    def encode_with_dynamic_precision(self, data: pd.Series, precision_levels: pd.Series) -> pd.Series:
        """
        Encode data dynamically using adjusted precision levels.
        :param data: Pandas Series of sensor values.
        :param precision_levels: Pandas Series indicating precision levels.
        :return: Pandas Series of dynamically encoded values.
        """
        encoded_values = []
        for i, (value, levels) in enumerate(zip(data, precision_levels)):
            self.encoder.levels = levels
            encoded_values.append(self.encoder.encode(pd.Series([value])).iloc[0])
        return pd.Series(encoded_values, index=data.index)
