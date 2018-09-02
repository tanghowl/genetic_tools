import pandas as pd
from collections import defaultdict
from itertools import product

class Compute(object):

    def __init__(self, content):
        self.input = content
        self.df = self.read_data()

    def read_data(self):

        data = {'Rsid': [], 'gt': [], 'freq': [], 'beta': []}

        for line in self.input.strip().split('\n')[1:]:
            each = line.strip().split()
            data['Rsid'].append(each[0])
            data['gt'].append(each[1])
            data['freq'].append(each[2])
            data['beta'].append(each[3])

        df = pd.DataFrame(data, dtype=float)
        df.index = df[['Rsid', 'gt']]

        return df

    def cartesian_product(self):
        
        risd_dict = defaultdict(list)
        for each in self.df.index.tolist():
            rs = each[0]
            risd_dict[rs].append(each)
        all_gt = tuple(risd_dict.values())
        combinations = product(*all_gt)
        
        results = ''
        for comb in combinations:
            result = [i[1] for i in comb]
            result.append(round(self.df.loc[comb, 'freq'].prod(), 2))
            result.append(round(self.df.loc[comb, 'beta'].sum(), 2))
            results += '\t'.join(map(str, result)) + '\r\n'

        head = '\t'.join([i[0] for i in comb] + ['merge_freq', 'merge_beta']) + '\r\n'
        results = head + results
        
        return results