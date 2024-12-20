import os
import pandas as pd
import xarray as xr

class DataLoader:
    def __init__(self, data_dir: str = "../data/NetCDF"):
        """
        Initialize the DataLoader with a default or specified directory containing NetCDF files.
        
        :param data_dir: Directory path containing NetCDF data files.
        """
        self.data_dir = data_dir

    def load_variable(self, variable_name: str, file_list: list) -> pd.DataFrame:
        """
        Load multiple NetCDF files for a given variable and combine them into a single DataFrame.
        
        :param variable_name: Name of the variable (e.g., 'temperature', 'u_wind')
        :param file_list: List of NetCDF filenames corresponding to this variable.
        :return: A pandas DataFrame containing combined data for the specified variable.
        """
        combined_df = []
        for file in file_list:
            file_path = os.path.join(self.data_dir, file)
            print(f"Loading {variable_name} data from: {file_path}")

            # Open NetCDF file and convert to DataFrame
            ds = xr.open_dataset(file_path)
            df = ds.to_dataframe().reset_index()

            # Drop missing values and rename the variable column
            var_name_in_ds = list(ds.data_vars.keys())[0]
            df = df.dropna().rename(columns={var_name_in_ds: "value"})

            df["variable"] = variable_name  # Add variable name column
            combined_df.append(df)

        # Combine all DataFrames
        final_df = pd.concat(combined_df, ignore_index=True)
        return final_df

    def load_all(self, file_dict: dict) -> dict:
        """
        Load and combine data for all variables specified in file_dict.
        
        :param file_dict: A dictionary mapping variable names to lists of their NetCDF filenames.
                          Example: { "temperature": ["file1.nc", "file2.nc"], "u_wind": [...], ... }
        :return: A dictionary mapping variable names to their combined DataFrame.
        """
        dataframes = {}
        for variable_name, files in file_dict.items():
            print(f"\nLoading and combining {variable_name.capitalize()} files...")
            dataframes[variable_name] = self.load_variable(variable_name, files)
        return dataframes
