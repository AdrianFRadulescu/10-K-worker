# -*- coding: utf-8 -*-

import unicodedata
import string
import urllib
import os
from bs4 import BeautifulSoup
from file_word_counter_test import read_text_from_file_without_tables
import re





print os.path.exists('/Volumes/Seagate Backup Plus Drive/DBPartTime/SEC-Edgar-data/APPLE/')
print os.listdir('/Volumes/Seagate Backup Plus Drive/DBPartTime/SEC-Edgar-data/APPLE/')

l = os.listdir('/Volumes/Seagate Backup Plus Drive/DBPartTime/SEC-Edgar-data/APPLE/')[1:]
file_path1 = '/Volumes/Seagate Backup Plus Drive/DBPartTime/SEC-Edgar-data/APPLE/' + l[16]

print l[16]


x = l[16]
print int(list(filter(lambda a: a.isdigit() and len(a) is 4, x.split('-')))[0])


'''
# kill all script and style elements
for script in soup(["script", "style"]):
    script.extract()    # rip it out

# get text
text = soup.get_text()
'''

#print text
