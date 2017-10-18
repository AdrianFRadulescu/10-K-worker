import re
import os
import string
import ahocorasick
from sys import platform
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup


def make_automaton_from_list(args=[]):
    """
        Creates an automaton form a given list
    :param args:
    :return:
    """

    automaton = ahocorasick.Automaton(ahocorasick.STORE_LENGTH)
    for a in args:
        automaton.add_word(a)
    return automaton


def make_frequency_automaton_from_list(args=[]):
    """
        Convert a given string list into an searching automaton
    :param args:
    :return:
    """

    automaton = ahocorasick.Automaton(ahocorasick.STORE_INTS)
    for a in args:
        if automaton.exists(a):
            automaton.add_word(a, automaton.get(a) + 1)
        else:
            automaton.add_word(a, 1)

    return automaton


def sanitize_freqs_automaton(automaton=ahocorasick.Automaton()):
    """
    Cleans the dictionary of items that contain other characters besides alphas
    :param dict:
    :return:
    """
    for it in automaton.keys():
        if not it.isalpha:
            automaton.add_word(it, 0)

    return automaton


def read_text_from_file_without_tables(file_path=''):
    """
    Get the content of the file as a string and cut the tables and form it in order to preserve the actual text
    Cut as many tags as possible and the first line as well

    :param file_path:
    :return:

    """

    fr = open(file_path, 'r')
    data = fr.read()
    # make a copy for safety purposes
    initial_data = data
    # get the text of the file
    try:
        data = re.search('<TEXT>(.+?)</TEXT>', data).group(1)
    except AttributeError:
        # no text
        data = ''  # apply your error handling

    # remove the tables
    data = re.sub(r'<TABLE>.*?</TABLE>', r'', data)
    data = re.sub(r'<table>.*?</table>', r'', data)

    # print data is initial_data

    if data is '':
        data = initial_data

    # print 'data=' + data

    return data


def beautify_data(data='', flag=False):
    """
        Remove html and special characters from text

    :param text:
    :return:
    """

    if 'win32' in platform or ('win' in platform and 'darwin' not in platform):
        try:
            soup = BeautifulSoup(data, 'html.parser')
        except:
            soup = BeautifulSoup(data)
    else:
        soup = BeautifulSoup(data, 'lxml')

    # extract the text
    text_data = soup.get_text().encode('unicode-escape')  # .decode('unicode-escape')
    final_text_data = text_data.decode('unicode-escape').encode('utf-8').strip()
    final_text_data = re.sub(r'<.*?>', '', final_text_data)

    # replace special caracters
    final_text_data = final_text_data.replace('-\n', '').replace('and/or', 'and or').replace('--', '').replace('- ', '')
    final_text_data = final_text_data.replace('_', '').replace('  ', '')
    final_text_data = final_text_data.replace('\n', '')

    if flag:
        # replace unprintable characters
        printables = string.printable
        not_printables = set()
        for ch in final_text_data:
            if ch not in string.printable:
                not_printables.add(ch)
        for ch in not_printables:
            final_text_data = final_text_data.replace(ch, ' ', final_text_data.count(ch))

    return final_text_data


def check(args=''):
    """
        Check if a given string is a word
    :param args:
    :return:
    """
    return args.replace('-', '').isalpha()


def count_words_in_text(args=''):
    """
        Calculate the total number of words(alpha sub-strings) from a given string
    :param args:
    :return:
    """
    return len([str for str in word_tokenize(args) if check(str)])


def get_word_frequencies(args=''):
    """
        Get the frequencies of the words from a given string
    :param args:
    :return:
    """

    tokens = [str.lower() for str in word_tokenize(args) if check(str)]
    return make_frequency_automaton_from_list(tokens)


def get_refined_word_frequencies(args='', negative_words=[], remove_range=2):
    '''
        Eliminates the negative words and the words affected by them as according to the remove range
        and then calculates their frequencies
    :param args:
    :param negative_words:
    :param remove_range:
    :return:
    '''

    tokens = [str.lower() for str in word_tokenize(text=args) if check(str)]

    # print tokens
    refined_tokens = []

    # a list of True and False which indicates if a previous token is in the negative_words list
    prev_tokens = []

    is_any_previous_token_negative = 0

    for token in tokens:

        if is_any_previous_token_negative == 0 and token not in negative_words:
            refined_tokens += [token]

        prev_tokens += [1 if token in negative_words else 0]
        is_any_previous_token_negative += prev_tokens[-1]

        if len(prev_tokens) > remove_range:
            is_any_previous_token_negative -= prev_tokens[0]
            prev_tokens.pop(0)

    # print list(make_frequency_automaton_from_list(refined_tokens))

    freq_automaton = make_frequency_automaton_from_list(refined_tokens)
    return freq_automaton


def get_cik(file=''):
    """
        Checks the file and return the comapny CIK from it
    :param file:
    :return:
    """

    try:
        rez = ''
        for ch in file:
            if ch.isalnum():
                rez += ch
            else:
                break
        return (10 - len(rez) if 10 >= len(rez) else 0) * '0' + rez
    except:
        print 'CIK ERROR, invalid file'
        return ''


def get_file_year(file=''):
    """
        Check the file name and extract the year from it
    :param file: the name of the target file
    :return:
    """
    return int(list(filter(lambda a: a.isdigit() and len(a) is 4, file.split('-')))[0])


def get_file_year_from_content(file=''):
    """

    :param file: the path to the targeted file
    :return:
    """

    data = open(file, 'r').read().split('\n')[:25]
    year = ''

    for line in data:
        if 'CONFORMED PERIOD OF REPORT:' in line:
            year = year.join(filter(lambda ch: ch.isdigit(), line))[:4]
            break

    return year


def get_company_name(file=''):
    return re.search('-(.*)-', file).group(1)


def get_file_company(file=''):
    """
        Returns the name of the company from the file name
    :param file:    the file's name
    :return:
    """
    try:
        return file if '-' not in file else file.split('-')[1]
    except:
        print "file name error:" + file
        return ""


def get_item_7(directory='', file=''):
    """
        Extract the item 7 section of the given file as a single string
    :param directory: the directory of the file
    :param file: the name of the file
    :return:
    """

    data = ''

    try:
        if directory[-1] != '/':
            directory += '/'
        data = read_text_from_file_without_tables(directory + file)
    except IOError:
        return ''

    final_text_data = beautify_data(data)

    # print "------ len --------"
    # print len(final_text_data)

    # print 'file=', file
    # print data


    # print 'fdata = ', final_text_data
    # print 'item 7' in final_text_data or 'ITEM 7' in final_text_data or 'Item 7' in final_text_data
    # global fw
    # fw.write('fdata = ' + str(final_text_data) + "\n")
    # fw.write(str('item 7' in final_text_data or 'ITEM 7' in final_text_data or 'Item 7' in final_text_data))
    # fw.write("\n")
    # global acc
    # acc = acc and ('item' in final_text_data or 'ITEM' in final_text_data or 'Item' in final_text_data)
    # find item 7
    patterns = []
    patterns += [re.compile(r'(?<=Item\xc2\xa07\.).*?(?=Item\xc2\xa08\.)')]

    patterns += [re.compile(r'(?<=Item 7\.).*?(?=Item .\.)')]
    # patterns += [re.compile(r'(?<=Item 7\.).*?(?=ITEM .\.)')]
    # patterns += [re.compile(r'(?<=Item 7\.).*?(?=item .\.)')]
    patterns += [re.compile(r'(?<=ITEM 7\.).*?(?=ITEM .\.)')]
    # patterns += [re.compile(r'(?<=ITEM 7\.).*?(?=Item .\.)')]
    # patterns += [re.compile(r'(?<=ITEM 7\.).*?(?=item .\.)')]
    patterns += [re.compile(r'(?<=item 7\.).*?(?=item .\.)')]
    # patterns += [re.compile(r'(?<=item 7\.).*?(?=Item .\.)')]
    # patterns += [re.compile(r'(?<=item 7\.).*?(?=ITEM .\.)')]
    patterns += [re.compile(r'MANAGEMENT.*?DISCUSSION.*?FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA')]
    patterns += [re.compile(r'Management.*?Discussion.*?Financial Statements and Supplementary Data')]
    patterns += [re.compile(r'management.*?discussion.*?financial statements and supplementary data')]

    patterns += [re.compile(r'MANAGEMENT.*?DISCUSSION.*?FINANCIAL STATEMENTS AND SUPPLEMENTAL DATA')]
    patterns += [re.compile(r'Management.*?Discussion.*?Financial Statements and Supplemental Data')]
    patterns += [re.compile(r'management.*?discussion.*?financial statements and supplemental data')]

    patterns += \
        [re.compile(
            r'MANAGEMENT.*?DISCUSSION.*?FINANCIAL\xc2\xa0STATEMENTS\xc2\xa0AND\xc2\xa0SUPPLEMENTARY\xc2\xa0DATA')]
    patterns += \
        [re.compile(
            r'Management.*?Discussion.*?Financial\xc2\xa0Statements\xc2\xa0and\xc2\xa0Supplementary\xc2\xa0Data')]
    patterns += \
        [re.compile(
            r'management.*?discussion.*?financial\xc2\xa0statements\xc2\xa0and\xc2\xa0supplementary\xc2\xa0data')]

    patterns += \
        [re.compile(
            r'MANAGEMENT.*?DISCUSSION.*?FINANCIAL\xc2\xa0STATEMENTS\xc2\xa0AND\xc2\xa0SUPPLEMENTAL\xc2\xa0DATA')]
    patterns += \
        [re.compile(
            r'Management.*?Discussion.*?Financial\xc2\xa0Statements\xc2\xa0and\xc2\xa0Supplemental\xc2\xa0Data')]
    patterns += \
        [re.compile(
            r'management.*?discussion.*?financial\xc2\xa0statements\xc2\xa0and\xc2\xa0supplemental\xc2\xa0data')]

    '''
        write a regex for 1996 ZYCAD
    '''

    # patterns += [re.compile(r'ITEM 7.*?MANAGEMENT.*?DISCUSSION.*?')]

    item_7 = ''
    i = 0
    for p in patterns:
        result = p.findall(final_text_data)
        if result:
            # print i, 'fjafasdfhasufhuadsfupads', result
            for r in result:
                if len(r) > len(item_7):
                    item_7 = r
        i += 1
    del patterns
    del final_text_data
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


def get_item_7_word_frequencies_from_file(directory='', file='', negative_words=[], remove_range=2, refined=False):
    """
        Returns a dictionary containing all the words in the MANAGEMENT section of the document and their respecive
        frequencies
    :param directory:
    :param file:
    :param negative_words
    :param remove_range
    :param refined
    :return:
    """
    text_data = get_item_7(directory=directory, file=file)
    return get_word_frequencies(text_data) if not refined else get_refined_word_frequencies(text_data, negative_words,
                                                                                            remove_range)


def get_item_7_word_frequencies_for_company_from_year(parent_directory='~/', company='', year='', refined=False,
                                                      negative_words=[], remove_range=2):
    frequencies = ahocorasick.Automaton(ahocorasick.STORE_INTS)

    if not os.path.exists(parent_directory + company + '/'):
        return []
    files = os.listdir(parent_directory + company + '/')[0:]

    # print files

    for file in files:
        if year in file:
            candidate = get_item_7_word_frequencies_from_file(directory=parent_directory + company + '/',
                                                              file=file) if not refined \
                else get_item_7_word_frequencies_from_file(directory=parent_directory + company + '/', file=file,
                                                           refined=True, negative_words=negative_words,
                                                           remove_range=remove_range)
            if bool(candidate):
                frequencies = candidate
                # print 'file==', file
                # print frequencies ,"\ndasdad"
    # print '+', frequencies
    return sanitize_freqs_automaton(frequencies)


def get_text_word_frequencies_from_file(directory='', file='', refined=False, negative_words=[], remove_range=2):
    """
        Reads the file and gets the frequencies of all the words in the file
    :param directory:
    :param file:
    :return:
    """

    if directory[-1] != '/':
        directory += '/'

    # print "----- lent ------"
    # print len(beautify_data(read_text_from_file_without_tables(directory+file), flag=True))
    return get_word_frequencies(
        beautify_data(read_text_from_file_without_tables(directory + file), flag=True)) if not refined \
        else get_refined_word_frequencies(
        beautify_data(read_text_from_file_without_tables(directory + file), flag=True), negative_words=negative_words,
        remove_range=remove_range)


def get_text_word_frequencies_for_company_from_year(parent_directory='~/', company='', year='', refined=False,
                                                    negative_words=[], remove_range=2):
    """
        Returns the frequencies for the most likely file of the given year
    :param parent_directory:    the directory in which the database is contained
    :param company:             the company to which the file belongs
    :param year:                the year of the file
    :param refined:             true if the frequencies are to be refined
    :param negative_words:      the list of negative words that precede words that need to be exluded
    :param remove_range:        the maximum distance after a negative word for words to be eliminated
    :return:
    """

    frequencies = ahocorasick.Automaton(ahocorasick.STORE_INTS)
    current_total = 0

    if not os.path.exists(parent_directory + company + '/'):
        return []
    files = os.listdir(parent_directory + company + '/')[0:]

    # print files

    for file in files:
        if year in file:
            candidate = get_text_word_frequencies_from_file(directory=parent_directory + company + '/', file=file,
                                                            refined=refined, negative_words=negative_words,
                                                            remove_range=remove_range)
            candidate_total = sum(candidate.values())
            if bool(candidate) and candidate_total > current_total:
                frequencies = candidate
                current_total = candidate_total
                # print 'file==', file
                # print frequencies ,"\ndasdad"
    # print '+', frequencies
    return sanitize_freqs_automaton(frequencies)


if __name__ == "__main__":
    # for a single company file

    # print os.path.exists('/Volumes/Seagate Backup Plus Drive/DBPartTime/SEC-Edgar-data/Zoro Mining Corp.')
    # print os.listdir('/Volumes/Seagate Backup Plus Drive/DBPartTime/SEC-Edgar-data/Zoro Mining Corp.')

    print get_cik('1599407-1847 Holdings LLC-2015-04-15')

    negative_words = ['not', 'less', 'nothing', 'no', 'never', 'negative', 'nobody', 'nondescript', 'futile',
                      'unnecessary', 'useless']

    l = os.listdir('/Volumes/Seagate Backup Plus Drive/DBPartTime/SEC-Edgar-data/Zoro Mining Corp.')[1:]
    file_path1 = '/Volumes/Seagate Backup Plus Drive/DBPartTime/SEC-Edgar-data/Zoro Mining Corp.' + l[0]

    # print get_item_7_word_frequencies_from_file('/Volumes/Seagate Backup Plus Drive/DBPartTime/SEC-Edgar-data/Zoro Mining Corp.', l[0])
    # print get_item_7_word_frequencies_from_file('/Volumes/Seagate Backup Plus Drive/DBPartTime/SEC-Edgar-data/Zoro Mining Corp.', l[1])
    import time

    time0 = time.localtime()
    print time0
    # print get_refined_word_frequencies("I'm not your boss you fucking moron. Go see her and do not tell her that", negative_words=negative_words)



    refined_result1 = get_item_7_word_frequencies_for_company_from_year(
        parent_directory='/Volumes/Seagate Backup Plus Drive/DBPartTime/SEC-Edgar-data/',
        company='Zoro Mining Corp.', year='2011', refined=True, negative_words=negative_words)

    print dict(map(lambda q: (q, refined_result1.get(q)), refined_result1))
    print sum(dict(map(lambda q: (q, refined_result1.get(q)), refined_result1)).values())

    time_r1 = time.localtime()
    # print time_r1 - time0,'sec'

    refined_result2 = get_text_word_frequencies_for_company_from_year(
        parent_directory='/Volumes/Seagate Backup Plus Drive/DBPartTime/SEC-Edgar-data/',
        company='Zoro Mining Corp.', year='2011', refined=True)  # , negative_words=negative_words)
    time_r2 = time.localtime()
    # print time_r2 - time_r1,'sec'


    print dict(map(lambda q: (q, refined_result2.get(q)), refined_result2))
    print sum(dict(map(lambda q: (q, refined_result2.get(q)), refined_result2)).values())

    result1 = get_item_7_word_frequencies_for_company_from_year(
        parent_directory='/Volumes/Seagate Backup Plus Drive/DBPartTime/SEC-Edgar-data/',
        company='Zoro Mining Corp.', year='2011')

    time1 = time.localtime()
    # print time1-time_r2,'sec'

    print dict(map(lambda q: (q, result1.get(q)), result1))
    print sum(dict(map(lambda q: (q, result1.get(q)), result1)).values())

    result2 = get_text_word_frequencies_for_company_from_year(
        parent_directory='/Volumes/Seagate Backup Plus Drive/DBPartTime/SEC-Edgar-data/',
        company='Zoro Mining Corp.', year='2011')
    time2 = time.localtime()
    # print time2-time1,'sec'

    print dict(map(lambda q: (q, result2.get(q)), result2))
    print sum(dict(map(lambda q: (q, result2.get(q)), result2)).values()), '\n'

    print get_cik('1599407-1847 Holdings LLC-2015-04-15')

    print get_file_year_from_content(
        '/Users/adrian_radulescu1997/Documents/Uni-Courses/DBPartTimeJob/crawler/utility_tests/0000017206/17206-CAPITAL HOLDING CORP-1993-12-22')
