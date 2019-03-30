#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Reads through a .csv (Comma Seperated Values) type file, and looks for errors.
Also needs an .ecffc file, that defines what to be consider an error.

Usage: ec_csv_check.py demo_checker.csv demo_checker.ecffc
"""

import sys
import dateutil.parser
from uuid import UUID

### ToDo
#   Uniqueness by column check
#   Error statistics summary
#   real CLI interface
#   real testing
#   real documantation
#   real logging

def load_format_file(str_fn):

    print("\nLoading format file: {}".format(str_fn))

    # Load file format
    dic_format = dict()  # Create dict and fill with some default values.
    dic_format["header"] = 'Yes'
    dic_format["delim"] = ','
    dic_format["nodata"] = 'N/A'
    dic_format["tokens"] = dict()
    with open(str_fn, 'r') as filf:  # Overwrite the defaults with the values from the .ecffc file
        for line in filf:
            str_info = line.split("#")[0]  # Lose all comments
            str_info = str_info.strip().replace('\t','')  # Trim and lose TAB
            if len(str_info) > 1:  # Skip empty lines
                if str_info[0] == "+" and ":" in str_info:  # Spec for entire data file
                    str_hkey, str_hval = [tok.strip() for tok in str_info[1:].strip().split(':')]
                    ##print "ffk:", str_hkey, "=", str_hval
                    if str_hkey != "tokens":
                        dic_format[str_hkey] = str_hval
                else:  # Specs for a specific column of data
                    ##print "fft: |" + str_info.strip() + "|"
                    if ',' in str_info:
                        lst_tok = [tok.strip() for tok in str_info.strip().split(',')]
                        if isinteger(lst_tok[0]):  # Column definition must start with column number
                            num_col = int(lst_tok[0])
                            if num_col in dic_format["tokens"].keys():
                                print("Warning: Column number {} have all ready been defined, Skipping line: \"{}\"".format(num_col, str_info))
                                continue
                            dic_tok = dict()
                            dic_tok["datatype"] = lst_tok[1].strip()
                            if len(lst_tok[2].strip()) > 0:
                                dic_tok["maxi_len"] = float(lst_tok[2].strip())
                            if len(lst_tok[3].strip()) > 0:
                                dic_tok["maxi_val"] = float(lst_tok[3].strip())
                            if len(lst_tok[4].strip()) > 0:
                                dic_tok["precessi"] = float(lst_tok[4].strip())
                            dic_tok["nullable"] = lst_tok[5].strip().lower() == "yes"
                            dic_format["tokens"][num_col] = dic_tok
                        else:
                            print("First token must be + or integer. Skipping line: {}".format(line))
                    else:
                        print("Format descripter line have no ','. That is strange: {}".format(line))

    print("Format:")
    for keyf in dic_format.keys():
        if keyf != 'tokens':
            print("  {}: {}".format(keyf, dic_format[keyf]))
    if 'tokens' in dic_format.keys():
        for keyt in sorted(dic_format['tokens'].keys()):
            print("    {} : {}".format(keyt, dic_format['tokens'][keyt]))

    return dic_format

def isinteger(str_in):
    try:
        num_n = int(str_in)
        return True
    except ValueError:
        return False

def scan_data_file(str_fn, dic_form):

    print("\nScanning data file: {}".format(str_fn))
    dic_ret = dict()

    str_deli = dic_form["delim"]
    bol_head = dic_form['header'].lower() == 'yes'
    str_noda = dic_form['nodata'].strip('"')
    lst_error_by_col = [0 for t in dic_form['tokens'].keys()]

    cnt_lines = 0
    num_cols = 0
    with open(str_fn, 'r') as fili:
        for line in fili:
            bol_err_in_this_line = False  # Assumed innocent, until proven guilty...
            lst_tok = [tok.strip() for tok in line.strip().split(str_deli)]
            if cnt_lines == 0 and bol_head:
                lst_header = lst_tok
                num_cols = len(lst_header)
                print("Delimiter: {}\nNumber of columns: {}\nheader: {}".format(str_deli, num_cols, lst_header))
            else:
                if bol_head and num_cols != 0:
                    if len(lst_tok) != num_cols:
                        print("! lin {} has wrong number of delimiters: {}".format(cnt_lines, line))
                        continue
                for num_col in range(num_cols):
                    str_val = lst_tok[num_col].strip()
                    dic_fmt = dic_form['tokens'][num_col+1]

                    # Data-type
                    if str_val != '':
                        if dic_fmt['datatype'].lower() == 'boolean':
                            if str_val.lower() in ['true', 'false', 'yes', 'no', '1', '0']:
                                pass
                            else:
                                bol_err_in_this_line = True
                                lst_error_by_col[num_col] += 1
                                print("! lin {} col {} Type error: '{}' is not {}".format(cnt_lines, num_col, str_val, dic_fmt['datatype']))
                        elif dic_fmt['datatype'].lower() == 'integer':
                            try:
                                res = int(str_val)
                            except ValueError:
                                bol_err_in_this_line = True
                                lst_error_by_col[num_col] += 1
                                print("! lin {} col {} Type error: '{}' is not {}".format(cnt_lines, num_col, str_val, dic_fmt['datatype']))
                        elif dic_fmt['datatype'].lower() == 'float':
                            try:
                                res = float(str_val)
                            except ValueError:
                                bol_err_in_this_line = True
                                lst_error_by_col[num_col] += 1
                                print("! lin {} col {} Type error: '{}' is not {}".format(cnt_lines, num_col, str_val, dic_fmt['datatype']))
                        elif dic_fmt['datatype'].lower() == 'date':
                            try:
                                res = dateutil.parser.parse(str_val)
                            except ValueError:
                                bol_err_in_this_line = True
                                lst_error_by_col[num_col] += 1
                                print("! lin {} col {} Type error: '{}' is not {}".format(cnt_lines, num_col, str_val, dic_fmt['datatype']))
                        elif dic_fmt['datatype'].lower() == 'string':
                            pass  ## Nothing to check...
                        elif dic_fmt['datatype'].lower() == 'uuid':
                            try:
                                res = UUID(str_val, version=4)
                            except ValueError:
                                bol_err_in_this_line = True
                                lst_error_by_col[num_col] += 1
                                print("! lin {} col {} Type error: '{}' is not {}".format(cnt_lines, num_col, str_val, dic_fmt['datatype']))
                        else:
                            pass #XXXprint "Seems to be non ISO data type:", dic_fmt['datatype']

                        # Maximum length
                        if not bol_err_in_this_line:  # i.e. No errors so far, in this line
                            if 'maxi_len' in dic_fmt.keys():
                                if len(str_val) <= dic_fmt['maxi_len']:
                                    pass
                                else:
                                    bol_err_in_this_line = True
                                    lst_error_by_col[num_col] += 1
                                    print("! lin {} col {} Maxi-length error: '{}' exceeds {} length".format(cnt_lines, num_col, str_val, dic_fmt['maxi_len']))

                        # Maximum value
                        if not bol_err_in_this_line:  # i.e. No errors so far, in this line
                            if 'maxi_val' in dic_fmt.keys() and dic_fmt['datatype'].lower() in ('integer', 'float'):
                                if float(str_val) <= float(dic_fmt['maxi_val']):
                                    pass
                                else:
                                    bol_err_in_this_line = True
                                    lst_error_by_col[num_col] += 1
                                    print("! lin {} col {} Maxi-value error: '{}' exceeds {} value".format(cnt_lines, num_col, str_val, dic_fmt['maxi_val']))

                    # Maximum precession
                    if not bol_err_in_this_line:  # i.e. No errors so far, in this line
                        if 'precessi' in dic_fmt.keys() and dic_fmt['datatype'].lower() in ('float'):
                            if len(str_val.split('.')[1]) <= float(dic_fmt['precessi']):
                                pass
                            else:
                                bol_err_in_this_line = True
                                lst_error_by_col[num_col] += 1
                                print("! lin {} col {} Maxi-precession error: '{}' exceeds {} decimals".format(cnt_lines, num_col, str_val, dic_fmt['precessi']))

                    # Illegal no-data occurrences
                    if True: # not bol_err_in_this_line):  # i.e. No errors so far, in this line
                        if 'nullable' in dic_fmt.keys():
                            ##print "\t", dic_fmt['nullable'], "|"+str_val+"|"
                            if dic_fmt['nullable'] == True or str_val != str_noda:
                                pass
                            else:
                                bol_err_in_this_line = True
                                lst_error_by_col[num_col] += 1
                                print("! lin {} col {} Nullable error: No-data value in non-nullable column.".format(cnt_lines, num_col, str_val))

            # register progress
            cnt_lines += 1
            if cnt_lines%100000 == 0:
                print("line: {}".format(cnt_lines))

    dic_ret['num_lines'] = cnt_lines
    dic_ret['err_by_col'] = lst_error_by_col

    return dic_ret

if __name__ == '__main__':

    # Read CLI parameters
    if len(sys.argv) > 2:
        str_fn_i_name = sys.argv[1] # Assume this to be the .csv file
        str_fn_f_name = sys.argv[2] # Assume this to be the .ecffc file
    else:
        print("\n\tUsage: ec_csv_check.py demo_checker.csv demo_checker.ecffc")
        sys.exit(999)

    dic_form = load_format_file(str_fn_f_name)

    dic_anal = scan_data_file(str_fn_i_name, dic_form)

    # Summarize error statistics...
    print("\nNumber of Errors in {} lines: {}, \n  by column = {}".format(dic_anal['num_lines'], sum(dic_anal['err_by_col']), dic_anal['err_by_col']))

    print("Done...")
