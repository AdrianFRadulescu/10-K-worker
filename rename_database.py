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

    #cik_file_writer = csv.writer(cik_file, delimiter=',')

    if option == '-cik':

        if len(sys.argv) == 5 and sys.argv[4] == 'a':
            # rewrite file
            cik_table_file = open(sys.argv[2] + '/company_cik_table', "a")
            cik_file = open(sys.argv[2] + '/company_ciks.csv', "a")
        else:
            # append to table
            cik_table_file = open(sys.argv[2] + '/company_cik_table', "w")
            cik_file = open(sys.argv[2] + '/company_ciks.csv', "w")

        ciks = {}

        already_renamed_ciks = {}

        line_delim = "-" * (len("company") + 35 + 11 + 6) + "\n"
        if sys.argv[4] == 'a':

            # get all the directories that have already been renamed
            with open(sys.argv[2] + '/company_ciks.csv', 'r') as aux_cik_file:
                #print aux_cik_file.read().replace('\n', '')
                for cik in aux_cik_file.read().replace('\n', '').split(','):
                    already_renamed_ciks[cik] = True
        else:
            cik_table_file.write(15 * " " + "Company" + 27 * " " + "CIK" + "\n")
            cik_table_file.write(line_delim)

        for name_dir in sorted(os.listdir(database_path)):

            if os.path.isdir(database_path + '/' + name_dir) and len(os.listdir(database_path + '/' + name_dir)) != 0:
                print name_dir

                if name_dir in already_renamed_ciks:
                    print 'directory already renamed, skipping'
                    continue

                print get_cik(os.listdir(database_path + '/' + name_dir)[0])

                if get_cik(os.listdir(database_path + '/' + name_dir)[0]) == name_dir:
                    ciks[name_dir] = database_path + '/' + name_dir
                    print '--'

                print get_cik(os.listdir(database_path + '/' + name_dir)[0]) in ciks

                cik_table_file.write(
                    get_file_company(os.listdir(database_path + '/' + name_dir)[0]) + (42 - len(get_file_company(os.listdir(database_path + '/' + name_dir)[0]))) * " " + "|" + " " + get_cik(os.listdir(database_path + '/' + name_dir)[0]) + "\n"
                )
                cik_table_file.write(line_delim)

                if get_cik(os.listdir(database_path + '/' + name_dir)[0]) in ciks:

                    print 'encountered directory with already registered cik'

                    # move files in this directory to the directory with already registerd cik
                    for fl in os.listdir(database_path + '/' + name_dir):
                        print database_path + '/' + name_dir + '/' + fl
                        try:
                            print "trying to rename ", get_cik(fl), " " + fl
                            os.rename(database_path + '/' + name_dir + '/' + fl, ciks[get_cik(fl)] + '/' + fl)
                            print "rename successful"
                        except OSError:
                            print 'rename failed for:'
                            print database_path + '/' + name_dir + '/' + fl
                            print ciks[get_cik(fl)] + '/' + fl

                    # delete directory
                    shutil.rmtree(database_path + '/' + name_dir)
                    # os.remove(database_path + '/' + dir)

                else:
                    ciks[get_cik(os.listdir(database_path + '/' + name_dir)[0])] = database_path + '/' + get_cik(
                        os.listdir(database_path + '/' + name_dir)[0])
                    os.rename(database_path + '/' + name_dir, database_path + '/' + get_cik(os.listdir(sys.argv[2] + '/' + name_dir)[0]))

        # write the file with all the ciks
        for cik in list(ciks):
            cik_file.write(cik + ',\n')

        pprint.pprint(ciks)

    elif option == '-names':

        for cik_dir in os.listdir(database_path):
            if not os.path.isdir(database_path + '/' + cik_dir):
                print cik_dir
                continue

            # get all different companies that are in current directory and their files

            companies = {}

            for fl in os.listdir(database_path + '/' + cik_dir):
                if get_file_company(fl) in companies:
                    companies[get_file_company(fl)] += [fl]
                else:
                    companies[get_file_company(fl)] = [fl]

            # rename current file with the first name in the dictionary

            try:
                print "renaming ", cik_dir, " to ", list(companies)[0]
                os.rename(database_path + '/' + cik_dir, database_path + '/' + list(companies)[0])
                print "successful renaming"
            except OSError:
                print "fail"

            print "renaming other files if any"

            for comp in list(companies)[1:]:

                for fl in companies[comp]:
                    try:
                        print "renaming ", fl, " to ",
                        os.rename(database_path + '/' + list(companies)[0] + '/' + fl, database_path + '/' + comp + '/' + fl)
                    except OSError:
                        print "fail"

            '''
            for fl in os.listdir(database_path + '/' + cik_dir):
                company_name = get_file_company(fl)
                print fl, '-->>', company_name
                print database_path + '/' + cik_dir + '/' + fl, " to ", database_path + '/' + company_name + '/' + fl
                os.rename(database_path + '/' + cik_dir, database_path + '/' + company_name)
            '''
