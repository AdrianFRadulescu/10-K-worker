# -*- coding: utf-8 -*-

import unicodedata
import string
import urllib
import os
from bs4 import BeautifulSoup
from file_word_counter_test import read_text_from_file_without_tables
import re
import sys



if __name__ == "__main__":

    for x in sys.argv:
        print x