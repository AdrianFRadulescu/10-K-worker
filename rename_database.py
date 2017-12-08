"""
    This is a separate mini-script for renaming the files folders/directories in the
    current database

    Main options are:
    -cik    converts the names of the companies in the database to their CIKs
    -names  converts the cik from the database to their company names

"""

import os
import sys
import csv
import pprint
import shutil

from file_word_counting import get_cik
from file_word_counting import get_file_company

if __name__ == "__main__":

    database_path = sys.argv[2]
    option = sys.argv[1]

    cik_table_file = open(sys.argv[2] + '/company_cik_table', "w")
    cik_file = open(sys.argv[2] + '/company_ciks.csv', "w")
    #cik_file_writer = csv.writer(cik_file, delimiter=',')

    if option == '-cik':

        ciks = {}

        cik_table_file.write(15 * " " + "Company" + 27 * " " + "CIK" + "\n")
        line_delim = "-"*(len("company") + 35 + 11 + 6) + "\n"
        cik_table_file.write(line_delim)

        for dir in sorted(os.listdir(database_path)):

            if os.path.isdir(database_path + '/' + dir) and len(os.listdir(database_path + '/' + dir)) != 0:
                print dir
                print get_cik(os.listdir(database_path + '/' + dir)[0])

                if get_cik(os.listdir(database_path + '/' + dir)[0]) == dir:
                    ciks[dir] = database_path + '/' + dir
                    print '--'

                pprint.pprint(ciks)
                print get_cik(os.listdir(database_path + '/' + dir)[0]) in ciks

                cik_table_file.write(
                    get_file_company(os.listdir(database_path + '/' + dir)[0]) + (42 - len(get_file_company(os.listdir(database_path + '/' + dir)[0]))) * " " + "|" + " " + get_cik(os.listdir(database_path + '/' + dir)[0]) + "\n"
                )
                cik_table_file.write(line_delim)

                if get_cik(os.listdir(database_path + '/' + dir)[0]) in ciks:

                    # move files in this directory to the directory with already registerd cik
                    for fl in os.listdir(database_path + '/' + dir):
                        print database_path + '/' + dir + '/' + fl
                        print ciks[get_cik(fl)] + '/' + fl
                        try:
                            os.rename(database_path + '/' + dir + '/' + fl, ciks[get_cik(fl)] + '/' + fl)
                        except OSError:
                            print database_path + '/' + dir + '/' + fl
                            print ciks[get_cik(fl)] + '/' + fl

                    # delete directory
                    shutil.rmtree(database_path + '/' + dir)
                    # os.remove(database_path + '/' + dir)

                else:
                    ciks[get_cik(os.listdir(database_path + '/' + dir)[0])] = database_path + '/' + get_cik(
                        os.listdir(database_path + '/' + dir)[0])
                    os.rename(database_path + '/' + dir, database_path + '/' + get_cik(os.listdir(sys.argv[2] + '/' + dir)[0]))

        # write the file with all the ciks
        for cik in list(ciks):
            cik_file.write(cik + ',\n')


    elif option == '-names':

        for dir in os.listdir(database_path):
            if not os.path.isdir(database_path + '/' + dir):
                print dir
                continue
            company_name = get_file_company(os.listdir(database_path + '/' + dir)[0])
            print company_name, os.listdir(database_path + '/' + dir)[0]
            os.rename(database_path + '/' + dir, database_path + '/' + company_name)

