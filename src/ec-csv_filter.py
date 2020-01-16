# !/usr/bin/python3
import os
import sys

print(f"Number of arguments: {len(sys.argv)}, arguments:{sys.argv}")
str_dir = sys.argv[1]
if len(sys.argv) > 2:
    lst_clues = [tok for tok in sys.argv[2:]]

print(str_dir, lst_clues)

lst_files = list()
for root, dirs, files in os.walk(str_dir):
    for str_fn in files:
        str_ffn = os.path.join(root, str_fn)
        print(str_ffn)
        lst_files.append(str_ffn)

for str_ffn_in in lst_files:
    print(f"Filtering: {str_ffn_in}")
    lst_ffn_ou = str_ffn_in.rsplit('.', 1)
    str_ffn_ou = lst_ffn_ou[0] + '_out' + lst_ffn_ou[1]
    with open(str_ffn_in) as fil_in:
        with open(str_ffn_ou, "w") as fil_ou:
            for str_lin in fil_in:
                if any([clue in str_lin for clue in lst_clues]):
                    fil_ou.write(str_lin)