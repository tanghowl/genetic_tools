import pandas as pd


class Compute(object):

    def __init__(self, content):
        self.input = content
        self.df = self.read_data()

    def read_data(self):

        data = {'Rsid': [], 'gt': [], 'freq': [], 'beta': []}

        for line in self.input.strip().split('\n'):
            each = line.strip().split()
            data['Rsid'].append(each[0])
            data['gt'].append(each[1])
            data['freq'].append(each[2])
            data['beta'].append(each[3])

        df = pd.DataFrame(data, dtype=float)
        return df

    def comput_three(self, rs):
        head = '\t'.join([rs[0], rs[1], rs[2], 'merge_freq', 'merge_beta']) + '\r\n'
        result = head
        for k1, v1 in self.df[self.df['Rsid'] == rs[0]].iterrows():
            for k2, v2 in self.df[self.df['Rsid'] == rs[1]].iterrows():
                for k3, v3 in self.df[self.df['Rsid'] == rs[2]].iterrows():
                    merge_freq = v1['freq'] * v2['freq'] * v3['freq']
                    merge_beta = v1['beta'] + v2['beta'] + v3['beta']
                    result += '\t'.join(
                        map(str, [v1['gt'], v2['gt'], v3['gt'], round(merge_freq, 2), round(merge_beta, 2)])) + '\r\n'

        return result

    def comput_four(self, rs):
        head = '\t'.join([rs[0], rs[1], rs[2], rs[3], 'merge_freq', 'merge_beta']) + '\r\n'
        result = head
        for k1, v1 in self.df[self.df['Rsid'] == rs[0]].iterrows():
            for k2, v2 in self.df[self.df['Rsid'] == rs[1]].iterrows():
                for k3, v3 in self.df[self.df['Rsid'] == rs[2]].iterrows():
                    for k4, v4 in self.df[self.df['Rsid'] == rs[3]].iterrows():
                        merge_freq = v1['freq'] * v2['freq'] * v3['freq'] * v4['freq']
                        merge_beta = v1['beta'] + v2['beta'] + v3['beta'] + v4['freq']
                        result += '\t'.join(map(str, [v1['gt'], v2['gt'], v3['gt'], v4['gt'], round(merge_freq, 2),
                                                      round(merge_beta, 2)])) + '\r\n'

        return result

    def main(self):
        rs = self.df['Rsid'].unique()
        num = len(rs)
        result = f'只能输入3个或4个位点，你输入了{num}个位点: {rs}'
        if len(rs) == 3:
            result = self.comput_three(rs)
        elif len(rs) == 4:
            result = self.comput_four(rs)
        return result
