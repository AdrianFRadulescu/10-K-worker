import pickle
import re


def get_categories(file_path='/Users/adrian_radulescu1997/Documents/Uni-Courses/DBPartTimeJob/crawler/Culture type Bag of words.ctg'):

    """
        Reads a .ctg file to extract the words for the contained categories and organizes
        them into a dictionary
    :param file_path: the path to the file
    :return: a dictionary of the categories and their associated words
    """


    fr = open(file_path, 'r')

    categories = {}
    current_category = ''

    comment_tag = False

    for line in fr.readlines():

        if '\'\'\'' in line:
            continue

        if '->Category' in line:
            current_category = re.findall(r'\(.*?\)', line)[0].replace('(', '').replace(')', '')
            categories[current_category] = []

        if '-->>words' in line:
                for word in line.split(':')[1].split(','):
                    categories[current_category] += [word.replace(' ', '', 1).replace('\n', '')]

    return categories

if __name__ == "__main__":

    from pprint import pprint
    pprint(get_categories())