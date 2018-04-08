#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Reads through a .csv (Comma Seperated Values) type file, and looks for errors.
Also needs an .ecffc file, that defines what to be consider an error.

Usage: ec_csv_check.py demo.csv demo.ecffc
"""

import sys
import dateutil.parser
from uuid import UUID

### ToDo
#   Error statistics summary
#   real CLI interface
#   real testing
#   real documantation
#   real logging

def isinteger(str_in):
    try:
        num_n = int(str_in)
        return True
    except ValueError:
        return False

if __name__ == '__main__':

    # Read CLI parameters
    if len(sys.argv) > 2:
        str_fn_i_name = sys.argv[1] # Assume this to be the .csv file
        str_fn_f_name = sys.argv[2] # Assume this to be the .ecffc file
    else:
        print "\n\tUsage: ec_csv_check.py demo.csv demo.ecffc"
        sys.exit(999)

    # Load file format
    dic_format = dict()  # Create dict and fill with some default values.
    dic_format["header"] = 'Yes'
    dic_format["delim"] = ','
    dic_format["nodata"] = 'N/A'
    dic_format["tokens"] = dict()
    with open(str_fn_f_name, 'r') as filf:  # Overwrite the defaults with the values from the .ecffc file
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
                        dic_tok["nullable"] = lst_tok[5].strip().lower() == "yes"
                        dic_format["tokens"][int(lst_tok[0])] = dic_tok
                    else:
                        print "First token must be + or integer. Skipping line:", line

    deli = dic_format["delim"]
    head = dic_format['header'].lower() == 'yes'
    noda = dic_format['nodata'].strip('"')
    lst_error_by_col = [0 for t in dic_format['tokens'].keys()]

    cnt_lines = 0
    num_cols = 0
    with open(str_fn_i_name, 'r') as fili:
        for line in fili:
            bol_err_in_this_line = False
            if cnt_lines == 0 and head:
                ##print "header", line
                lst_header = line.split(deli)
                num_cols = len(lst_header)
            else:
                lst_tok = line.split(deli)
                if head and num_cols != 0:
                    if len(lst_tok) != num_cols:
                        print "! lin {} has wrong number of delimiters:".format(cnt_lines, line)
                        continue
                for num_col in range(num_cols):
                    str_val = lst_tok[num_col].strip()
                    dic_fmt = dic_format['tokens'][num_col+1]

                    # Data-type
                    if dic_fmt['datatype'].lower() == 'boolean':
                        if str_val.lower() in ['true', 'false', 'yes', 'no', '1', '0']:
                            pass
                        else:
                            bol_err_in_this_line = True
                            lst_error_by_col[num_col] += 1
                            print "! lin {} col {} Type error: '{}' is not {}".format(cnt_lines, num_col, str_val, dic_fmt['datatype'])
                    elif dic_fmt['datatype'].lower() == 'integer':
                        try:
                            res = int(str_val)
                        except ValueError:
                            bol_err_in_this_line = True
                            lst_error_by_col[num_col] += 1
                            print "! lin {} col {} Type error: '{}' is not {}".format(cnt_lines, num_col, str_val, dic_fmt['datatype'])
                    elif dic_fmt['datatype'].lower() == 'float':
                        try:
                            res = float(str_val)
                        except ValueError:
                            bol_err_in_this_line = True
                            lst_error_by_col[num_col] += 1
                            print "! lin {} col {} Type error: '{}' is not {}".format(cnt_lines, num_col, str_val, dic_fmt['datatype'])
                    elif dic_fmt['datatype'].lower() == 'date':
                        try:
                            res = dateutil.parser.parse(str_val)
                        except ValueError:
                            bol_err_in_this_line = True
                            lst_error_by_col[num_col] += 1
                            print "! lin {} col {} Type error: '{}' is not {}".format(cnt_lines, num_col, str_val, dic_fmt['datatype'])
                    elif dic_fmt['datatype'].lower() == 'string':
                        pass  ## Nothing to check...
                    elif dic_fmt['datatype'].lower() == 'uuid':
                        try:
                            res = UUID(str_val, version=4)
                        except ValueError:
                            bol_err_in_this_line = True
                            lst_error_by_col[num_col] += 1
                            print "! lin {} col {} Type error: '{}' is not {}".format(cnt_lines, num_col, str_val, dic_fmt['datatype'])
                    else:
                        print "Seems to be non ISO data type:", dic_fmt['datatype']

                    # Maximum length
                    if not bol_err_in_this_line:  # i.e. No errors so far, in this line
                        if 'maxi_len' in dic_fmt.keys():
                            if len(str_val) <= dic_fmt['maxi_len']:
                                pass
                            else:
                                bol_err_in_this_line = True
                                lst_error_by_col[num_col] += 1
                                print "! lin {} col {} Maxi-length error: '{}' exceeds {} length".format(cnt_lines, num_col, str_val, dic_fmt['maxi_len'])

                    # Maximum value
                    if not bol_err_in_this_line:  # i.e. No errors so far, in this line
                        if 'maxi_val' in dic_fmt.keys() and dic_fmt['datatype'].lower() in ('integer', 'float'):
                            if float(str_val) <= float(dic_fmt['maxi_val']):
                                pass
                            else:
                                bol_err_in_this_line = True
                                lst_error_by_col[num_col] += 1
                                print "! lin {} col {} Maxi-value error: '{}' exceeds {} value".format(cnt_lines, num_col, str_val, dic_fmt['maxi_val'])

                    # Maximum precession
                    if not bol_err_in_this_line:  # i.e. No errors so far, in this line
                        if 'precessi' in dic_fmt.keys() and dic_fmt['datatype'].lower() in ('float'):
                            if len(str_val.split('.')[1]) <= float(dic_fmt['precessi']):
                                pass
                            else:
                                bol_err_in_this_line = True
                                lst_error_by_col[num_col] += 1
                                print "! lin {} col {} Maxi-precession error: '{}' exceeds {} decimals".format(cnt_lines, num_col, str_val, dic_fmt['precessi'])

                    # Illegal no-data occurrences
                    if True: # not bol_err_in_this_line):  # i.e. No errors so far, in this line
                        if 'nullable' in dic_fmt.keys():
                            ##print "\t", dic_fmt['nullable'], "|"+str_val+"|"
                            if dic_fmt['nullable'] == True or str_val != noda:
                                pass
                            else:
                                bol_err_in_this_line = True
                                lst_error_by_col[num_col] += 1
                                print "! lin {} col {} Nullable error: No-data value in non-nullable column.".format(cnt_lines, num_col, str_val)

            # register progress
            cnt_lines += 1
            if cnt_lines%100000 == 0:
                print "line:", cnt_lines

    # Summarize error statistics...
    print "\nNumber of Errors in {} lines, by column = {}".format(cnt_lines, lst_error_by_col)

    print "Done..."
