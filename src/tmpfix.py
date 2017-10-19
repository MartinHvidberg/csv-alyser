

if __name__ == '__main__':

    # Hardcoded - to be later converted to command line parameters
    str_filei_name = "/home/martin/MEGA/Snaps_HDD/DATA/Forekomster/GBIF_org/0010573-170714134226665.csv"
    str_fileo_name = "/home/martin/MEGA/Snaps_HDD/DATA/Forekomster/GBIF_org/0010573-170714134226665f.csv"

    cnt_lines = 0
    with open(str_filei_name, 'r') as fili:
        with open(str_fileo_name, 'w') as filo:
            for line in fili:
                if '735860780' in line:
                    lino = line.replace('"','')
                    print "FIXED:"
                    print "<<<", line
                    print ">>>", lino
                else:
                    lino = line
                filo.write(lino)
                cnt_lines += 1
                if cnt_lines%100000 == 0:
                    print "line:", cnt_lines

    print "Done {} lines...".format(cnt_lines)
