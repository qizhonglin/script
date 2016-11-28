#!/usr/bin/python

import csv

def write_csv():
    with open('data/some.csv', 'wb') as f:
        writer = csv.writer(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['a', '1', '2'])
        writer.writerow(['b', '2', '3'])


def read_csv():
    with open('data/some.csv', 'rb') as f:
        reader = csv.reader(f, delimiter=' ', quotechar='|')
        for row in reader:
	    print ','.join(row)


if __name__ == '__main__':
    write_csv()
    read_csv()
