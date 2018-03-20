"""
Program to provide generic parsing for all files in user-specified directory.
The program assumes the input files have been scrubbed,
  i.e., HTML, ASCII-encoded binary, and any other embedded document structures that are not
  intended to be analyzed have been deleted from the file.

Dependencies:
    Python:  Load_MasterDictionary.py
    Data:    LoughranMcDonald_MasterDictionary_2014.csv

The program outputs:
   1.  File name
   2.  File size (in bytes)
   3.  Number of words (based on LM_MasterDictionary)
   4.  Proportion of positive words (use with care - see LM, JAR 2016)
   5.  Proportion of negative words
   6.  Proportion of uncertainty words
   7.  Proportion of litigious words
   8.  Proportion of modal-weak words
   9.  Proportion of modal-moderate words
  10.  Proportion of modal-strong words
  11.  Proportion of constraining words (see Bodnaruk, Loughran and McDonald, JFQA 2015)
  12.  Number of alphanumeric characters (a-z, A-Z, 0-9)
  13.  Number of alphabetic characters (a-z, A-Z)
  14.  Number of digits (0-9)
  15.  Number of numbers (collections of digits)
  16.  Average number of syllables
  17.  Average word length
  18.  Vocabulary (see Loughran-McDonald, JF, 2015)

  ND-SRAF
  McDonald 2016/06
"""
import csv
import re
import string
import time
#sys.path.append('D:\GD\Python\TextualAnalysis\Modules')  # Modify to identify path for custom modules
import Load_MasterDictionary as LM

from aux_functions import get_item_7, get_file_year_from_content, get_company_name_from_content, get_conformed_period_of_report_from_content
from aux_functions import get_cik_from_content, get_all_files
import categories_key_words_reading
from database_api import add_file_data_to_db, is_file_in_database

"""
    USER DEFINED ENVIRONMENT
    
    COMPLETE THIS SECTION WITH THE APPROPRIATE PATHS AND VALUES FOR YOUR PC
    
"""

# User defined Bag of Words (specify the path to the file containing the bag of words)
BAG_OF_WORDS_FILE_PATH = '/Users/adrian_radulescu1997/Documents/Uni-Courses/DBPartTimeJob/crawler/temp_name/Culture type Bag of words.ctg'
BAG_OF_WORDS = categories_key_words_reading.get_categories(BAG_OF_WORDS_FILE_PATH)

# File System path (specify the path to the folder containing all the files)
FILE_SYSTEM_PATH = r'/Users/adrian_radulescu1997/Documents/Uni-Courses/DBPartTimeJob/crawler/temp_name/Adrian_10-Ks'

# get a list of all the interest files
TARGET_FILES = get_all_files(path=FILE_SYSTEM_PATH, sorted=True) # returns all files from the folder given and sub-folders

# True if adding to database, false otherwise
UPDATE_DATABASE = True

# list(map(lambda x: FILE_SYSTEM_PATH + '/' + x, os.listdir(FILE_SYSTEM_PATH)))

# the number of range in which a negative word can influence other words
TEXT_WORD_RANGE = 3

# the list of negative words
NEGATIVE_WORDS_FILE \
    = '/Users/adrian_radulescu1997/Documents/Uni-Courses/DBPartTimeJob/crawler/temp_name/negative_words'

with open(NEGATIVE_WORDS_FILE, 'r') as f_in:
    NEGATIVE_WORDS = f_in.read().split(',')

# User defined text section('item_7' if item_7 is needed, '' otherwise)
TEXT_SECTION = 'item_7'

# User defined output file
OUTPUT_FILE = r'/Users/adrian_radulescu1997/Documents/Uni-Courses/DBPartTimeJob/crawler/temp_name/tmp_results.csv'
OUTPUT_FILE_ITEM_7 = r'/Users/adrian_radulescu1997/Documents/Uni-Courses/DBPartTimeJob/crawler/temp_name/tmp_results_item7.csv'

# Setup output
OUT_DATA_FIELDS = ['file name,', 'file size,', 'number of words,', '% positive,', '% negative,',
                 '% uncertainty,', '% litigious,', '% modal-weak,', '% modal moderate,',
                 '% modal strong,', '% constraining,', '# of alphanumeric,', '# of digits,',
                 '# of numbers,', 'avg # of syllables per word,', 'average word length,', 'vocabulary'] + list(BAG_OF_WORDS)


OUTPUT_FIELDS = ['year', 'CIK', 'company name'] + list(BAG_OF_WORDS) + ['number of words in text']
OUTPUT_FIELDS_ITEM_7 = ['year', 'CIK', 'company name'] + list(BAG_OF_WORDS) + ['number of words in item 7', 'number of words in text']

# User defined file pointer(path) to LM dictionary
MASTER_DICTIONARY_FILE = '/Users/adrian_radulescu1997/Documents/Uni-Courses/DBPartTimeJob/crawler/temp_name/LoughranMcDonald_MasterDictionary_2014.csv'

lm_dictionary = LM.load_masterdictionary(MASTER_DICTIONARY_FILE, True)


def get_data(doc):

    vdictionary = {}
    _odata = [0] * 21
    total_syllables = 0
    word_length = 0

    bag_of_words_categories_indexes = {}

    for (ctg, index) in zip(list(BAG_OF_WORDS), [x + 17 for x in range(0, len(BAG_OF_WORDS))]):
        bag_of_words_categories_indexes[ctg] = index
    
    tokens = re.findall('\w+', doc)  # Note that \w+ splits hyphenated words

    # eliminate words preceded by up to 3 words by a negative word

    prev_tokens = []

    for token in tokens:

        if not token.isdigit():

            if len(token) > 1 and token in lm_dictionary and not any(map(lambda pt: pt in NEGATIVE_WORDS, prev_tokens)):

                _odata[2] += 1  # word count
                word_length += len(token)
                if token not in vdictionary:
                    vdictionary[token] = 1
                if lm_dictionary[token].positive:
                    _odata[3] += 1
                if lm_dictionary[token].negative:
                    _odata[4] += 1
                if lm_dictionary[token].uncertainty:
                    _odata[5] += 1
                if lm_dictionary[token].litigious:
                    _odata[6] += 1
                if lm_dictionary[token].weak_modal:
                    _odata[7] += 1
                if lm_dictionary[token].moderate_modal:
                    _odata[8] += 1
                if lm_dictionary[token].strong_modal:
                    _odata[9] += 1
                if lm_dictionary[token].constraining:
                    _odata[10] += 1

                # bag of words calculations
                if lm_dictionary[token].get_category() is not None:
                    for ctg in BAG_OF_WORDS:
                        if lm_dictionary[token].category_traits[ctg]:
                            _odata[bag_of_words_categories_indexes[ctg]] += 1

                total_syllables += lm_dictionary[token].syllables

            if len(token) > 1 or token == 'a':
                prev_tokens += [token]
                if len(prev_tokens) > TEXT_WORD_RANGE:
                    prev_tokens = prev_tokens[1:]


    _odata[11] = len(re.findall('[A-Z]', doc))
    _odata[12] = len(re.findall('[0-9]', doc))
    # drop punctuation within numbers for number count
    doc = re.sub('(?!=[0-9])(\.|,)(?=[0-9])', '', doc)
    doc = doc.translate(str.maketrans(string.punctuation, " " * len(string.punctuation)))
    _odata[13] = len(re.findall(r'\b[-+\(]?[$\xe2\x82\xac\xc2\xa3]?[-+(]?\d+\)?\b', doc))

    if _odata[2] == 0:
        with open('/Users/adrian_radulescu1997/Documents/Uni-Courses/DBPartTimeJob/crawler/temp_name/errors', 'w') as f_out:
            f_out.write(doc)
            f_out.write('-----------------------------------------------------------------------------------------------------------------------')

    _odata[16] = len(vdictionary)
    
    # Convert counts to %
    for i in range(3, 10 + 1):
        _odata[i] = (_odata[i] / _odata[2]) * 100
    # Vocabulary

    return _odata


def main(**kwargs):

    f_out = open(OUTPUT_FILE, 'w')
    wr = csv.writer(f_out, lineterminator='\n')

    if kwargs['item_7']:
        wr.writerow(OUTPUT_FIELDS_ITEM_7)
    else:
        wr.writerow(OUTPUT_FIELDS)

    if 'target_files' in kwargs.keys():
        file_list = kwargs['target_files']
    else:
        file_list = TARGET_FILES

    file_statistics = []

    for file in file_list:

        if is_file_in_database(filepath=file):
            continue

        print(file)
        with open(file, 'r') as f_in:
            doc = f_in.read()
        doc_len = len(doc)
        doc = re.sub('(May|MAY)', ' ', doc)  # drop all May month references
        doc = doc.upper()  # for this parse caps aren't informative so shift

        if kwargs['item_7']:
            doc_item_7 = get_item_7(doc)

        if len(doc_item_7) > 0:
            try:
                output_data_item_7 = get_data(doc_item_7)

                # print('len:' + '\n')
                output_data_item_7[0] = file.replace(FILE_SYSTEM_PATH, '')
                output_data_item_7[1] = doc_len

            except ArithmeticError:
                print('ArithmeticError file: ' + file)
                continue

        output_data = get_data(doc)

        # print('len:' + '\n')
        output_data[0] = file.replace(FILE_SYSTEM_PATH, '')
        output_data[1] = doc_len

        output_data += [get_file_year_from_content(file), get_company_name_from_content(file), get_conformed_period_of_report_from_content(file)]
        output_data += [get_cik_from_content(file)]
        file_statistics += [{'company': output_data[-2], 'year':output_data[-3], 'file_name':output_data[0], 'cpr': output_data[-1]}]

        """
            output_data = list containing a line describing the stats of the file
            
            output_data[-4] = file year
            output_data[-1] = company CIK
            output_data[-3] = company name
            output_data[17:17 + len(BAG_OF_WORDS)] = the counts for each category
            output_data[2] = number of words in the whole document 
            
        """

        if kwargs['item_7']:
            wr.writerow([output_data[-4], output_data[-1], output_data[-3]] + output_data_item_7[17:21] + [output_data_item_7[2]] + [output_data[2]])
            # write info to DB
            add_file_data_to_db(filename=file.split('/')[-1], filepath=file)

        else:
            wr.writerow([output_data[-4], output_data[-1], output_data[-3]] + output_data[17:17 + len(BAG_OF_WORDS)] + [output_data[2]])
            # write info to DB
            add_file_data_to_db(filename=file.split('/')[-1], filepath=file)

    return file_statistics


if __name__ == '__main__':

    start_time = time.strftime('%c')
    print('\n' + start_time + '\nGeneric_Parser.py\n')
    #import pprint
    #pprint.pprint(TARGET_FILES)

    main(item_7=TEXT_SECTION is 'item_7')

    print(TARGET_FILES)
    '''sys.argv[1]'''
    end_time = time.strftime('%c')
    print('\n' + start_time)
    print('\n' + end_time + '\nNormal termination.')

# Word,Sequence Number,Word Count,Word Proportion,Average Proportion,Std Dev,Doc Count,Negative,Positive,Uncertainty,Litigious,Constraining,Superfluous,Interesting,Modal,Irr_Verb,Harvard_IV,Syllables,Source
# NO,48937,25615520,0.001799473,0.001953919,0.001344438,894911,0,0,0,0,0,0,0,0,0,0,1,12of12inf
