"""
    The main file connecting all the scripts
"""
#!/usr/bin/python

import sys
import csv
import platform


def extract_args(argv=[]):

    fargs = {}
    fargs['defcat'] = True

    index = 1
    while index < len(argv):
        if argv[index][0] is '-':
            # there is an option to be configured
            if argv[index] == '-rdir':
                fargs['rdir'] = argv[index + 1]

            elif argv[index] == '-comp':
                fargs['comp'] = argv[index + 1].replace('-', ' ')

            elif argv[index] == '-categs':
                fargs['categs'] = argv[index + 1]
                fargs['defcat'] = False

            elif argv[index] == '-wdir':
                fargs['wdir'] = argv[index + 1]

            elif argv[index] == '-refined':
                fargs['refined'] = argv[index + 1]

            elif argv[index] == '-nw':
                result = []
                current_word = ''
                for ch in list(argv[index + 1])[1:]:

                    if ch.isalpha():
                        current_word += ch

                    else:
                        result += [current_word]
                        current_word = ''

                fargs['nw'] = result

            elif argv[index] == '-rmr':
                fargs['rmr'] = int(argv[index + 1])

            elif argv[index] == '-t':
                fargs['t'] = argv[index + 1]

            elif argv[index] == '-ewdir':
                fargs['ewdir'] = argv[index + 1]

            elif argv[index] == '-y':
                fargs['y'] = int(argv[index + 1])

            elif argv[index] == '-fy':
                fargs['fy'] = int(argv[index + 1])

            elif argv[index] == '-ly':
                fargs['ly'] = int(argv[index + 1])

            elif argv[index] == '-csv':
                fargs['csv'] = argv[index + 1]

            elif argv[index] == '-i':
                fargs['i'] = argv[index + 1]

            elif argv[index] == '-csvwdir':
                fargs['csvwdir'] = argv[index + 1]

            elif argv[index] == '-csvrf':
                fargs['csvrf'] = argv[index + 1]

            elif argv[index] == '-rblkcsv':
                fargs['rblkcsv'] = argv[index + 1]

            elif argv[index] == '-ccount':
                fargs['ccount'] = int(argv[index + 1])

            elif argv[index] == '-sdir':
                fargs['sdir'] = argv[index + 1]

            elif argv[index] == '-ddir':
                fargs['ddir'] = argv[index + 1]

            elif argv[index] == '-csvstf':
                fargs['csvstf'] = 'csvstf'

            elif argv[index] == '-comps':
                if '[' and ']' in argv[index + 1]:
                    fargs['comps'] = argv[index + 1][1:-1].split(',')
                else:
                    with open(argv[index + 1]) as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        fargs['comps'] = []
                        for line in reader:
                            fargs['comps'] += line
                print fargs['comps']

            elif argv[index] == '-c_item7':
                fargs['c_item7'] = argv[index + 1]

            elif argv[index] == '-csvfile':
                fargs['csvrf'] = argv[index + 1].split('/')[-1]
                fargs['csvwdir'] = (argv[index + 1][:-len(argv[index + 1].split('/')[-1])])[:-1]

        index += 1

    return fargs


def main(argv):

    if argv == []:
        return
    print argv
    print 'extracting args'
    if argv[0] == '-h':

        if len(argv) is 1:

            print
            print 'In order to avoid errors please make sure that the arguments given to the script'
            print 'are all valid and in the right format'
            print
            print
            print 'The company folders(containing the 10-Ks for each company) should be kept in the same folder as the ' \
                  'names.csv file which keeps track of the files in the Edgar database'
            print 'For downloading new files(from the last years) updating the names.csv files is required before the actual download'
            print 'For automatically downloading the modules run main.py -i'
            print

            print 'main.py -h <option>  -information only on a particular action of the script'

        elif argv[1] == '-rf':

            print 'main.py -rf -rdir <read_directory> -comp <company_name> -categs <category_dictionary_file> '
            print '-wdir <write_directory> -refined <true/false> -nw <negative_words_list> -rmr <remove_range>'
            print '-t <report_type> -ewdir <excel_write_directory> -y <year>'
            print
            print 'main.py -rf         -make a report for a given file'
            print '        -rdir       -the parent directory where the database of files is located'
            print '        -comp       -the company to which the file belongs to '
            print '                     name must be given exactly as it appears in the folder that contains all the files'
            print '                     with "\\" put in front of the spaces between words'
            print '        -categs     -the file that contains the categories and the words belonging to them'
            print '                     it must be a .pkl file '
            print '        -wdir       -the directory where the report should be writen for basic type reports'
            print '        -refined    -"true" if the report is to be a refined one or "false" otherwise'
            print '        -nw         -a list of the negative words that need to be provided in case of a refined report'
            print '                     needs to be given in the format [nw1,nw2,nw3,nw4,...] with no spaces in between'
            print '        -rmr        -the range in which words appearing after a negative one are removed. 2 By default'
            print '        -t          -the type of the report: "excel" for an excel report and "raw" otherwise '
            print '        -ewdir      -the directory in which the excel type reports will be written'
            print '        -csvwdir    -the directory in which the csv type reports will be writen'
            print '        -csvrf      -the file where the csv report has to be written'
            print '        -y          -the year of the file'
            print
            print

            print 'All option arguments should be inserted in full paths, if one of the directories contains a " "' \
                  ' in its name and "\\" has to be inserted before it.\n' \
                  'For example if the name is "Zoro Corp" then the argument whould be "Zoro\ Corp"'
            print 'In order to specify the current directory in an unix based system(mac or linux) ' \
                  'type "." as argument for "rdir" or "wdir"'

            print 'For this option a report for the file will also be printed on the commandline'
            print 'Here is a sample report:'
            print
            print '         CRE          |          COM          |          COL          |          CON   '
            print '-----------------------------------------------------------------------------------------------'
            print '      origin:8        |       agreem:61       |        help:4         |      control:29'
            print '-----------------------------------------------------------------------------------------------'
            print '       creat:8        |      excellen:4       |       people:0        |       engag:12         '
            print '-----------------------------------------------------------------------------------------------'
            print '     discontin:1      |      revenue:12       |      certain:20       |        life:5         '
            print
            print

        elif argv[1] == '-rc':

            print 'main.py -rc -rdir <read_directory> -comp <company_name> -categs <category_dictionary_file> '
            print '-wdir <write_directory> -refined <true/false> -nw <negative_words_list> -rmr <remove_range>'
            print '-t <report_type> -ewdir <excel_write_directory>'
            print
            print 'main.py -rc          -make a report for a company'
            print '        -rdir       -the parent directory where the database of files is located'
            print '        -comp       -the company to which the file belongs to '
            print '                     name must be given exactly as it appears in the folder that contains all the files'
            print '                     with "\\" put in front of the spaces between words'
            print '        -categs     -the file that contains the categories and the words belonging to them'
            print '                     it must be a .pkl file '
            print '        -wdir       -the directory where the report should be writen for basic type reports'
            print '        -refined    -"true" if the report is to be a refined one or "false" otherwise'
            print '        -nw         -a list of the negative words that need to be provided in case of a refined report'
            print '                     needs to be given in the format [nw1,nw2,nw3,nw4,...] with no spaces in between'
            print '        -rmr        -the range in which words appearing after a negative one are removed'
            print '        -t          -the type of the report: "excel" for an excel report and "raw" otherwise '
            print '        -ewdir      -the directory in which the excel type reports will be written'
            print '        -csvwdir    -the directory in which the csv type reports will be writen'
            print '        -csvrf      -the file where the csv report has to be written'
            print
            print

            print 'All option arguments should be inserted in full paths, if one of the directories contains a " "' \
                  ' in its name and "\\" has to be inserted before it.\n' \
                  'For example if the name is "Zoro Corp" then the argument whould be "Zoro\ Corp"'
            print 'In order to specify the current directory in an unix based system(mac or linux) ' \
                  'type "." as argument for "rdir" or "wdir"'

        elif argv[1] == '-rcy':

            print 'main.py -rcy -rdir <read_directory> -comp <company_name> -categs <category_dictionary_file> '
            print '-wdir <write_directory> -refined <true/false> -nw <negative_words_list> -rmr <remove_range>'
            print '-t <report_type> -ewdir <excel_write_directory> -fy <first_year> -ly <last_year>'
            print
            print 'main.py -rcy'
            print '        -rdir       -the parent directory where the database of files is located'
            print '        -comp       -the company to which the file belongs to '
            print '                     name must be given exactly as it appears in the folder that contains all the files'
            print '                     with "\\" put in front of the spaces between words'
            print '        -categs     -the file that contains the categories and the words belonging to them'
            print '                     it must be a .pkl file '
            print '        -wdir       -the directory where the report should be writen for basic type reports'
            print '        -refined    -"true" if the report is to be a refined one or "false" otherwise'
            print '        -nw         -a list of the negative words that need to be provided in case of a refined report'
            print '                     needs to be given in the format [nw1,nw2,nw3,nw4,...] with no spaces in between'
            print '        -rmr        -the range in which words appearing after a negative one are removed'
            print '        -t          -the type of the report: "excel" for an excel report and "raw" otherwise '
            print '        -ewdir      -the directory in which the excel type reports will be written'
            print '        -csvwdir    -the directory in which the csv type reports will be writen'
            print '        -csvrf      -the file where the csv report has to be written'
            print '        -fy         -the starting year which the report on the company has to include'
            print '        -ly         -the ending year which the report on the company has to include'
            print
            print

            print 'All option arguments should be inserted in full paths, if one of the directories contains a " "' \
                  ' in its name and "\\" has to be inserted before it.\n' \
                  'For example if the name is "Zoro Corp" then the argument whould be "Zoro\ Corp"'
            print 'In order to specify the current directory in an unix based system(mac or linux) ' \
                  'type "." as argument for "rdir" or "wdir"'
            print 'Example:'
            print 'python main.py -rcy -rdir "/Users/adrian_radulescu1997/Documents/Uni-Courses/DBPartTimeJob/crawler/utility_tests" ' \
                  '-csvwdir csv_test -nw [no,none,not,useless,unless,less,unnecessary] -comp 0000320193 -t csv -csvrf test4.csv -fy 1994 -ly 2016 -ccount 0'

        elif argv[1] == '-rcsy':

            print 'main.py -rcsy -rdir <read_directory> -comp <company_name> -categs <category_dictionary_file> '
            print '-wdir <write_directory> -refined <true/false> -nw <negative_words_list> -rmr <remove_range>'
            print '-t <report_type> -ewdir <excel_write_directory> -fy <first_year> -ly <last_year>'
            print
            print 'main.py -rcsy'
            print '        -rdir       -the parent directory where the database of files is located'
            print '        -comps       -the companies that are to be reported, the argument must be given as a list in the format "[c1,c2,c3,c4,...]"'
            print '                     name must be given exactly as it appears in the folder that contains all the files'
            print '                     with "\\" put in front of the spaces between words'
            print '        -categs     -the file that contains the categories and the words belonging to them'
            print '                     it must be a .pkl file '
            print '        -wdir       -the directory where the report should be writen for basic type reports'
            print '        -refined    -"true" if the report is to be a refined one or "false" otherwise'
            print '        -nw         -a list of the negative words that need to be provided in case of a refined report'
            print '                     needs to be given in the format [nw1,nw2,nw3,nw4,...] with no spaces in between'
            print '        -rmr        -the range in which words appearing after a negative one are removed'
            print '        -t          -the type of the report: "excel" for an excel report and "raw" otherwise '
            print '        -ewdir      -the directory in which the excel type reports will be written'
            print '        -csvwdir    -the directory in which the csv type reports will be writen'
            print '        -csvrf      -the file where the csv report has to be written'
            print '        -fy         -the starting year which the report on the company has to include'
            print '        -ly         -the ending year which the report on the company has to include'
            print '        -defcat     -True if the default categories are to be used, False otherwise'
            print
            print

            print 'All option arguments should be inserted in full paths, if one of the directories contains a " "' \
                  ' in its name and "\\" has to be inserted before it.\n' \
                  'For example if the name is "Zoro Corp" then the argument whould be "Zoro\ Corp"'
            print 'In order to specify the current directory in an unix based system(mac or linux) ' \
                  'type "." as argument for "rdir" or "wdir"'
            print 'Example:'
            print "python main.py -rcsy -rdir '/Users/adrian_radulescu1997/Documents/Uni-Courses/DBPartTimeJob/crawler/utility_tests'  " \
                  "-csvwdir csv_test -nw [no,none,not,useless,unless,less,unnecessary] -comps /Users/adrian_radulescu1997/Documents/Uni-Courses/DBPartTimeJob/crawler/comps.csv  " \
                  "-t csv -csvrf test6.csv -fy 1994 -ly 2016 -ccount 0 -defcat False -categs '/Users/adrian_radulescu1997/Documents/Uni-Courses/DBPartTimeJob/crawler/Culture type Bag of words.ctg'"

            """
                Make it take a .csv file instead of a list

            """

        elif argv[1] == '-ud':

            print 'main.py -ud -wdir <write_directory>'
            print
            print 'Configuration options:'
            print 'main.py -ud         -updates the edgar database register file'
            print '        -wdir       -the directory where the names.csv file representing the informations on the files '
            print '                    -in the Edgar database will be stored'
            print
            print

            print 'All option arguments should be inserted in full paths, if one of the directories contains a " "' \
                  ' in its name and "\\" has to be inserted before it.\n' \
                  'For example if the name is "Zoro Corp" then the argument whould be "Zoro\ Corp"'
            print 'In order to specify the current directory in an unix based system(mac or linux) ' \
                  'type "." as argument for "rdir" or "wdir"'

        elif argv[1] == '-uf':

            print 'main.py -uf -wdir <write_directory> -csv <csv_register_file> -comp <company_name>'
            print

            print 'main.py -uf         -updates the edgar 10-K files contained in the database(downloads missing or new files)'
            print '        -wdir       -the directory where the downloaded files will be stored'
            print '        -csv        -the .csv register file which the script uses in order to download 10-K files'
            print '        -comp       -the name of the company for which the files need to be updated/downloaded'
            print '                     has to be written in capital letters'
            print '        -t          -alphabetical threshold'
            print
            print

            print 'For exaample:'
            print 'python main.py -uf -wdir "quick_test" -csv /Volumes/Seagate\ Backup\ Plus\ Drive/DBPartTime/SEC-Edgar-data/name.csv -t "Questar Corp"'
            print 'will download all the 10-K files for the companies whose names are after "Questar Corp" in alphabetical order'
            print
            print

            print 'All option arguments should be inserted in full paths, if one of the directories contains a " "' \
                  ' in its name and "\\" has to be inserted before it.\n' \
                  'For example if the name is "Zoro Corp" then the argument whould be "Zoro\ Corp"'
            print 'In order to specify the current directory in an unix based system(mac or linux) ' \
                  'type "." as argument for "rdir" or "wdir"'

        elif argv[1] == '-rblkcsv':

            print 'main.py -rblkcsv -rdir <read_directory> -comp <company_name> -categs <category_dictionary_file> '
            print '-wdir <write_directory> -refined <true/false> -nw <negative_words_list> -rmr <remove_range>'
            print '-t <report_type> -ewdir <excel_write_directory> -fy <first_year> -ly <last_year> -csvrf <csv_report_file>' \
                  ' -csvwdir <csv_write_dir>'
            print
            print 'main.py -rblkcsv'
            print '        -rdir       -the parent directory where the database of files are located'
            print '                     with "\\" put in front of the spaces between words'
            print '                     it must be a .pkl file '
            print '        -nw         -a list of the negative words that need to be provided in case of a refined report'
            print '                     needs to be given in the format [nw1,nw2,nw3,nw4,...] with no spaces in between'
            print '        -rmr        -the range in which words appearing after a negative one are removed'
            print '        -t          -the type of the report: "excel" for an excel report and "raw" otherwise '
            print '        -csvwdir    -the directory in which the csv type reports will be writen'
            print '        -csvrf      -the file where the csv report has to be written'
            print '        -fy         -the starting year which the report on the company has to include'
            print '        -ly         -the ending year which the report on the company has to include'
            print '        -ccount     -the number of companies that have already been processed by the script'
            print
            print 'For example:'
            print 'python main.py -rblkcsv -rdir "/Volumes/Seagate Backup Plus Drive/DBPartTime/SEC-Edgar-data" -csvwdir csv_test -nw [no,none,not,useless,unless,less,unnecessary] -t csv -csvrf test1.csv -fy 1994 -ly 2016 -ccount 0'
            print 'will process the 10-k files for the companies that are in "/Volumes/Seagate Backup Plus Drive/DBPartTime/SEC-Edgar-data" and write(append) the results'
            print 'to "csv_test" withouth taking the first 20 companies(in alphabetical orer into account)'
            print
            print 'A status file will be created in the same folder/direcory with the report file'
            print

            print 'All option arguments should be inserted in full paths, if one of the directories contains a " "' \
                  ' in its name and "\\" has to be inserted before it.\n' \
                  'For example if the name is "Zoro Corp" then the argument whould be "Zoro\ Corp"'
            print 'A simpler alternative is to write the names of the directories between quotes as shown above'

            print 'In order to specify the current directory in an unix based system(mac or linux) ' \
                  'type "." as argument for "rdir" or "wdir"'
            print
            print

        elif argv[1] == '-tf':

            print 'main.py -tf -sdir <source_directory> -ddir <destiantion_directory> -t <alphabetical_threshold>'
            print
            print 'main.py -tf         -transfers(moves) files between directories'
            print '        -sdir       -source directory, containing the files need to be transfered'
            print '        -ddir       -destination directory, where the files need to be transfered'
            print '        -t          -alphabetical threshold, should be given as "" if no threshold is desired,'
            print '                    otherwise the full name of the company should be given'
            print
            print 'For example, the command:'
            print 'python main.py -tf -sdir /Users/adrian_radulescu1997/Documents/Uni-Courses/DBPartTimeJob/crawler/excel_reports -ddir /Users/adrian_radulescu1997/Documents/Uni-Courses/DBPartTimeJob/crawler/trans_tests -t 1847'
            print 'will transfer the subdirecories(folders) from the location given to "-sdir" to the location given to "-ddir" withought moving the ones that preceed a file that starts with "1847"'
            print
            print

        sys.exit()

    else:

        print

        if '-r' in argv[0]:
            fargs = extract_args(argv)
            print 'args extracted'
            import company_word_counting

            if argv[0] == '-rf' or '-rc' in argv[0]:

                if argv[0] == '-rf':
                    scores = company_word_counting.rawscore_for_words_for_company(**fargs)
                    table = company_word_counting.beautify_report(scores)
                    print table
                elif argv[0] == '-rcy':
                    scores = company_word_counting.rawscore_for_words_for_company(**fargs)
                    print scores
                elif argv[0] == '-rcsy':
                    print "comp ciks ", fargs['comps']
                    for comp in fargs['comps']:
                        fargs['comp'] = comp
                        print comp
                        scores = company_word_counting.rawscore_for_words_for_company(**fargs)
                        print scores

            else:

                import os
                i = 0
                count_threshold = 0 if 'ccount' not in fargs else fargs['ccount']
                error_count = 0

                # open the status file for writing
                if fargs['csvwdir'][-1] is not '/' and fargs['csvwdir'] is not '\\':
                    fargs['csvwdir'] += '/'
                stf = open(str(fargs['csvwdir']) + 'report_status', 'w')

                # for the 10-K files of every company calculate their scores
                # a dictionary with the raw scores is returned and every category value is printed on screen
                for company in sorted(os.listdir(fargs['rdir'])):

                    if i > count_threshold:

                        if not os.path.isdir(fargs['rdir'] + ('/' if fargs['rdir'][-1] is not '/' else '') + company) \
                                or i < fargs['ccount']:
                                continue

                        print 'processing company: ', company

                        fargs['comp'] = company
                        try:
                            scores = company_word_counting.rawscore_for_words_for_company(**fargs)
                            print 'processed'
                            stf.write('CRE: ' + str(scores['CRE']) + ' CON: ' + str(scores['CON']) + ' COL: ' + str(scores['COL'])
                                      + ' COM: ' + str(scores['COM']) + '\n')
                            print 'current number of processed companies = ', i + 1
                            stf.write('current number of processed companies = ' + str(i + 1))
                        except KeyboardInterrupt:
                            print 'current number of processed companies = ', i + 1
                            print 'error count = ', error_count
                            break
                        except:
                            print 'Error while processing the files for company' + company
                            print 'moving on'
                            error_count += 1

                    i += 1

                print 'companies processed  = ', i
                print 'misses               = ', error_count

        elif argv[0] == '-ud':
            fargs = extract_args(argv)
            import database_creation
            database_creation.update_database(fargs['wdir'])
        elif argv[0] == '-uf':
            fargs = extract_args(argv)
            import bulk_download
            bulk_download.bulk_download(fargs)
        elif argv[0] == '-i':
            fargs = extract_args(argv)
            modules = ['pyahocorasick', 'openpyxl', 'regex', 'bs4', 'nltk', 'pysqlite', 'pandas', 'requests', 'sqlalchemy', 'BeautifulSoup4']
            import os
            for mod in modules:
                os.system(sys.executable + ' -m pip install ' + mod)
        elif argv[0] == '-tf':
            fargs = extract_args(argv)
            import file_transfering
            file_transfering.transfer_subdirs(source=fargs['sdir'], dest=fargs['ddir'], threshold=fargs['t'])

        sys.exit()

if __name__ == "__main__":

    print "This is a script which performs Edgar 10-K files related operations"
    print "Type the coresponding option for the operation you need to perform"
    print "For more informations type -h for the full help menu"
    print "For different options type -h -'option', for example: 'python main.py -h -rf' will give instruction on the -rf action"

    print "Required libraries/modules:"
    print
    print "1.  pyahocorasick  - for handling string matching                    https://pypi.python.org/pypi/pyahocorasick/"
    print "2.  bs4            - for parsing html                                https://pypi.python.org/pypi/beautifulsoup4"
    print "3.  nltk           - for text processing                             https://pypi.python.org/pypi/nltk"
    print "4.  pickle         - for object serialization                        "
    print "5.  regex          - for using regular expressions                   https://pypi.python.org/pypi/regex/"
    print "6.  sqlite3        - for database management"
    print "7.  requests       - for managing script connections to internet"
    print "8.  pandas         - for reading databases                           https://pypi.python.org/pypi/pandas/"
    print "9.  sqlalchemy     - for managing sql queries over a connection"
    print "10. openpyxel      - for writing excel reports.                      https://pypi.python.org/pypi/openpyxl"
    print "11. csv            - for reading .csv database files"
    print "12. BeautifulSoup4 - for parsing html"
    print
    print 'These libraries can be downloaded at the provided links or installed automatically by typing'
    print 'python main.py -i on MAC OSX or Linux or'
    print 'C:\Python27\python.exe main.py -i on Windows'
    print 'IMPORTANT: for some of these libraries to work, the Microsoft Visual C++ compiler for Python 2.7 needs to be installed'
    print 'If this is not already on your device you cand download it ad https://www.microsoft.com/en-us/download/details.aspx?id=44266'


    print "Available actions are:"
    print "     -rf          -make a report on a give file"
    print "     -rc          -make a report on a company"
    print "     -rcy         -make a report on a company between specific years"
    print "     -rcsy        -make a report on multiple company between specific years"
    print "     -rblkcsv     -creates a csv file containing reports for all the files in the database which have not yet been reported"
    print "     -ud          -updates the EDGAR database register .csv file which contains information about all the files that are in the EDGAR detabase"
    print "     -uf          -updates the 10-K files that are contained in the local database"
    print "     -tf          -transfers database content between given locations"

    if platform.system() == 'Windows':
        main(sys.argv[2:])
    else:
        main(sys.argv[1:])
