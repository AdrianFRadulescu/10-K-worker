import os
import sys

"""
    This is a separate mini-script for renaming the files folders/directories in the
    current database
"""
from file_word_counting import get_cik

if __name__ == "__main__":

    f = open(sys.argv[1] + '/company_ciks', "w")

    f.write("Company" + 36 * " " + "CIK" + "\n")
    line_delim = "-"*(len("company") + 35 + 11 + 6) + "\n"
    f.write(line_delim)
    for directory in os.listdir(sys.argv[1]):

        if os.path.isdir(sys.argv[1] + '/' + directory):
            print directory
            f.write(directory + (42 - len(directory)) * " " + "|" + " " + get_cik(os.listdir(sys.argv[1] + '/' + directory)[0]) + "\n")
            os.rename(sys.argv[1] + '/' + directory, sys.argv[1] + '/' + get_cik(os.listdir(sys.argv[1] + '/' + directory)[0]))
            f.write(line_delim)