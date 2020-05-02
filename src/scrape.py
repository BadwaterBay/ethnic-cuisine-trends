# %%
# hayleydummy
print('Initiating...')

import pandas as pd
import matplotlib.pyplot as plt
import time
import pickle
from pytrends.request import TrendReq
pytrend = TrendReq()

print('Finished importing modules')

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

    def scrape(self, toPlain={}):
        pytrend.build_payload(self.kwList, timeframe=self.timeframe(), geo='US')
        results = (pytrend.interest_by_region(resolution='REGION')).reset_index()
        if toPlain:
            results = results.rename(columns=toPlain)
        self.trend = results

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

print('Prep work done!')

# %%

def main():
    # kw_list = ['"Canon" "mirrorless"', '"Nikon" "mirrorless"', '"Sony" "mirrorless"']
    kw_list = ["/m/01xw9", "/m/051zk", "/m/09y2k2", "/m/07hxn", "/m/01h5q0"]
    col_convert = {"/m/01xw9": "Chinese cuisine",
                   "/m/051zk": "Mexican cuisine",
                   "/m/09y2k2": "Italian cuisine",
                   "/m/07hxn": "Thai cuisine",
                   "/m/01h5q0": "Indian cuisine"}
    # kw_list = ['chinese cuisine', 'mexican cuisine', '/m/01xw9']

    for y in range(2004, 2021):
        for m in range(1, 13):
            if (y == 2020 and m > 3):
                break
            while True:
                try:
                    print('Starting to scrap: ' + str(y) + '-' + str(m))
                    t = Trend(y, m, kw_list)
                    t.scrape(toPlain=col_convert)
                    print('Previewing data: ' + str(y) + '-' + str(m))
                    t.preview()
                    t.toPickle('cuisine', './data/raw')
                    t.scatter()
                    print('Just finished scraping: ' + str(y) + '-' + str(m))
                    time.sleep(0.1)  # in seconds
                    break
                except:
                    t_pause = 30
                    print('Error caught. Going to pause for ' + str(t_pause) + 'seconds and retry scraping ' + str(y) + '-' + str(m))
                    time.sleep(t_pause)

if __name__ == '__main__':
    print('Starting main()!')
    main()
    print('All data scraping is finished!')


# %%
