
import os
import sys
import csv

str_root_dir = r"../data"

def csv_2_lod(ffn):
    lst_ret = list()
    with open(ffn) as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        num_row = 0
        for row in spamreader:
            dic_ret = dict()
            row = [bar.strip() for bar in row]
            num_row += 1
            if num_row == 1:  # Header
                if all([tok in [itm.strip() for itm in row] for tok in ['id', 'alias', 'time', 'name']]):
                    lst_pos = list()
                    lst_pos.append(row.index('id'))
                    lst_pos.append(row.index('name'))
                    lst_pos.append(row.index('alias'))
                    lst_pos.append(row.index('time'))
                    ##print(lst_pos)
                else:
                    print("incomplete header: {}".format(row))
                    break
            else:  # data line
                try:
                    dic_ret['id'] = row[lst_pos[0]]
                    dic_ret['name'] = row[lst_pos[1]]
                    dic_ret['alias'] = row[lst_pos[2]]
                    dic_ret['time'] = row[lst_pos[3]]
                except IndexError:
                    print("Line don't match header: {}".format(row))
                    continue
                ##print(dic_ret)
                lst_ret.append(dic_ret)
    return lst_ret


def fill_missing_w_previous(lod_in, fld_f, miss=''):
    lst_ret = list()
    val_latest = miss
    for dic_in in lod_in:
        if fld_f not in dic_in.keys():
            dic_in[fld_f] = None
        if dic_in[fld_f] == miss:
            dic_in[fld_f] = val_latest
        else:
            val_latest = dic_in[fld_f]
        lst_ret.append(dic_in)
    return lst_ret


def split_lod_by_field(lod_in, fld_in):  #  XXX <----------------------------------- It dosn't split s...
    ##print("lod_in: {} {}".format(str(type(lod_in)), lod_in))
    dic_ret = dict()
    for itm in lod_in:
        if fld_in in itm.keys():
            if itm[fld_in] not in dic_ret.keys():
                dic_ret[itm[fld_in]] = list()
            dic_ret[itm[fld_in]].append(itm)
        else:
            print("Warning in split_lod_by_field() Field: '{}' not in dic.".format(fld_in))
    lst_ret = list()
    for key_ou in dic_ret.keys():
        lst_ret.append(dic_ret[key_ou])
    return lst_ret


def list_minmax_per_name():
    pass


for (dirpath, dirs, files) in os.walk(str_root_dir):
    for filename in files:
        if filename.endswith('.csv') and filename.startswith('jo'):
            print(filename)
            lod_data = csv_2_lod(dirpath + os.sep + filename)
            print(lod_data)
            lod_data = fill_missing_w_previous(lod_data, 'name', miss='')
            print(lod_data)
            lol_data = split_lod_by_field(lod_data, 'name')
            print(lod_data)
            lst_mima = list_minmax_per_name(lol_data)