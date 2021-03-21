import urllib, json, os
import pandas as pd
from bikevisualization.io import url_counters, counters

def format_json(web_content):
  str_content = str(web_content)
  str_content = str_content.replace("\\n","")
  str_content = "["+str_content[2:-1]+"]"
  print(str_content[0:15])
  str_content = str_content.replace("} {","},{")
  str_content = str_content.replace("}  {","},{")
  str_content = str_content.replace("}   {","},{")
  str_content = str_content.replace("}{","},{")
  return str_content

class Load_json:
  def __init__(self, list_url=url_counters, list_name=counters):
    for i in range(len(list_url)):
      url = list_url[i]
      counter_name = list_name[i]

      response = urllib.request.urlopen(url)
      web_content = response.read()
      str_content = format_json(web_content)

      path_target = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "data", counter_name + ".json")
      file = open(path_target, "w")
      file.write(str_content)
  
  @staticmethod
  def save_as_df(list_name=counters):
    df_list = []
    for counter in list_name :
      path_target = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "data", counter + ".json")
      print(counter)
      df = pd.read_json(path_target)
      df_list.append(df)

    return df_list