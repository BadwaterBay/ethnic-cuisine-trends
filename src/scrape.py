# %%

import pandas as pd
import matplotlib as plt
import time
import pickle
from pytrends.request import TrendReq
pytrend = TrendReq()


class Trend:
    # Required:
    # import pandas as pd
    # import pickle
    # import matplotlib.pyplot as plt
    # from pytrends.request import TrendReq
    # pytrend = TrendReq()

    def __init__(self, year, month, kwList):
        self.year = year
        self.month = month
        self.kwList = kwList

    def monthEndDate(self):
        switcher = {
            1: 31,
            2: 28,
            3: 31,
            4: 30,
            5: 31,
            6: 30,
            7: 31,
            8: 31,
            9: 30,
            10: 31,
            11: 30,
            12: 31,
        }
        if ((self.year % 4 == 0) and (self.month == 2)):
            switcher[2] = 29
        return switcher.get(self.month)

    def timeframe(self):
        date_start = str(self.year) + '-' + str(self.month) + '-01'
        date_end = str(self.year) + '-' + str(self.month) + \
            "-" + str(self.monthEndDate())
        return date_start + ' ' + date_end

    def scrape(self):
        pytrend.build_payload(self.kwList, timeframe=self.timeframe())
        self.trend = (pytrend.interest_by_region()).reset_index()

    def toPickle(self, keyword, path):
        keyword = keyword.replace(' ', '-')
        monthStr = '0' + \
            str(self.month) if self.month < 10 else str(self.month)
        fileName = str(self.year) + '-' + monthStr + '-' + str(keyword)
        pathName = str(path) + '/' + fileName + '.pkl'
        with open(pathName, 'wb') as f:
            pickle.dump(self.trend, f)

    def preview(self):
        print("Head:")
        print(self.trend.head(10))
        print("..............................")
        print("Tail:")
        print(self.trend.tail(10))

    def hist(self):
        plt.figure(figsize=(8, 6))
        for i in range(1, len((self.trend).columns)):
            plt.hist((self.trend).iloc[:, i], range=(
                0, 100), bins=10, alpha=0.3, label=(self.trend).columns[i])
        plt.title(str(self.year) + '-' + str(self.month))
        plt.ylabel('Frequency')
        plt.legend()
        plt.show()

    def scatter(self):
        plt.figure(figsize=(8, 6))
        for i in range(1, len((self.trend).columns)):
            plt.scatter(x=(self.trend).index, y=(
                self.trend).iloc[:, i], s=4, alpha=0.5, label=(self.trend).columns[i])
        plt.title(str(self.year) + '-' + str(self.month))
        plt.ylabel('Trending index')
        plt.legend()
        plt.show()


# %%

def main():
    kw_list = ['"Canon" "mirrorless"', '"Nikon" "mirrorless"', '"Sony" "mirrorless"']
    # kw_list = ['%2Fm%2F01xw9', '%2Fm%2F051zk',
    #            '%2Fm%2F09y2k2', '%2Fm%2F07hxn', '%2Fm%2F01h5q0']

    for y in range(2020, 2021):
        for m in range(1, 13):
            if (y == 2020 and m > 3):
                break
            while True:
                try:
                    t = Trend(y, m, kw_list)
                    t.scrape()
                    t.toPickle('testing', 'data/raw/test')
                    t.scatter()
                    print(str(y) + '-' + str(m) + ': DONE')
                    time.sleep(0.1)  # in seconds
                    break
                except:
                    print("Error caught. Going to pause for some duration...")
                    time.sleep(3)

if __name__ == '__main__':
    print('Start!')
    main()
