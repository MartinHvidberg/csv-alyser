#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

"""

import dateutil.parser
from uuid import UUID

### ToDo
#   real logging

def isinteger(str_in):
    try:
        num_n = int(str_in)
        return True
    except ValueError:
        return False

if __name__ == '__main__':

    # Hardcoded - to be later converted to command line parameters
    str_fn_i_name = r"../data/demo.csv"
    str_fn_f_name = r"../data/demo.ecffc"

    # Load file format
    dic_format = dict()  # Create dict and fill with some default values.
    dic_format["header"] = 'Yes'
    dic_format["delim"] = ','
    dic_format["tokens"] = dict()
    with open(str_fn_f_name, 'r') as filf:
        for line in filf:
            str_info = line.split("#")[0]
            if len(str_info) > 1:
                if str_info[0] == "+" and ":" in str_info:
                    str_hkey = str_info[1:].split(":")[0].strip().lower()
                    str_hval = str_info[1:].split(":")[1].strip()
                    ##print "ffk:", str_hkey, "=", str_hval
                    if str_hkey != "tokens":
                        dic_format[str_hkey] = str_hval
                else:
                    ##print "fft: |" + str_info.strip() + "|"
                    lst_tok = str_info.split(",")
                    if isinteger(lst_tok[0]):
                        dic_tok = dict()
                        dic_tok["datatype"] = lst_tok[1].strip()
                        if len(lst_tok[2].strip()) > 0:
                            dic_tok["maxi_len"] = float(lst_tok[2].strip())
                        if len(lst_tok[3].strip()) > 0:
                            dic_tok["maxi_val"] = float(lst_tok[3].strip())
                        if len(lst_tok[4].strip()) > 0:
                            dic_tok["precessi"] = float(lst_tok[4].strip())
                        dic_tok["nullable"] = bool(lst_tok[5].strip())
                        dic_tok["null_val"] = lst_tok[6].strip()
                        dic_format["tokens"][int(lst_tok[0])] = dic_tok
                    else:
                        print "First token must be integer. Skipping line:", line

    deli = dic_format["delim"]
    head = dic_format['header'].lower() == 'yes'

    print head, deli, dic_format
    for k in dic_format['tokens'].keys():
        print str(type(k)), k

    cnt_lines = 0
    with open(str_fn_i_name, 'r') as fili:
        for line in fili:
            if cnt_lines == 0 and head:
                print "header", line
                lst_header = line.split(deli)
                num_cols = len(lst_header)
            else:
                lst_tok = line.split(deli)
                if head:
                    if len(lst_tok) != num_cols:
                        print "!!! Row has wrong number of delimiters:", line
                        continue
                for num_col in range(num_cols):
                    str_val = lst_tok[num_col].strip()
                    dic_fmt = dic_format['tokens'][num_col+1]
                    ##print ">>>", num_col, str_val, dic_fmt
                    # Data-type
                    lst_vali = list()
                    if dic_fmt['datatype'].lower() == 'boolean':
                        if str_val.lower() in ['true', 'false', 'yes', 'no', '1', '0']:
                            lst_vali.append(True)
                        else:
                            lst_vali.append(False)
                            print "!!! Type error: line {} > '{}' is not {}".format(cnt_lines, str_val, dic_fmt['datatype'])
                    elif dic_fmt['datatype'].lower() == 'integer':
                        try:
                            res = int(str_val)
                            lst_vali.append(True)
                        except ValueError:
                            lst_vali.append(False)
                            print "!!! Type error: line {} > '{}' is not {}".format(cnt_lines, str_val, dic_fmt['datatype'])
                    elif dic_fmt['datatype'].lower() == 'float':
                        try:
                            res = float(str_val)
                            lst_vali.append(True)
                        except ValueError:
                            lst_vali.append(False)
                            print "!!! Type error: line {} > '{}' is not {}".format(cnt_lines, str_val, dic_fmt['datatype'])
                    elif dic_fmt['datatype'].lower() == 'date':
                        try:
                            res = dateutil.parser.parse(str_val)
                            lst_vali.append(True)
                        except ValueError:
                            lst_vali.append(False)
                            print "!!! Type error: line {} > '{}' is not {}".format(cnt_lines, str_val, dic_fmt['datatype'])
                    elif dic_fmt['datatype'].lower() == 'string':
                        pass  ## Nothing to check...
                    elif dic_fmt['datatype'].lower() == 'uuid':
                        try:
                            res = UUID(str_val, version=4)
                            lst_vali.append(True)
                        except ValueError:
                            lst_vali.append(False)
                            print "!!! Type error: line {} > '{}' is not {}".format(cnt_lines, str_val, dic_fmt['datatype'])
                    else:
                        print "Seems to be non ISO data type:", dic_fmt['datatype']


            # register progress
            cnt_lines += 1
            if cnt_lines%100000 == 0:
                print "line:", cnt_lines

    print "Done {} lines...".format(cnt_lines)
