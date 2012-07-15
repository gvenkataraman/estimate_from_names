"""
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without
limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
OR OTHER DEALINGS IN THE SOFTWARE.
"""
from __future__ import division

from collections import defaultdict
import pandas as pd
import sys


def get_all_names():
    years = xrange(1999, 2012)
    pieces = []
    columns = ['name', 'sex', 'births']
    for year in years:
        path = 'names/yob%d.txt' % year
        frame = pd.read_csv(path, names=columns)
        frame['year'] = year
        pieces.append(frame)
    names = pd.concat(pieces, ignore_index=True)
    return names


def get_indian_names_set():
    fname = sys.argv[1]
    fptr = open(fname, 'rb')
    indian_names = set()
    for line in fptr:
        words = line.split(' ')
        if words[0]:
            indian_names.add(words[0][:-1].lower())

    return indian_names


if __name__ == '__main__':
    """
    python estimate_names.py <indian_names>
    """
    # data from wikipedia
    p2_actual = 2843391
    p1_actual = 1678765

    actual_rate = 100 * (p2_actual - p1_actual) / p1_actual
    print 'actual rate ', actual_rate
    names = get_all_names()
    interesting_names = get_indian_names_set()

    numb_names = len(names.name)
    year_to_births = defaultdict(int)
    name_to_births = defaultdict(int)

    for index in xrange(numb_names):
        name = names.name[index]
        if not name:
            continue
        if name.lower() in interesting_names:
            year_to_births[int(names.year[index])] += int(names.births[index])
            name_to_births[name.lower()] += int(names.births[index])

    p2_predict = year_to_births[2010]
    p1_predict = year_to_births[2000]

    predicted_rate = (p2_predict - p1_predict) / (p1_predict)

    predicted_population = p1_actual * (p2_predict / p1_predict)

    error = 100 * (predicted_population - p2_actual) / p2_actual

    print 'predicted rate ', predicted_rate
    print 'actual population: ', p2_actual
    print 'predicted population ', predicted_population
    print 'error ', error
