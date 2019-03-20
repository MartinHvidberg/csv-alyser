
import datetime

str_fn_i = r"/home/martin/Work/AIS_DK/aisdk_20190208_samp.csv"
#eklagerstr_fn_i = r"/home/martin/Work/AIS_DK/aisdk_20190208.csv"
str_fn_o = r"/home/martin/Work/AIS_DK/aisdk_20190208_samp_cln.csv"

def cln_ais_line(line):
    str_ret = ''

    # 1 Expect date
    t1, rest = line.split(',', 1)
    try:
        dtt1 = datetime.datetime.strptime(t1, "%d/%m/%Y %H:%M:%S")  # e.g. 08/02/2019 00:01:04
        str_ret += dtt1.isoformat()
    except ValueError as e:
        print("ValueError: {}".format(e))
        return None

    # 2 Expect Class
    t2, rest = rest.split(',', 1)
    if t2 in ['Class A', 'Class B', 'Base Station', 'AtoN']:
        str_ret += ',' + t2
    else:
        print("Unexpected AIS Class: {}".format(t2))

    # 3 Expect MMSI
    t3, rest = rest.split(',', 1)
    try:
        imsi = int(t3)
        str_ret += ',' + str(imsi)
    except ValueError as e:
        print("ValueError: {}".format(e))
        return None

    # 4, 5 Expect Lat, Lon
    t4, t5, rest = rest.split(',', 2)
    try:
        lat_dd = float(t4)
        lon_dd = float(t5)
        str_ret += ',' + str(lat_dd) + ',' + str(lon_dd)
    except ValueError as e:
        print("ValueError: {}".format(e))
        return None

    # 6 Expect MMSI
    t6, rest = rest.split(',', 1)
    if t6 in ['Under way using engine', 'Under way sailing',
              'Engaged in fishing',
              'Moored', 'At anchor',
              'Constrained by her draught', 'Aground',
              'Restricted maneuverability', 'Not under command',
              'Reserved for future use [11]',
              'Reserved for future amendment [WIG]',
              'Reserved for future amendment [HSC]',
              'AIS-SART',
              'Unknown value']:
        str_ret += ',' + t6
    else:
        print("Unexpected Navigational Status: {}".format(t6))

    # 7 ROT
    t7, rest = rest.split(',', 1)
    if t7 != '':
        try:
            rot = float(t7)
            str_ret += ',' + str(rot)
        except ValueError as e:
            print("ValueError: {}".format(e))
            return None
    else:
        str_ret += ','

    # 8 Expect SOG
    t8, rest = rest.split(',', 1)
    if t8 != '':
        try:
            sog = float(t8)
            str_ret += ',' + str(sog)
        except ValueError as e:
            print("ValueError: {}".format(e))
            return None
    else:
        str_ret += ','

    # 9 Expect COG
    t9, rest = rest.split(',', 1)
    if t9 != '':
        try:
            cog = float(t9)
            str_ret += ',' + str(cog)
        except ValueError as e:
            print("ValueError: {}".format(e))
            return None
    else:
        str_ret += ','

    # 10 Expect Heading
    t10, rest = rest.split(',', 1)
    if t10 != '':
        try:
            heading = int(t10)
            str_ret += ',' + str(heading)
        except ValueError as e:
            print("ValueError: {}".format(e))
            return None
    else:
        str_ret += ','

    # 11 Expect IMO
    t11, rest = rest.split(',', 1)
    if t11 != 'Unknown':
        try:
            imo = int(t11)
            str_ret += ',' + str(imo)
        except ValueError as e:
            print("ValueError: {}".format(e))
            return None
    else:
        str_ret += ','

    # 12 Expect Callsign
    t12, rest = rest.split(',', 1)
    if t12 != '':
        if t12 == t12.upper() and len(t12) < 8:
            str_ret += ',' + t12
        else:
            print("Non-Upper, or very long, Callsign: {}".format(t12))
            return None
    else:
        str_ret += ','

    # 13 Expect Name
    if rest[0] == '"':
        t13, rest = rest[1:].split('"', 1)
        rest.lstrip(',')
    else:
        t13, rest = rest.split(',', 1)
    str_ret += ',' + t13.replace(',', '.')

    # 14 Expect Ship type
    t14, rest = rest.split(',', 1)
    if t14 in ['Passenger', 'Tanker', 'Cargo',
               'Fishing',
               'Pleasure', 'Sailing',
               'Dredging', 'Tug', 'Towing', 'Towing long/wide',
               'Port tender',
               'Diving',
               'Pilot', 'SAR', 'SAR Airborne',
               'Search and Rescue Transponder', 'Man Overboard Device',
               'Military', 'Law enforcement',
               'Anti-pollution', 'Medical',
               'Reserved', 'HSC', 'Not party to conflict',
               'WIG', 'Search and Rescue Transponder', 'SAR Airborne',
               '', 'Other', 'Undefined',
               'Spare 1', 'Spare 2', '"MARIE ASTRID"" ND115"', '"SPICA"""']:
        str_ret += ',' + t14
    else:
        print("Unexpected Ship type: {}".format(t14))

    return str_ret

if __name__ == '__main__':

    dic_typ = dict()
    with open(str_fn_o, 'w') as filo:
        num_lin = 0
        with open(str_fn_i, 'r') as filf:
            for line in filf:
                num_lin += 1
                if num_lin % 100000 == 0:
                    print(num_lin)
                str_ret = cln_ais_line(line)
                if str_ret:
                    filo.write(str_ret+'\n')
