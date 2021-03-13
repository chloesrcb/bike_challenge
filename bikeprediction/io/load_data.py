import pandas as pd
from download import download
from bikeprediction.io import url_db, path_target

class Load_data:
  def __init__(self, url=url_db, target_name=path_target):
    download(url, target_name, replace=False)
  
  @staticmethod
  def save_as_df():
    df_bike = pd.read_csv(path_target, na_values="", low_memory=False, converters={'Date': str, 'Heure / Time': str})
    return df_bike