#!/usr/bin/python3
"""Routine to load MasterDictionary class"""
# BDM : 201510


import time
import categories_key_words_reading

BAG_OF_WORDS = categories_key_words_reading.get_categories('/Users/adrian_radulescu1997/Documents/Uni-Courses/DBPartTimeJob/crawler/temp_name/Culture type Bag of words.ctg')

CTG_STATS = {}


class MasterDictionary:
    def __init__(self, cols, _stopwords):
        self.word = cols[0].upper()

        self.category_traits = {}

        self._get_category(self.word)

        for ctg in BAG_OF_WORDS:
            if self.category is ctg:
                self.category_traits[ctg] = 1
            else:
                self.category_traits[ctg] = 0

        self.sequence_number = int(cols[1])
        self.word_count = int(cols[2])
        self.word_proportion = float(cols[3])
        self.average_proportion = float(cols[4])
        self.std_dev_prop = float(cols[5])
        self.doc_count = int(cols[6])
        self.negative = int(cols[7])
        self.positive = int(cols[8])
        self.uncertainty = int(cols[9])
        self.litigious = int(cols[10])
        self.constraining = int(cols[11])
        self.superfluous = int(cols[12])
        self.interesting = int(cols[13])
        self.modal_number = int(cols[14])
        self.strong_modal = False
        if int(cols[14]) == 1:
            self.strong_modal = True
        self.moderate_modal = False
        if int(cols[14]) == 2:
            self.moderate_modal = True
        self.weak_modal = False
        if int(cols[14]) == 3:
            self.weak_modal = True
        self.sentiment = {}
        self.sentiment['negative'] = bool(self.negative)
        self.sentiment['positive'] = bool(self.positive)
        self.sentiment['uncertainty'] = bool(self.uncertainty)
        self.sentiment['litigious'] = bool(self.litigious)
        self.sentiment['constraining'] = bool(self.constraining)
        self.sentiment['strong_modal'] = bool(self.strong_modal)
        self.sentiment['weak_modal'] = bool(self.weak_modal)
        self.irregular_verb = int(cols[15])
        self.harvard_iv = int(cols[16])
        self.syllables = int(cols[17])
        self.source = cols[18]

        if self.word in _stopwords:
            self.stopword = True
        else:
            self.stopword = False
        return

    def _get_category(self, word=''):
        """
            Checks to which category(ies) from the BAG_OF_WORDS this word belongs to
            and marks it as a trait
        :param word:
        :return:
        """
        self.category = None
        for ctg in BAG_OF_WORDS:

            self.category_traits[ctg] = 0

            for root in BAG_OF_WORDS[ctg]:
                if root is not '' and word.startswith(root.upper()):
                    self.category_traits[ctg] = 1
                    self.category = ctg


        return None

    def get_category(self):
        return self.category

    def get_category_traits(self):
        return self.category_traits


def create_sentimentdictionaries(_master_dictionary, _sentiment_categories):

    _sentiment_dictionary = {}
    for category in _sentiment_categories:
        _sentiment_dictionary[category] = {}
    # Create dictionary of sentiment dictionaries with count set = 0
    for word in _master_dictionary.keys():
        for category in _sentiment_categories:
            if _master_dictionary[word].sentiment[category]:
                _sentiment_dictionary[category][word] = 0

    return _sentiment_dictionary


def load_masterdictionary(file_path, print_flag=False, f_log=None, get_other=False, bag_of_words=False, ctg_stats={}):
    _master_dictionary = {}
    _sentiment_categories = ['negative', 'positive', 'uncertainty', 'litigious', 'constraining',
                             'strong_modal', 'weak_modal']
    # Load slightly modified nltk stopwords.  I do not use nltk import to avoid versioning errors.
    # Dropped from nltk: A, I, S, T, DON, WILL, AGAINST
    # Added: AMONG,
    _stopwords = ['ME', 'MY', 'MYSELF', 'WE', 'OUR', 'OURS', 'OURSELVES', 'YOU', 'YOUR', 'YOURS',
                       'YOURSELF', 'YOURSELVES', 'HE', 'HIM', 'HIS', 'HIMSELF', 'SHE', 'HER', 'HERS', 'HERSELF',
                       'IT', 'ITS', 'ITSELF', 'THEY', 'THEM', 'THEIR', 'THEIRS', 'THEMSELVES', 'WHAT', 'WHICH',
                       'WHO', 'WHOM', 'THIS', 'THAT', 'THESE', 'THOSE', 'AM', 'IS', 'ARE', 'WAS', 'WERE', 'BE',
                       'BEEN', 'BEING', 'HAVE', 'HAS', 'HAD', 'HAVING', 'DO', 'DOES', 'DID', 'DOING', 'AN',
                       'THE', 'AND', 'BUT', 'IF', 'OR', 'BECAUSE', 'AS', 'UNTIL', 'WHILE', 'OF', 'AT', 'BY',
                       'FOR', 'WITH', 'ABOUT', 'BETWEEN', 'INTO', 'THROUGH', 'DURING', 'BEFORE',
                       'AFTER', 'ABOVE', 'BELOW', 'TO', 'FROM', 'UP', 'DOWN', 'IN', 'OUT', 'ON', 'OFF', 'OVER',
                       'UNDER', 'AGAIN', 'FURTHER', 'THEN', 'ONCE', 'HERE', 'THERE', 'WHEN', 'WHERE', 'WHY',
                       'HOW', 'ALL', 'ANY', 'BOTH', 'EACH', 'FEW', 'MORE', 'MOST', 'OTHER', 'SOME', 'SUCH',
                       'NO', 'NOR', 'NOT', 'ONLY', 'OWN', 'SAME', 'SO', 'THAN', 'TOO', 'VERY', 'CAN',
                       'JUST', 'SHOULD', 'NOW']

    with open(file_path) as f:
        _total_documents = 0
        _md_header = f.readline()
        for line in f:
            cols = line.split(',')

            _master_dictionary[cols[0]] = MasterDictionary(cols, _stopwords)

            aux = _master_dictionary[cols[0]]

#            if aux.get_category() is not None:
#                print(aux.get_category(), aux.get_category_traits())

#            for ctg in CTG_STATS:
#                ctg_stats[ctg] += aux.get_category_traits()[ctg]

            _total_documents += _master_dictionary[cols[0]].doc_count
            if len(_master_dictionary) % 5000 == 0 and print_flag:
                print('\r ...Loading Master Dictionary' + ' {}'.format(len(_master_dictionary)), '', True)

    if print_flag:
        #print('\r', end = '')  # clear line
        print('\nMaster Dictionary loaded from file: \n  ' + file_path)
        print('  {0:,} words loaded in master_dictionary.'.format(len(_master_dictionary)) + '\n')

    if f_log:
        try:
            f_log.write('\n\n  load_masterdictionary log:')
            f_log.write('\n    Master Dictionary loaded from file: \n       ' + file_path)
            f_log.write('\n    {0:,} words loaded in master_dictionary.\n'.format(len(_master_dictionary)))
        except Exception as e:
            print('Log file in load_masterdictionary is not available for writing')
            print('Error = {0}'.format(e))

    if get_other:
        return _master_dictionary, _md_header, _sentiment_categories, _stopwords, _total_documents, ctg_stats
    else:
        return _master_dictionary


if __name__ == '__main__':
    # Full test program in /TextualAnalysis/TestPrograms/Test_Load_MasterDictionary.py
    print(time.strftime('%c') + '/n')
    md = '/Users/adrian_radulescu1997/Documents/Uni-Courses/DBPartTimeJob/crawler/temp_name/LoughranMcDonald_MasterDictionary_2014.csv'
    master_dictionary, md_header, sentiment_categories, stopwords, total_documents, CTG_STATS = load_masterdictionary(md, True, False, True, ctg_stats=CTG_STATS)
    print('\n' + 'Normal termination.')
    print(time.strftime('%c') + '/n')
