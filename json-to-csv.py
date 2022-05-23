import json
import glob
import pandas as pd

read_files = glob.glob("JSON/*.json")
output_list = []
all_items = []
for f in read_files:
    with open(f, "rb") as json_file:
        output_list.append(json.load(json_file))
df = pd.DataFrame(output_list)
df.to_csv("mri.csv", sep=";")
