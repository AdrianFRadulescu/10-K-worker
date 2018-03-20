'''

This script takes the location of a filesystem and
iterates through them inserting the relative path(to the filesystem of a file)
into a table in a newly created database


'''

from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlalchemy.exc as sqlexec
import mysql.connector.errors as mysqlerrors
from aux_functions import *
import csv

"""
    USER DEFINED ENVIRONMENT

    COMPLETE THIS SECTION WITH THE APPROPRIATE PATHS AND VALUES FOR YOUR PC

"""

# the username for the database
USER = 'mockadmin'

# the file containing the password for the user
PASSWORD_FILE = '/Users/adrian_radulescu1997/Documents/Uni-Courses/DBPartTimeJob/crawler/temp_name/database/db_pass'

# the password for the selected user
with open(PASSWORD_FILE, 'r') as f_in:
    PASSWORD = f_in.read()

# the database identifier
DATABASE = 'mysql+mysqlconnector://'+ USER + ':' + PASSWORD + '@localhost/10_Ks'

BASE = declarative_base()


class Files(BASE):

    __tablename__ = 'Files'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    year = Column(Integer)
    company = Column(String)
    CIK = Column(String)
    path = Column(String, unique=True)
    conformed_period_of_report = Column(String)


def get_file_location_by_name(filename=''):

    """
        Returns the location of the file in the filesystem
    :param file_name:
    :return:
    """

    session = sessionmaker(bind=create_engine(DATABASE, echo=True))()

    try:
        path = session.query(Files.path).filter_by(name=filename).first().path
        print(path)
    except AttributeError:
        path = ''
    finally:
        session.close()
    return path


def is_file_in_database(filepath=''):

    """
        Checks whether the file identified by the given filepath is in the db
    :param filepath:
    :return:
    """

    session = sessionmaker(bind=create_engine(DATABASE, echo=True))()

    try:
        path = session.query(Files.path).filter_by(path=filepath).first().path
        print(path)
    except AttributeError:
        path = ''
    finally:
        session.close()

    if path == '':
        return False

    return True


def get_file_locations_by_cik(cik=''):

    session = sessionmaker(bind=create_engine(DATABASE, echo=True))()

    paths = list(map(lambda t: t.path, session.query(Files.path).filter_by(CIK=cik).order_by(Files.year).all()))

    session.close()

    return paths


def get_files_by_ciks(cikfile=''):

    with open(cikfile) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')

        ciks = []

        for line in reader:
            for cik in line:
                if cik is not '':
                    ciks += [cik]

    filelist = []

    for cik in ciks:
        filelist += get_file_locations_by_cik(cik)

    return filelist


def get_file_company_by_name(filename=''):

    """
        Return the company of the file
    :param file_name:
    :return:
    """
    session = sessionmaker(bind=create_engine(DATABASE, echo=True))()

    company = session.query(Files.company).filter_by(name=filename).first().company

    session.close()
    return company


def add_file_data_to_db(**kwargs):

    session = sessionmaker(bind=create_engine(DATABASE, echo=True))()

    try:


        session.add(
            Files(
                name=kwargs['filename'],
                year=get_file_year_from_content(kwargs['filepath']),
                company=get_company_name_from_content(kwargs['filepath']),
                CIK=get_cik_from_content(kwargs['filepath']),
                path=kwargs['filepath'],
                conformed_period_of_report=get_conformed_period_of_report_from_content(kwargs['filepath'])
            )
        )

    except:
        print('File might already be in the Database')
        session.rollback()

    finally:
        session.commit()
        session.close()


def run_sql_select(sql=''):

    if 'select' not in sql and 'SELECT' not in sql:

        print('wrong query type')
        return

    else:
        session = sessionmaker(bind=create_engine(DATABASE, echo=True))()

        query_result = session.execute(sql)

        result = []

        for row in query_result:
            result += [{}]

            for key in row.iterkeys():
                result[-1][key] = row[key]

        session.close()

    return result


def execute_sql(sql=''):

    if 'update' not in sql and 'UPDATE' not in sql:
        return

    else:
        session = sessionmaker(bind=create_engine(DATABASE, echo=True))()

        session.execute(sql)

        session.commit()
        session.close()


if __name__ == "__main__":

    """
    file = '/Users/adrian_radulescu1997/Documents/Uni-Courses/DBPartTimeJob/crawler/temp_name/database/db_pass'

    with open(file, 'r') as f_in:
        doc = f_in.read()

    engine1 = create_engine('mysql+mysqlconnector://mockadmin:' + doc + '@localhost/10_Ks', echo=True)

    Session = sessionmaker(bind=engine1)
    session = Session()

    Base = declarative_base()


    # declare model

    class Proto(Base):

        __tablename__ = 'proto'

        id = Column(Integer, primary_key=True)
        name = Column(String)


    session.add(Proto(id=4, name='Naruto'))

    session.commit()

    result = session.query(Proto)

    for row in result:
        print(str(row.id) + ' ' + row.name)

    session.close()

    print(get_file_location_by_name('20130103_10-K_edgar_data_1411179_0001165527-13-000010_1.txt'))
    print(get_file_company_by_name('20130103_10-K_edgar_data_1411179_0001165527-13-000010_1.txt'))

    result1 = run_sql_select('SELECT COUNT(*) FROM files')

    print(result1)
    """

    #print(get_files_by_ciks('/Users/adrian_radulescu1997/Documents/Uni-Courses/DBPartTimeJob/crawler/temp_name/ciks'))

    #print(is_file_in_database(filepath='/Users/adrian_radulescu1997/Documents/Uni-Courses/DBPartTimeJob/crawler/temp_name/Adrian_10-Ks/EDGAR/10-X_C/2006/QTR2/20060414_10KSB_edgar_data_1167419_0001079973-06-000223_1.txt'))

    from pprint import pprint

    #pprint(get_file_locations_by_cik(cik='0000773717'))
    pprint(get_files_by_ciks('/Users/adrian_radulescu1997/Documents/Uni-Courses/DBPartTimeJob/crawler/temp_name/ciks'))