import pandas as pd

class UniversalEncoder:
    """
    Encodes raw sensor data into a normalized, quantized, and symbolic representation.
    """
    def __init__(self, levels: int = 10, min_value: float = None, max_value: float = None):
        """
        :param levels: Number of discrete levels for quantization.
        :param min_value: Minimum value for normalization (if None, auto-calculated from data).
        :param max_value: Maximum value for normalization (if None, auto-calculated from data).
        """
        self.levels = levels
        self.min_value = min_value
        self.max_value = max_value

    def fit(self, data: pd.Series, fixed_min: float = 280.0, fixed_max: float = 300.0):
        """
        Fit the min and max values based on the data or fixed thresholds.
        """
        self.min_value = fixed_min
        self.max_value = fixed_max


    def normalize(self, data: pd.Series) -> pd.Series:
        """
        Normalize data to the range [0, 1].
        :param data: Pandas Series with raw sensor values.
        :return: Normalized data as a Pandas Series.
        """
        # Normalize data and clip values to [0, 1]
        normalized = (data - self.min_value) / (self.max_value - self.min_value)
        return normalized.clip(0, 1).fillna(0.0).replace([float("inf"), float("-inf")], 0.0)

    def quantize(self, normalized_data: pd.Series) -> pd.Series:
        """
        Quantize normalized data into discrete levels.
        :param normalized_data: Normalized data as a Pandas Series.
        :return: Quantized data as integers.
        """
        # Scale normalized data to levels, round, and ensure integer type
        quantized = (normalized_data * (self.levels - 1)).round(0)
        return quantized.fillna(0).astype(int)

    def encode(self, data: pd.Series) -> pd.Series:
        """
        Encode raw sensor data into symbolic levels.
        :param data: Pandas Series with raw sensor values.
        :return: Encoded symbolic series.
        """
        # Fit the encoder, normalize, and quantize
        self.fit(data)
        normalized_data = self.normalize(data)
        quantized_data = self.quantize(normalized_data)
        return quantized_data
