import argparse
import time
# import numpy as np
from bisect import bisect

import pandas as pd

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
                help="path to input file")
ap.add_argument("-o", "--output", required=True,
                help="path to save results")
ap.add_argument("-m", "--mmetric", type=int, default=100,
                help="number of all possible incidents values")  # !!! not actually needed, but add it according to TEST
ap.add_argument("-t", "--dt", type=float, required=True,
                help="value of time difference to incident counting")

args = vars(ap.parse_args())


class incidentCounter():

    def __init__(self, args):

        self.args = args
        self.df = pd.read_csv(args['input'])
        self.incident_dict = {}
        self.res = []  # results incident counting

    def preprocess_data(self):

        # cash time values according to incident values
        # {incidet_value : [t1, t4, t77, ...], ...}

        self.df.sort_values(by='time', inplace=True, ascending=False)
        #self.df.reset_index(inplace=True)

        for f1, f2, incid_time in zip(self.df['feature1'], self.df['feature2'], self.df['time']):
            incident = str(f1) + str(f2)

            # insert time values in sorted order

            if incident not in self.incident_dict.keys():
                self.incident_dict[incident] = [incid_time]

            else:
                if self.incident_dict[incident][-1] >= incid_time:

                    self.incident_dict[incident].insert(0, incid_time)
                else:
                    self.incident_dict[incident].append(incid_time)

    def counting(self):

        # find length of time list [time, ..., time-dt] with binary search

        for f1, f2, incid_time in zip(self.df['feature1'], self.df['feature2'], self.df['time']):
            incident = str(f1) + str(f2)
            t2 = bisect(self.incident_dict[incident], incid_time - self.args['dt'])  # return index of last incident
            t1 = bisect(self.incident_dict[incident], incid_time)  # return index of first incident
            self.res.append((t1 - 1) - t2)
        self.df['res'] = self.res

        # save to csv
        self.df[['id', 'res']].sort_values(by='id').to_csv(args['output'], index=None)

    def main(self):

        self.preprocess_data()
        self.counting()


if __name__ == "__main__":
    cur_time = time.time()

    inc_count = incidentCounter(args)
    inc_count.main()

    cur_time = time.time() - cur_time
    print('time to process file contain {} rows with M = {} is {} sec'.format(inc_count.df.shape[0],
                                                                              args['mmetric'], cur_time))
