import datetime
import sqlite3
import requests
import pandas
from sqlalchemy import create_engine
import os


def update_database(write_dir=''):

    if write_dir[-1] is not '/':
        write_dir += '/'

    # Generate the list of index files archived in EDGAR since start_year (earliest: 1993) until the most recent quarter
    csvfiles = [] # a list of all temporary files that will be created and then appended
    for (sty,cy) in [(1993,2011), (2011,2014), (2014,2015), (2015,2017)]:
        current_year = cy
        start_year = sty
        years = list(range(start_year, current_year))
        quarters = ['QTR1', 'QTR2', 'QTR3', 'QTR4']
        history = [(y, q) for y in years for q in quarters]
        urls = ['https://www.sec.gov/Archives/edgar/full-index/%d/%s/master.idx' % (x[0], x[1]) for x in history]
        urls.sort()

        # Download index files and write content into SQLite

        con = sqlite3.connect('edgar_idx.db')
        cur = con.cursor()
        cur.execute('DROP TABLE IF EXISTS idx')
        cur.execute('CREATE TABLE idx (cik TEXT, conm TEXT, type TEXT, date TEXT, path TEXT)')

        for url in urls:
            lines = requests.get(url).text.splitlines()
            records = [tuple(line.split('|')) for line in lines[11:]]
            cur.executemany('INSERT INTO idx VALUES (?, ?, ?, ?, ?)', records)
            print(url, 'downloaded and wrote to SQLite')

        con.commit()
        con.close()

        # Write SQLite database to Statae

        engine = create_engine('sqlite:///edgar_idx.db')
        with engine.connect() as conn, conn.begin():
            data = pandas.read_sql_table('idx', conn)
            data.to_stata('edgar_idx.dta')

        ex = pandas.read_stata('edgar_idx.dta')
        csvexfile = write_dir + "name" + str(start_year) + "-" + str(current_year) + ".csv"
        ex.to_csv(csvexfile)
        csvfiles += [csvexfile]

        os.remove('edgar_idx.db')
        os.remove('edgar_idx.dta')
        print str(sty) + '-' + str(cy), ': finished downloading'

    from csv_handling import append_files

    append_files(write_dir + "name.csv", csvfiles)

    # delete the auxiliary files
    for csvfile in csvfiles:
        os.remove(csvfile)

if __name__ == '__main__':

    update_database(write_dir='utility_tests')
