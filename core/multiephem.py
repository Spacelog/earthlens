from __future__ import division, absolute_import, print_function, unicode_literals
from datetime import datetime, timedelta
from bisect import bisect

class MultiEphem(object):
    """ Given a file of historical two-line orbital elements, select the
        correct set for a given date. """

    def get_elements_for_date(self, time):
        result = bisect(self.available_dates, time)
        return self.elements[self.available_dates[result]]

    def load_elements(self, elements):
        self.elements = {}
        self.available_dates = []
        for tle in elements:
            year = int(tle[0][18:20])
            if year > 61:
                year = year + 1900
            else:
                year = year + 2000
            doy = int(tle[0][21:23])
            day_frac = float("0." + tle[0][24:32])
            date = datetime(year, 1, 1) + timedelta(days=doy, seconds=int(day_frac * 86400))
            self.elements[date] = tle
            self.available_dates.append(date)
        self.available_dates.sort()

    def load_elements_from_list(self, elements_data):
        elements = []
        for index in range(0, len(elements_data), 2):
            if elements_data[index] == '':
                continue
            elements.append(elements_data[index:index+2])
        self.load_elements(elements)

if __name__ == '__main__':
    me = MultiEphem()
    with open('iss.elements', 'r') as fh:
        data = fh.read().split("\n")
        me.load_elements_from_list(data)

    print(me.get_elements_for_date(datetime(2013, 2, 3, 16, 02, 00)))
