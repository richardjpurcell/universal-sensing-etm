from .universal_encoder import UniversalEncoder

class HierarchicalEncoder(UniversalEncoder):
    """
    Extends the UniversalEncoder to allow multi-resolution encoding.
    """
    def __init__(self, resolutions: list = [10, 20, 50], min_value: float = None, max_value: float = None):
        """
        :param resolutions: List of resolutions (number of levels) for encoding.
        :param min_value: Minimum value for normalization.
        :param max_value: Maximum value for normalization.
        """
        super().__init__(levels=resolutions[0], min_value=min_value, max_value=max_value)
        self.resolutions = resolutions

    def encode_hierarchically(self, data):
        """
        Encode data at multiple resolutions.
        :param data: Pandas Series with raw sensor values.
        :return: Dictionary of encoded data at different resolutions.
        """
        encoded_outputs = {}
        for resolution in self.resolutions:
            self.levels = resolution
            encoded_outputs[f"resolution_{resolution}"] = self.encode(data)
        return encoded_outputs
