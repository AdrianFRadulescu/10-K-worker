
This is a collection of scripts which perform Edgar 10-K files related operations.
Type the corresponding option for the operation you need to perform.
For help type -h for the full help menu.
For different options type -h -'option', for example: 'python main.py -h -rf' will give instruction on the -rf action.


Required libraries/modules:

    1.  pyahocorasick  - for handling string matching                    https://pypi.python.org/pypi/pyahocorasick/
    2.  bs4            - for parsing html                                https://pypi.python.org/pypi/beautifulsoup4
    3.  nltk           - for text processing                             https://pypi.python.org/pypi/nltk
    4.  pickle         - for object serialization                        
    5.  regex          - for using regular expressions                   https://pypi.python.org/pypi/regex/
    6.  sqlite3        - for database management
    7.  requests       - for managing script connections to internet
    8.  pandas         - for reading databases                           https://pypi.python.org/pypi/pandas/
    9.  sqlalchemy     - for managing sql queries over a connection
    10. openpyxel      - for writing excel reports.                      https://pypi.python.org/pypi/openpyxl
    11. csv            - for reading .csv database files
    12. BeautifulSoup4 - for parsing html

These libraries can be downloaded at the provided links or installed automatically by typing
    'python main.py -i' on MAC OSX or Linux or
    'C:\Python27\python.exe main.py -i' on Windows

IMPORTANT: for some of these libraries to work, the Microsoft Visual C++ compiler for Python 2.7 needs to be installed'

If this is not already on your device you can't download it at https://www.microsoft.com/en-us/download/details.aspx?id=44266'


Available actions(for main.py) are:

     -rf          - make a report on a give file
     -rc          - make a report on a company
     -rcy         - make a report on a company between specific years
     -rcsy        - make a report on multiple company between specific years
     -rblkcsv     - creates a csv file containing reports for all the files in the database 
                    which have not yet been reported
     -ud          - updates the EDGAR database register .csv file which contains information 
                    about all the files that are in the EDGAR detabase
     -uf          - updates the 10-K files that are contained in the local database
     -tf          - transfers database content between given locations

Genaral arguments are:
    
    -rdir         - the directory where the database is located
    -csvfile      - the path to the csv output file
    -nw           - a list of negative words to be used in case of refined reports
    -comps        - the path to the file containing the list of companies to be processed
    -c_item7      - True if the words are to be counted only from item 7, False otherwise
    -t            - the type of the report(csv, excel)
    -fy           - first year from which the proceesing starts
    -ly           - last year
    -ccount       - the number of already counted companies
    -defcat       - specifies if the default categories from "Culture bag og words are to be used"
    -categs       - the file containing the categories

Example Usage:

On Windows(assuming your python interpreter is intalled in "C:\Python27\python.exe", arguments are given on individual lines):

    C:\Python27\python.exe main.py 
        -rcsy 
        -rdir /Users/adrian_radulescu1997/Documents/Uni-Courses/DBPartTimeJob/crawler/utility_tests  
        -csvfile csv_test/test6.csv (can be also given as -csvwdir csv_test -csvrf test6.csv)
        -nw [no,none,not,useless,unless,less,unnecessary] 
        -comps /Users/adrian_radulescu1997/Documents/Uni-Courses/DBPartTimeJob/crawler/comps.csv  
        -t csv 
        -c_item7 True
        -fy 1994 
        -ly 2016 
        -ccount 0 
        -defcat False 
        -categs '/Users/adrian_radulescu1997/Documents/Uni-Courses/DBPartTimeJob/crawler/Culture type Bag of words.ctg'
    
    This will make a report for companies on multiple years only for the item 7 section.

An additional script for reanming the directories in the database is provided:

Available actions(for rename_database.py) are:

    -cik        -will change the names of the directories in the database to represent the ciks of the companies the 
                 files describe
    -namse      -will revert the 'cik' actions 
    
Arguments are:
    
    -cik :
        database_path   -the path to the directory containing the folders of the companies
        -mode           -the opening mode for the cik_table and cik files('w' for writing them, 'a' for appending to them)
    -names:
        database_path   -the path to the directory containing the folders of the companies
    
    
Example Usage:

    C:\Python27\python.exe rename_database.py -cik database_location -mode 'w'
    C:\Python27\python.exe rename_database.py -names database_location
    
    This will rename the comapnies in the database and create an index file 



