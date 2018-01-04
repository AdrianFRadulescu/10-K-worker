import csv
import requests
import os


def reformat(args=""):
    """
        Insert '\' before all '/' in the given string
        :param args = the string to be reformated
    """
    result = args.replace('\\','')
    import string
    for ch in args:
        if ch not in string.printable:
            result.replace(ch,'')
    return result

# 188800 188816

'''/Volumes/Seagate Backup Plus Drive/DBPartTime/SEC-Edgar-data/name.csv'''


def bulk_download(args={}, write_dir='', downloaded_files_count=0, register_file='name.csv', company='-', threshold='', recover=False):

    """
        Download 10-K files that are contained in the given database csv register file
    :param write_dir:               the location where the files will be written(downloaded) on this computer
    :param downloaded_files_count:  optional
    :param register_file:           the path to the csv register file
    :param company:                 download only files from the given company
    :param threshold:               alphabetical lower threshold
    :return:
    """
    if 'wdir' in args:
        write_dir = args['wdir']
    if 'csv' in args:
        register_file = args['csv']
    if 'comp' in args:
        company = args['comp']
    if 't' in args:
        threshold = args['t']

    downloaded_companies = []

    # get the companies for which the files have already been downloaded

    if not recover:
        downloaded_companies = sorted(os.listdir(write_dir))
    else:
        # dive into the files and check
        print "are files registered with cik number at the moment? y/n?"
        answer = raw_input()
        if answer == 'y':
            for cik_file in sorted(os.listdir(write_dir)):
                if write_dir[-1] != '/':
                    write_dir[-1] += '/'
                downloaded_companies += os.listdir(write_dir + cik_file)
            downloaded_companies = sorted(downloaded_companies)
        else:
            downloaded_companies = sorted(os.listdir(write_dir))

    print "nr of donwloaded companies = ", len(downloaded_companies)
    print "display first 150? y/n?"

    answer = raw_input()
    if answer == 'y':
        print downloaded_companies

    if write_dir[-1] is not '/':
        write_dir += '/'

    count = 1

    with open(register_file) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        prevName = ''

        companies = []
        errors = []

        for line in reader:

            if '10-K' in line[4] and '10-K/A' not in line[4]:
                if '/' in line[3]:
                    line[3] = reformat(line[3])
                if company in line[3]:
                    print line[3]
                if company is not '-' and \
                        (company not in line[3] or len(company) - len(line[3]) >= 4 or len(company) - len(line[3]) <= -4):
                    continue

                if threshold.lower() >= line[3].lower() or line[3] in downloaded_companies:
                    # if the name of a company is alphabetically lower than the threshold then skip downloading its 10-ks
                    continue

                print line[4], line[3]

                if not os.path.exists(write_dir + line[3]):
                    os.makedirs(write_dir + line[3])

                saveas = write_dir + line[3] + '/' + '-'.join([line[2], line[3], line[5]])

                try:
                    if not os.path.isfile(saveas):
                        # Reorganize to rename the output filename.
                        url = 'https://www.sec.gov/Archives/' + line[6].strip()
                        with open(saveas, 'wb') as f:
                            if count > downloaded_files_count:
                                f.write(requests.get('%s' % url).content)
                                #g.write('count = ' + str(count) + ' ' + url + ' downloaded and wrote to text file - year: ' + line[5] + '\n')
                                print count, (url, 'downloaded and wrote to text file - year: ', line[5])
                    else:

                        if count > downloaded_files_count:
                            url = 'https://www.sec.gov/Archives/' + line[6].strip()
                            #g.write('count = ' + str(count) + ' ' + url + ' downloaded and wrote to text file - year: ' + line[5]+ '\n')
                            print count, (url, 'downloaded and wrote to text file - year: ', line[5])

                    count +=1
                except IOError:
                    errors += [line]

        print "10-Ks downloaded with the following exceptions:"
        fw = open("misses.txt", "wb")

        for err in errors:
            print err
            fw.write(err + "\n")



if __name__ == "__main__":
    #bulk_download('utility_tests',company='APPLE COMPUTER INC')
    #bulk_download(write_dir='ut3',register_file='name.csv', threshold='TRICO')
    print reformat('TECHNOLOGY SERVICE GROUP INC \DE\\')