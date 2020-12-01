#%%
import json
import glob

for in_file_name in glob.glob("/Users/polly.mckim/Desktop/OANN_others/oann-fixers/*txt"):
    out_file_name = in_file_name[:-4]+".json"
    with open(in_file_name, 'r') as in_file, \
        open(out_file_name, 'w') as out_file:
        out_file.write(
            json.dumps(
                    {
                        "text": in_file.read()
                    }
                )
            )

# %%
