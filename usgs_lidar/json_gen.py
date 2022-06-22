"""Generate json data."""

import json

dict_reg = {}
with open("rg_year.txt", "r") as f:
    ind = 1
    for line in f:
        dict_reg[ind] = line.replace(" ", "").replace('"', "").replace("\n", "")
        ind = ind + 1
        # break

with open("regions.json", "w") as f:
    json.dump(dict_reg, f)