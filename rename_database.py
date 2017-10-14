import os
import sys

"""
    This is a separate mini-script for renaming the files folders/directories in the
    current database
"""
from file_word_counting import get_cik

if __name__ == "__main__":

    for dir in os.listdir(sys.argv[1]):
        os.rename(sys.argv[1] + '/' + dir, sys.argv[1] + '/' +get_cik(os.listdir(sys.argv[1] + '/' + dir)[0]))
