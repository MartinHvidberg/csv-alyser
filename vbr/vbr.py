"""
Validate by Rules
Read a .csv (or .json) file
Convert each row to a dictionary, based on what's expected by the rules for the data set
Check each dictionary further for full compliance with the rules for the data set.
"""

import os
import csv
import datetime
import json


# CONSTANTS
INPUT_FILENAME = "./data/SacramentocrimeJanuary2006.csv"
#INPUT_FILENAME = "./data/SacramentocrimeJanuary2006.json"
DELIMITER = ','
QUOTECHAR = '"'


def obj_valid(obj_x):
    """ Examines a single object (dictionary), and check if it is valid according to all rules
    assuming data is valid until proven in-valid"""
    # Overall checks
    if not isinstance(obj_x, dict):
        print("Warning: Object is not a Dictionary but a: {}".format(str(type(obj_x))))
        return False
    if not len(obj_x.keys()) == 9:
        print("Warning: Object bo not seem to have the correct number of keys: {}".format(obj_x))
        return False
    lst_expected_keys = ["cdatetime","address","district","beat","grid","crimedescr","ucr_ncic_code","latitude","longitude"]
    if not all([tok in obj_x.keys() for tok in lst_expected_keys]):
        print("Warning: A mandatory key seems to be missing: {}".format(obj_x.keys()))
        return False
    # Check cdatetime as datetime
    cdatetime = obj_x['cdatetime']
    str_expected_format = '%m/%d/%y %H:%M'
    try:
        dtt_x = datetime.datetime.strptime(cdatetime, str_expected_format)
    except ValueError:
        print("Date seems to be mall formatted. input: {} don't match: {}".format(cdatetime, str_expected_format))
    # Check district is number
    district = obj_x['district']
    try:
        int_x = int(district)
    except ValueError:
        print("Warning: Value for 'destrict' seems to be non-integer: {}".format(district))
        return False
    # Check Lat/Lon
    lat = obj_x['latitude']
    lon = obj_x['longitude']
    try:
        flo_lat = float(lat)
        flo_lon = float(lon)
    except ValueError:
        print("Warning: Value for 'latitude' or 'longitude' seems to be non-float: {}, {}".format(lat, lon))
        return False
    if flo_lat < -90 or flo_lat > 90:
        print("Warning: Value for 'latitude' seems to be out of legal range: {}".format(flo_lat))
        return False
    if flo_lon < -180 or flo_lon > 180:
        print("Warning: Value for 'longitude' seems to be out of legal range: {}".format(flo_lon))
        return False
    # All checks completed - No problems found ...
    return True


def read_csv_file(str_fn):
    """ reads through a .csv file and turn each line into a valid object, i.e. a dict()
    Warnings are printed in case of invalid objects in the input
    Return: a list of valid objects """

    def dic_from_list(lst_i, lst_h):
        """ Takes a list of values, and a list of headers and return a dictionary """
        dic_ret = dict()  # Initialising the return object
        if all([isinstance(tok, list) for tok in [lst_i, lst_h]]):
            if len(lst_i) == len(lst_h):
                for n in range(len(lst_h)):
                    dic_ret[lst_h[n]] = lst_i[n]
            else:
                print("Warling: Line do not seem to have same length as header: {}".format(lst_i))
        else:
            print("Warning: Either the header or the line is not a list: {} {}".format(lst_h, lst_i))
        return dic_ret

    lst_ret = list()  # Initialising return object
    try:
        with open(str_fn, 'r') as fil_in:
            csv_reader = csv.reader(fil_in, delimiter=DELIMITER, quotechar=QUOTECHAR)
            num_cnt = 0  # Initialise row counter
            for row in csv_reader:
                num_cnt += 1
                if num_cnt == 1:  # It's the header line
                    lst_header = row
                else:  # It's a real data line
                    dic_in = dic_from_list(row, lst_header)
                    if obj_valid(dic_in):
                        lst_ret.append(dic_in)
                    else:
                        print("Warning: Line: {} seems to be invalid: {}".format(num_cnt, row))
    except FileNotFoundError as e:
        print("Err: File not found. OS says: {}".format(e))
    return lst_ret


def read_json_file(str_fn):
    """ Read a .json file
    Expect to find a list of dictionaries
    Remove first and last line - as they are known to be dispensable """
    lst_ret = list()  # Initialising return object
    with open(str_fn) as fil_json:
        data = fil_json.readlines()
    data = data[1:-1]  # Loose first and last line in file
    json_data = json.loads(' '.join(data))
    for dic_in in json_data:
        if obj_valid(dic_in):
            lst_ret.append(dic_in)
        else:
            print("Warning: Record seems to be invalid: {}".format(dic_in))
    return lst_ret


def read_ascii_file(str_filename):
    """ Determine the type of ascii file, and call the appropriate reader """
    if str_filename.endswith('.csv'):
        return read_csv_file(str_filename)
    elif str_filename.endswith('.json'):
        return read_json_file(str_filename)
    else:
        print("Err: Unknown file type: {}".format(str_filename.rsplit(os.sep, 1)))
        return list()


def main(str_filename):
    lst_objects = read_ascii_file(str_filename)
    print("Number of records found in file: {}".format(len(lst_objects)))


if __name__ == '__main__':
    main(INPUT_FILENAME)
