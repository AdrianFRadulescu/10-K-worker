
"""
    Contains auxiliary functions

"""
import string
import re
import os


def get_item_7(data=''):
    """
        Extract the item 7 section of the given file as a single string
    :param data:
    :return:
    """


    # print "------ len --------"
    # print len(final_text_data)

    # print 'file=', file
    # print data



    patterns = []
    patterns += [re.compile(r'(?<=ITEM\xc2\xa07)(?s).*?(?=ITEM\xc2\xa08\.)')]

    patterns += [re.compile(r'(?<=ITEM 7)(?s).*?(?=ITEM)')]
    patterns += [re.compile(r'(?<=ITEM\n7)(?s).*?(?=ITEM)')]

    patterns += [re.compile(r'(?=ITEM.*?7)(?s).*(?=ITEM.*?8)')]

    '''
    patterns += [re.compile(r'(?<=ITEM 7\.).*?(?=ITEM .\.)')]
    patterns += [re.compile(r'MANAGEMENT.*?DISCUSSION.*?FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA')]

    patterns += [re.compile(r'MANAGEMENT.*?DISCUSSION.*?FINANCIAL STATEMENTS AND SUPPLEMENTAL DATA')]

    patterns += \
        [re.compile(
            r'MANAGEMENT.*?DISCUSSION.*?FINANCIAL\xc2\xa0STATEMENTS\xc2\xa0AND\xc2\xa0SUPPLEMENTARY\xc2\xa0DATA')]

    patterns += \
        [re.compile(
            r'MANAGEMENT.*?DISCUSSION.*?FINANCIAL\xc2\xa0STATEMENTS\xc2\xa0AND\xc2\xa0SUPPLEMENTAL\xc2\xa0DATA')]

    '''

    # patterns += [re.compile(r'ITEM 7.*?MANAGEMENT.*?DISCUSSION.*?')]

    item_7 = ''
    i = 0
    for p in patterns:
        result = p.findall(data)
        if result:
            # print i, 'fjafasdfhasufhuadsfupads', result
            for r in result:
                if len(r) > len(item_7):
                    item_7 = r
        i += 1
    del patterns
    # print 'i7 = ', item_7
    # clear the characters that are not printable
    printables = string.printable
    not_printables = set()
    for ch in item_7:
        if ch not in string.printable:
            not_printables.add(ch)
    for ch in not_printables:
        item_7 = item_7.replace(ch, ' ', item_7.count(ch))

    return item_7


def get_file_year_from_content(filepath=''):
    """

    :param filepath: the path to the targeted file
    :return:
    """

    data = open(filepath, 'r').read().split('\n')[:50]
    year = ''

    for line in data:
        if 'CONFORMED PERIOD OF REPORT:' in line:
            year = year.join(filter(lambda ch: ch.isdigit(), line))[:4]
            break

        elif 'YEAR ENDED' in line or 'year ended' in line:

            # look for 4 alphanumerical characters
            current_string_year = ''
            for ch in line:
                if '0' <= ch:
                    if ch <= '9':
                        current_string_year += ch
                    else:
                        if len(current_string_year) < 4:
                            current_string_year = ''
                        else:
                            year = current_string_year
                            break
                else:
                    if len(current_string_year) < 4:
                        current_string_year = ''
                    else:
                        year = current_string_year
                        break

            if len(current_string_year) == 4:
                year = current_string_year
                break

    return int(year)


def get_conformed_period_of_report_from_content(filepath=''):

    """
    :param filepath: the path to the targeted file
    :return:
    """

    data = open(filepath, 'r').read().split('\n')[:50]
    cpr = ''

    for line in data:
        if 'CONFORMED PERIOD OF REPORT:' in line:
            cpr = cpr.join(filter(lambda ch: ch.isdigit(), line))[:4]
            break

    return cpr


def cut_nonalpha_prefix_and_suffix(str=''):

    while not str[0].isalpha():
        str = str[1:]
    while not str[-1].isalpha():
        str = str[:-1]

    return str


def cut_nonnum_prefix_and_suffix(str=''):

    while not str[0].isnumeric():
        str = str[1:]
    while not str[-1].isnumeric():
        str = str[:-1]

    return str


def get_company_name_from_content(filepath=''):

    """
        Returns the name of the company based on text sources
    :param filepath:
    :return:
    """

    data = open(filepath, 'r').read().split('\n')[:100]
    company = ''

    for line in data:
        if 'COMPANY CONFORMED NAME:' in line:
            company = company.join(cut_nonalpha_prefix_and_suffix(line.split(':')[1]))
            break

    return company


def get_cik_from_content(file_name=''):

    """
           Returns the cik of the company based on text sources
       :param file:
       :return:
       """

    data = open(file_name, 'r').read().split('\n')[:100]
    cik = ''

    for line in data:
        if 'CENTRAL INDEX KEY:' in line:
            cik = cik.join(cut_nonnum_prefix_and_suffix(line.split(':')[1]))
            break

    return cik


def get_all_files(**kwargs):

    """
        Returns all the files from a directory and its subdirectiries
    :param path:
    :return:
    """

    if kwargs['path'][-1] is not '/':
        kwargs['path'] = kwargs['path'] + '/'

    filelist = []

    for item in os.listdir(kwargs['path']):

        if '.DS_Store' in item:
            continue

        if os.path.isdir(kwargs['path'] + item):
            filelist += get_all_files(path=kwargs['path'] + item, sorted=False)
        elif os.path.isfile(kwargs['path'] + item):
            if not get_file_type(path=kwargs['path'] + item):
                print(item + 'Ignored non 10-K file')
            else:
                filelist += [kwargs['path'] + item]

    if 'sorted' in kwargs and kwargs['sorted']:
        filelist = sorted(filelist, key=lambda file: get_file_year_from_content(file))

    return filelist


def get_file_type(**kwargs):

    """
        Looks for the submission type and returns true for 10K,10K405 and 10KSB
        Returns false for anything else
    :param kwargs:
    :return:
    """

    #if kwargs['path'][-4:] is not '.txt':
     #   return False

    #print(kwargs['path'])

    #'CONFORMED SUBMISSION TYPE:' in line and not any(map(lambda s: s in line, ['10-K', '10-K405', '10-KSB']))

    file = open(kwargs['path'], 'r')

    data = open(kwargs['path'], 'r').read().split('\n')[:100]

    for line in data:
        if 'CONFORMED SUBMISSION TYPE:' in line and '10-K/A' not in line and '10K/A' not in line and any(map(lambda s: s in line, ['10-K', '10-K405', '10-KSB', '10K', '10K405', '10KSB'])):
            return True

    return False


if __name__ == '__main__':

    with open('/Users/adrian_radulescu1997/Documents/Uni-Courses/DBPartTimeJob/crawler/temp_name/Adrian_10-Ks/EDGAR/10-X_C/2006/QTR2/20060414_10KSB_edgar_data_1167419_0001079973-06-000223_1.txt', 'r') as f_in:

        data =f_in.read().upper()

        print(get_item_7(data))

        q = open('nrt.txt', 'w')

        q.write(data)

    """
    x = get_file_year_from_content('/Users/adrian_radulescu1997/Documents/Uni-Courses/DBPartTimeJob/crawler/temp_name/Adrian_10-Ks/20131113_10-K_edgar_data_1446896_0001446896-13-000041_1.txt')

    print(x)

    x = get_company_name_from_content('/Users/adrian_radulescu1997/Documents/Uni-Courses/DBPartTimeJob/crawler/temp_name/Adrian_10-Ks/20130103_10-K_edgar_data_1411179_0001165527-13-000010_1.txt')

    print(x)

    x = get_cik_from_content('/Users/adrian_radulescu1997/Documents/Uni-Courses/DBPartTimeJob/crawler/temp_name/Adrian_10-Ks/20130103_10-K_edgar_data_1411179_0001165527-13-000010_1.txt')

    print(x)
    """
    #file1 = get_all_files('/Users/adrian_radulescu1997/Documents/Uni-Courses/DBPartTimeJob/crawler/temp_name/Adrian_10-Ks')
    #from pprint import pprint
    #pprint(file1)