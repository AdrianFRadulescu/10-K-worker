import os
import pickle
import csv_handling
import excel_handling
from file_word_counting import *


# parameters
parent_directory1 = '/Volumes/Seagate Backup Plus Drive/DBPartTime/SEC-Edgar-data/'
company1 = '17206'

file1 = 'word_count_test_summary.txt'

dir = '/Users/adrian_radulescu1997/Documents/Uni-Courses/DBPartTimeJob/crawler/reports3'

excel_reports_dir = "/Users/adrian_radulescu1997/Documents/Uni-Courses/DBPartTimeJob/crawler/excel_reports"
refined_excel_reports_dir= "/Users/adrian_radulescu1997/Documents/Uni-Courses/DBPartTimeJob/crawler/refined_excel_reports"


def set_up_accumulator(categories=None):

    categories_raw_scores = {}
    for cat in categories:
        categories_raw_scores[cat] = {}
        for w in categories[cat]:
            categories_raw_scores[cat][w] = 0

    return categories_raw_scores


def write_scores_to_file(file_name='',directory='', scores=None):

    if scores is not None:
        if not os.path.exists(directory + '/'):
            os.mkdir(directory + '')
        # total
        with open(directory + '/' + file_name, 'w') as fw:
            fw.write(beautify_report(scores))


def beautify_report(report=None):

    """
        Return a table containing the report in the fom of a string
    :param raw_report:
    :return:
    """
    if report is None:
        pass

    table = ''
    for cat in report:
        table += 10 * " " + cat
        table += 10 * " " + "|"
    table = table[:-1]
    table += '\n'

    # use the lists of elements for each category
    cats = map(lambda x: report[x], report)
    cat_nmaes = map(lambda x: x, report)

    for i in range(0, max(map(lambda x: len(report[x]), report))):
        table += '-' * 95 + '\n'
        for (n, l) in zip(cat_nmaes, cats):
            cell = '-' if i >= len(l) else list(l)[i] + ":" + str(report[n][list(l)[i]])
            # format the cell
            cell = (23 - len(cell)) / 2 * " " + cell \
                   + ((23 - len(cell)) / 2 if (23 - len(cell)) % 2 == 0 else (23 - len(cell)) / 2 + 1) * " "
            cell += '|'
            table += cell
        table = table[:-1] + '\n'
    return table


def rawscore_for_words_for_company(**kwargs):

    # some default inits

    parent_directory = '/Volumes/Seagate Backup Plus Drive/DBPartTime/SEC-Edgar-data/'
    company = '17206'
    write_dir = ''
    refined = False
    negative_words = []
    remove_range = 2
    excel_write_dir = '/Users/adrian_radulescu1997/Documents/Uni-Courses/DBPartTimeJob/crawler/refined_excel_reports'
    csv_write_dir = ''
    csv_report_file = 'csv_report.csv'
    report_type = 'excel'
    first_year = -1999
    last_year = -2016


    # check arguments
    if kwargs is not {}:
        if 'rdir' in kwargs:
            parent_directory = kwargs['rdir']
        if 'comp' in kwargs:
            company = (10 - len(kwargs['comp'])) * '0' + kwargs['comp']
        if 'categs' in kwargs:
            category_file = kwargs['categs']
        if 'wdir' in kwargs:
            write_dir = kwargs['wdir']
        if 'refined' in kwargs:
            refined = kwargs['refined']
        if 'nw' in kwargs:
            negative_words = kwargs['nw']
        if 'rmr' in kwargs:
            remove_range = kwargs['rmr']
        if 'ewdir' in kwargs:
            excel_write_dir = kwargs['ewdir']
        if 't' in kwargs:
            report_type = kwargs['t']
        if 'y' in kwargs:
            first_year = kwargs['y']
            last_year  = kwargs['y']
        if 'fy' in kwargs:
            first_year = kwargs['fy']
        if 'ly' in kwargs:
            last_year = kwargs['ly']
        if 'csvwdir' in kwargs:
            csv_write_dir = kwargs['csvwdir']
        if 'csvrf' in kwargs:
            csv_report_file = kwargs['csvrf']

    if parent_directory[-1] is not '/':
        parent_directory += '/'
    if csv_write_dir[-1] is not '/':
        csv_write_dir += '/'
    if excel_write_dir[-1] is not '/':
        excel_write_dir += '/'
    if write_dir is not '' and write_dir[-1] is not '/':
        write_dir += '/'

    #print 'type: ' + report_type

    #categories = pickle.load(open(category_file, 'rb'))
    if kwargs['defcat']:
        categories = {'CRE': ['adapt', 'begin', 'chang', 'creat', 'discontin', 'dream', 'elabor', 'entrepre', 'envis', 'experim', 'fantas', 'freedom', 'futur', 'idea', 'init', 'innovat', 'intellec', 'learn', 'new', 'origin', 'pioneer', 'predict', 'radic', 'risk', 'start', 'thought', 'trend', 'unafra', 'ventur', 'vision'], 'COM': ['achiev', 'acqui', 'aggress', 'agreem', 'attack', 'budget', 'challeng', 'charg', 'client', 'compet', 'customer', 'deliver', 'direct', 'driv', 'excellen', 'expand', 'fast', 'goal', 'growth', 'hard', 'invest', 'market', 'mov', 'outsourc', 'performanc', 'position', 'pressur', 'profit', 'rapid', 'reputation', 'result', 'revenue', 'satisf', 'scan', 'succes signal', 'speed', 'strong', 'superior', 'target', 'win'], 'COL': ['boss', 'burocr', 'cautio', 'cohes', 'certain', 'chief', 'collab', 'conservat', 'cooperat', 'detail', 'document', 'efficien', 'error', 'fail', '', 'help', 'human', 'inform', 'logic', 'method', 'outcom', 'partner', 'people', 'predictab', 'relation', 'qualit', 'regular', 'solv', 'share', 'standard', 'team', 'teamwork', 'train', 'uniform', 'work group'], 'CON': ['capab', 'collectiv', 'commit', 'competenc', 'conflict', 'consens', 'control', 'coordin', 'cultur', 'decentr', 'employ', 'empower', 'engag', 'expectat', 'facilitator', 'hir', 'interpers', 'involv', 'life', 'long-term', 'loyal', 'mentor', 'monit', 'mutual', 'norm', 'parent', 'partic', 'procedur', 'productiv', 'retain', 'reten', 'skill', 'social', 'tension', 'value']}
    else:
        import categories_key_words_reading
        categories = categories_key_words_reading.get_categories(kwargs['categs'])
    #print categories

    # setup the accumulator for the results

    categories_raw_scores = set_up_accumulator(categories)
    categories_refined_scores = set_up_accumulator(categories)

    #print categories_raw_scores

    # find raw scores for each word for the given company

    if not os.path.isdir(parent_directory + company):
        print parent_directory + company
        print 'Wrong rdir specified'
        pass

    else:

        # get the years in which there are multiple files
        import collections
        files = os.listdir(parent_directory+company)
        special_years = [item for item, count in collections.Counter(files).items() if count > 1]

        print "sy = ", special_years
        for file in files:

            print get_file_year_from_content(parent_directory + company + '/' + file)
            print first_year > 0 and get_file_year_from_content(parent_directory + company + '/' + file) not in range(first_year,last_year+1)

            if first_year > 0 and get_file_year_from_content(parent_directory + company + '/' + file) not in range(first_year,last_year+1):
                continue
            print "check passed"
            if 'DS_Store' in file:
                continue

            # quick content check

            data = open(parent_directory + company + '/' + file, 'r').read().split('\n')[:50]

            ignore = False

            for line in data:
                if ('CONFORMED SUBMISSION TYPE:' and '/A' in line)\
                        or ('CONFORMED SUBMISSION TYPE:' in line and not any(map(lambda s: s in line, ['10-K', '10-K405', '10-KSB']))):
                    ignore = True
                    continue

            if ignore:
                print 'Ignoring {}, file {}, 10-K/A'.format(company, file)
                continue

            # check file size
            if count_words_in_text(beautify_data(read_text_from_file_without_tables(parent_directory + company + '/' + file))) < 2000:
                print 'Ignoring {}, file {}, word number smaller than 2000'.format(company, file)
                continue

            #print 'file= ', file

            refined_word_freqs = None
            word_freqs = None

            if kwargs['c_item7']:

                # get the refined word frequencies from item 7
                refined_word_freqs = get_item_7_word_frequencies_from_file(directory=parent_directory + company, file=file,
                                                                   refined=True, negative_words=negative_words,
                                                                   remove_range=remove_range)

                # get the word frequencies from the item 7
                word_freqs = get_item_7_word_frequencies_from_file(directory=parent_directory + company, file=file,
                                                                   refined=False)

            # get the word frequencies from the whole file
            text_word_freqs = get_text_word_frequencies_from_file(directory=parent_directory + company, file=file,
                                                                  refined=False, remove_range=remove_range,
                                                                  negative_words=negative_words)

            # get the refined word frequencies from the whole file
            refined_text_word_freqs = get_text_word_frequencies_from_file(directory=parent_directory + company, file=file,
                                                                  refined=True, remove_range=remove_range,
                                                                  negative_words=negative_words)

            print "twf = ", text_word_freqs.values()
            print "i7wf = ", word_freqs.values()

            # reinitialise
            categories_raw_scores = set_up_accumulator(categories)
            categories_refined_scores = set_up_accumulator(categories)

            if kwargs['c_item7']:
                # calculate raw and refined scores for item 7

                for cat in categories_raw_scores:
                    for w in categories_raw_scores[cat]:
                        if refined_word_freqs.match(w):
                            categories_raw_scores[cat][w] += sum(list(word_freqs.values(w)))

                for cat in categories_refined_scores:
                    for w in categories_refined_scores[cat]:
                        if refined_word_freqs.match(w):
                            categories_refined_scores[cat][w] += sum(list(refined_word_freqs.values(w)))

            else:
                # calculate raw and refined scores for the whole text
                for cat in categories_raw_scores:
                    for w in categories_raw_scores[cat]:
                        if refined_word_freqs.match(w):
                            categories_raw_scores[cat][w] += sum(list(text_word_freqs.values(w)))

                for cat in categories_refined_scores:
                    for w in categories_refined_scores[cat]:
                        if refined_word_freqs.match(w):
                            categories_refined_scores[cat][w] += sum(list(refined_text_word_freqs.values(w)))

            if report_type == 'excel' and (categories_raw_scores is not None or categories_refined_scores is not None):

                # make excel report
                if not word_freqs == {}: # still not the best way to handle this. A better one needs to be found

                    report_name = excel_write_dir + company + '/' + company + '.xlsx'
                    out_wb, out_ws = excel_handling.get_file(filedir=excel_write_dir+company, filename=report_name, company=company)
                    excel_handling.complete_report_for_year(
                        work_sheet=out_ws, year=get_file_year(file=file),
                        report_dictionary=categories_raw_scores,
                        freq_automaton=word_freqs,
                        file_word_freq_automaton=text_word_freqs
                    )
                    out_wb.save(report_name)
            elif report_type == 'csv' and (categories_raw_scores is not None or categories_refined_scores is not None):

                # add report as line to csv file
                if not len(list(word_freqs.values())) == 0:
                    report_name = csv_handling.get_file(csv_write_dir, csv_report_file)
                    csv_handling.add_year_report_as_row_to_csv_file(
                        file_path=report_name,
                        cik=get_cik(file=file),
                        company=get_company_name(file),
                        year=get_file_year_from_content(parent_directory + company + '/' + file),
                        report_dictionary=categories_raw_scores,
                        refined_report_dictionary=categories_refined_scores,
                        item_7_word_freq_automaton=word_freqs,
                        file_word_freq_automaton=text_word_freqs
                    )
            else:
                print 'HERE'
                write_scores_to_file(directory=write_dir + company, file_name=file, scores=categories_raw_scores)

    return categories_raw_scores


# just for testing purposes
def get_raw_scores_for_n_companies(directory='', n=0, write_dir='', refined=False, negative_words=[], remove_range=2,
                                   excel_write_dir=''):

    count = 0

    if not os.path.isdir(directory):
        pass
    else:
        for company in os.listdir(directory):
            crs = rawscore_for_words_for_company(parent_directory=directory, company=company, write_dir=write_dir+'/'+company,
                                                 refined=True, negative_words=negative_words, remove_range=remove_range,
                                                 excel_write_dir=excel_write_dir)
            count += 1
            print count
            if n > 0 and count > n:
                break


if __name__ == "__main__":

    negative_words = ['not', 'less', 'nothing', 'no', 'never', 'negative', 'nobody', 'nondescript', 'futile',
                      'unnecessary', 'useless']

    #tst(parent_directory1,'Zoro Mining Corp.')
    #tst(parent_directory1, 1, dir)

    get_raw_scores_for_n_companies(
        parent_directory1, 1, dir, refined=True, negative_words=negative_words,remove_range=2,
        excel_write_dir='/Users/adrian_radulescu1997/Documents/Uni-Courses/DBPartTimeJob/crawler/csv_reports'
    )

