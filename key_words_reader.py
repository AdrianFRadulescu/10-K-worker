import pickle
import re

fr = open('/Users/adrian_radulescu1997/Documents/Uni-Courses/DBPartTimeJob/crawler/Culture type Bag of words.txt', 'r')

categories = {}
current_category = ''

for line in fr.readlines():

    if any(map(lambda ch: ch.isdigit() or ch.isalpha(),line)):

        if line[0] == 'C':
            if '(' not in line:
                continue
            else:
                current_category = re.findall(r'\(.*?\)', line)[0].replace('(', '').replace(')', '')
                categories[current_category] = []

        else:
            for word in line.split(','):
                categories[current_category] += [word.replace(' ', '', 1).replace('\n', '')]


for c in categories:
    print c, categories[c]

pickle.dump(categories, open('categories.pkl','wb'))
print categories