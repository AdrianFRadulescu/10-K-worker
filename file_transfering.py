import os
import shutil
from file_word_counting import get_file_company

def transfer_subdirs(source=os.getcwd(),dest=os.getcwd(), threshold=''):

    """
        Transfers subdirectories between given directories. If a treshold is given then only files which are alphabetically higher
        will be tranfered
    :param source:      the source directory
    :param dest:        the destination directory
    :param threshold:   the alphabetical treshold
    :return:
    """

    if source[-1] is not '/':
        source += '/'
    if dest[-1] is not '/':
        dest += '/'

    #iterate through the subdirectories in the source
    for dirname in os.listdir(source):
        if dirname[-1] is not '/':
            dirname += '/'

        if not os.path.isdir(source + dirname):
            continue

        if get_file_company(dirname.lower()) > get_file_company(threshold.lower()):
            #check if a corresponding directory exists in dest, otherwise make one
            if not os.path.isdir(dest + dirname):
                os.mkdir(dest + dirname)

            # descend into the directory
            for filename in os.listdir(source + dirname):
                print dest + dirname + filename
                if os.path.exists(dest + dirname + filename):
                    continue
                print 'Transfering ' + filename
                shutil.move(source + dirname + filename, dest + dirname)


if __name__ == "__main__":

    print get_file_company('1599407-1847 Holdings LLC-2015-04-15')
    #print transfer_subdirs('/Users/adrian_radulescu1997/Documents/Uni-Courses/DBPartTimeJob/crawler/csv_test')

    transfer_subdirs('/Users/adrian_radulescu1997/Documents/Uni-Courses/DBPartTimeJob/crawler/reports2', 'main_tests', '180 Connect Inc.')