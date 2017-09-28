import os
import pickle
import csv_handling
import excel_handling
from file_word_counter_test import *


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
        #print cat
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


def rawscore_for_words_for_company(args={}, parent_directory='/Volumes/Seagate Backup Plus Drive/DBPartTime/SEC-Edgar-data/',
                                   company='17206',
                                   category_file='categories.pkl',
                                   write_dir='', refined=False,
                                   negative_words=[],
                                   remove_range=2,
                                   excel_write_dir='/Users/adrian_radulescu1997/Documents/Uni-Courses/DBPartTimeJob/crawler/refined_excel_reports',
                                   csv_write_dir='',
                                   csv_report_file='csv_report.csv',
                                   report_type='excel',
                                   first_year=-1999, last_year=-2016):
    # check arguments
    if args is not {}:
        if 'rdir' in args:
            parent_directory = args['rdir']
        if 'comp' in args:
            company = (10 - len(args['comp'])) * '0' + args['comp']
        if 'categs' in args:
            category_file = args['categs']
        if 'wdir' in args:
            write_dir = args['wdir']
        if 'refined' in args:
            refined = args['refined']
        if 'nw' in args:
            negative_words = args['nw']
        if 'rmr' in args:
            remove_range = args['rmr']
        if 'ewdir' in args:
            excel_write_dir = args['ewdir']
        if 't' in args:
            report_type = args['t']
        if 'y' in args:
            first_year = args['y']
            last_year  = args['y']
        if 'fy' in args:
            first_year = args['fy']
        if 'ly' in args:
            last_year = args['ly']
        if 'csvwdir' in args:
            csv_write_dir = args['csvwdir']
        if 'csvrf' in args:
            csv_report_file = args['csvrf']

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
    categories = {'CRE': ['adapt', 'begin', 'chang', 'creat', 'discontin', 'dream', 'elabor', 'entrepre', 'envis', 'experim', 'fantas', 'freedom', 'futur', 'idea', 'init', 'innovat', 'intellec', 'learn', 'new', 'origin', 'pioneer', 'predict', 'radic', 'risk', 'start', 'thought', 'trend', 'unafra', 'ventur', 'vision'], 'COM': ['achiev', 'acqui', 'aggress', 'agreem', 'attack', 'budget', 'challeng', 'charg', 'client', 'compet', 'customer', 'deliver', 'direct', 'driv', 'excellen', 'expand', 'fast', 'goal', 'growth', 'hard', 'invest', 'market', 'mov', 'outsourc', 'performanc', 'position', 'pressur', 'profit', 'rapid', 'reputation', 'result', 'revenue', 'satisf', 'scan', 'succes signal', 'speed', 'strong', 'superior', 'target', 'win'], 'COL': ['boss', 'burocr', 'cautio', 'cohes', 'certain', 'chief', 'collab', 'conservat', 'cooperat', 'detail', 'document', 'efficien', 'error', 'fail', '', 'help', 'human', 'inform', 'logic', 'method', 'outcom', 'partner', 'people', 'predictab', 'relation', 'qualit', 'regular', 'solv', 'share', 'standard', 'team', 'teamwork', 'train', 'uniform', 'work group'], 'CON': ['capab', 'collectiv', 'commit', 'competenc', 'conflict', 'consens', 'control', 'coordin', 'cultur', 'decentr', 'employ', 'empower', 'engag', 'expectat', 'facilitator', 'hir', 'interpers', 'involv', 'life', 'long-term', 'loyal', 'mentor', 'monit', 'mutual', 'norm', 'parent', 'partic', 'procedur', 'productiv', 'retain', 'reten', 'skill', 'social', 'tension', 'value']}
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

        for file in files:

            if first_year > 0 and get_file_year(file) not in range(first_year,last_year+1) or get_file_year(file) >= 2017:
                continue

            if 'DS_Store' in file:
                continue

            if get_file_year(file) in special_years:
                data = open(file, 'r').split('\n')[:100]

                for line in data:
                    if 'CONFORMED SUBMISSION TYPE:' and '/A' in line:
                        continue

                """
                    SEE IF FILE IS PROBLEMATIC
                """


            #print 'file= ', file

            # get the refined word frequencies from item 7
            refined_word_freqs = get_item_7_word_frequencies_from_file(directory=parent_directory + company, file=file,
                                                               refined=True, negative_words=negative_words,
                                                               remove_range=remove_range)

            # get the word frequencies from the item 7
            word_freqs = get_item_7_word_frequencies_from_file(directory=parent_directory + company, file=file,
                                                               refined=False)

            # get the word frequencies from the whole file
            text_word_freqs = get_text_word_frequencies_from_file(directory=parent_directory + company, file=file,
                                                                  refined=False,remove_range=remove_range,
                                                                  negative_words=negative_words)

            # reinitialise
            categories_raw_scores = set_up_accumulator(categories)
            categories_refined_scores = set_up_accumulator(categories)


            # calculate raw scores
            for cat in categories:
                for w in categories_raw_scores[cat]:
                    if word_freqs.match(w):
                        categories_raw_scores[cat][w] += sum(list(word_freqs.values(w)))

            # calcualte refined scores
            for cat in categories:
                for w in categories_refined_scores[cat]:
                    if refined_word_freqs.match(w):
                        categories_refined_scores[cat][w] += sum(list(refined_word_freqs.values(w)))

            if report_type == 'excel':

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

            elif report_type == 'csv':

                # add report as line to csv file
                if not len(list(word_freqs.values())) == 0:
                    report_name = csv_handling.get_file(csv_write_dir, csv_report_file)
                    csv_handling.add_year_report_as_row_to_csv_file(
                        file_path=report_name,
                        cik=get_cik(file=file),
                        company=get_company_name(file),
                        year=get_file_year(file),
                        report_dictionary=categories_raw_scores,
                        refined_report_dictionary=categories_refined_scores,
                        item_7_word_freq_automaton=word_freqs,
                        file_word_freq_automaton=text_word_freqs
                    )
            else:
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
        parent_directory1, 1, dir,refined=True, negative_words=negative_words,remove_range=2,
        excel_write_dir='/Users/adrian_radulescu1997/Documents/Uni-Courses/DBPartTimeJob/crawler/csv_reports'
    )

