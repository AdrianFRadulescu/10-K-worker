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


def is_cik(directory = '11111111'):
    """
        checks if a file's name is a cik or a company name
    :param directory:
    :return:
    """
    return all(map(lambda x: '0' <= x <= '9', directory)) and len(directory) == 10

if __name__ == "__main__":

    database_path = sys.argv[2]
    option = sys.argv[1]

    #cik_file_writer = csv.writer(cik_file, delimiter=',')

    if option == '-cik':

        if len(sys.argv) == 5 and sys.argv[4] == 'a':
            # rewrite file
            cik_table_file = open(sys.argv[2] + '/company_cik_table', "a")
            cik_file = open(sys.argv[2] + '/company_ciks.csv', "w")
        else:
            # append to table
            cik_table_file = open(sys.argv[2] + '/company_cik_table', "w")
            cik_file = open(sys.argv[2] + '/company_ciks.csv', "w")

        ciks = {}

        already_renamed_ciks = {}

        line_delim = "-" * (len("company") + 35 + 11 + 6) + "\n"

        if sys.argv[4] == 'a':

            # get all the directories that have already been renamed
            '''
            with open(sys.argv[2] + '/company_ciks.csv', 'r') as aux_cik_file:
                for cik in aux_cik_file.read().replace('\n', '').split(','):
                    already_renamed_ciks[cik] = True
            '''
            with open(sys.argv[2] + '/company_cik_table', 'r') as aux_cik_file:
                for content_line in aux_cik_file.read().split(line_delim)[1:]:
                    already_renamed_ciks[content_line.split('| ')[-1].replace('\n', '')] = True

        else:
            cik_table_file.write(15 * " " + "Company" + 27 * " " + "CIK" + "\n")
            cik_table_file.write(line_delim)

        for name_dir in sorted(os.listdir(database_path)):

            if os.path.isdir(database_path + '/' + name_dir) and len(os.listdir(database_path + '/' + name_dir)) != 0:
                print name_dir

                if name_dir in already_renamed_ciks:
                    ciks[name_dir] = database_path + '/' + name_dir
                    print 'directory already renamed, skipping'
                    continue

                if is_cik(name_dir):
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
                            if ciks[get_cik(fl)] not in map(lambda x: ciks[x], ciks):
                                print "not in ciks:"
                                print ciks[get_cik(fl)]
                                print ciks
                                print
                                print
                                os.mkdir(database_path + '/' + ciks[get_cik(fl)])
                            print "actual renaming"
                            print database_path + '/' + name_dir + '/' + fl  + '->>>>'
                            print database_path + '/' + get_cik(fl) + '/' + fl
                            print
                            print
                            os.rename(database_path + '/' + name_dir + '/' + fl, database_path + '/' + get_cik(fl) + '/' + fl)
                            print "rename successful"
                        except OSError:
                            print 'rename failed for:'
                            print database_path + '/' + name_dir + '/' + fl
                            print ciks[get_cik(fl)] + '/' + fl

                    # delete directory
                    if len(os.listdir(database_path + '/' + name_dir)) == 0 and not is_cik(name_dir):
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

        if database_path[-1] == '/':
            database_path= database_path[:-1]

        for cik_dir in os.listdir(database_path):

            if not is_cik(cik_dir):
                continue

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

            print "renaming files"
            pprint.pprint(companies)

            for comp in list(companies):

                print "renaming for company ", comp

                if not os.path.exists(database_path + '/' + comp):
                    os.mkdir(database_path + '/' + comp)

                for fl in companies[comp]:
                    try:
                        print "moving ", database_path + '/' + cik_dir + '/' + fl, " to ", database_path + '/' + comp
                        shutil.move(database_path + '/' + cik_dir + '/' + fl, database_path + '/' + comp)
                        #os.rename(database_path + '/' + list(companies)[0] + '/' + fl, database_path + '/' + comp + '/' + fl)
                    except OSError:
                        print "fail"

            shutil.rmtree(database_path + '/' + cik_dir)