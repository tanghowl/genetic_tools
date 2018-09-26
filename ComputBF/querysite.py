#! /usr/bin/env python3.6

import os
import pandas as pd


class QureyExist(object):

    def __init__(self, chrom, pos):
        wd = os.getcwd()
        self.v1_path = os.path.join(wd, 'configfile/v1_comparison_table')
        self.v2_path = os.path.join(wd, 'configfile/v2_comparison_table')
        self.v2_1_path = os.path.join(wd, 'configfile/v2.1_comparison_table')
        self.chrom = chrom.upper()
        self.pos = pos
        self.site = chrom.upper() + '_' + pos

    def qurey(self, path, version):
        df = pd.read_table(path, header=None, names=['chr', 'pos', 'ID', 'ref', 'alt'])
        df['chr_pos'] = df['chr'].astype(str) + '_' + df['pos'].astype(str)
        match_df = df[df['chr_pos'].isin([self.site])]
        del match_df['chr_pos']
        if match_df.shape[0] == 0:
            match_df.loc[0] = 'NA'
            match_df.loc[0, 'chr'] = self.chrom
            match_df.loc[0, 'pos'] = self.pos
        match_df['version'] = version
        return match_df

    def merge(self):
        v1_df = self.qurey(self.v1_path, 'v1')
        v2_df = self.qurey(self.v2_path, 'v2')
        v2_1_df = self.qurey(self.v2_1_path, 'v2.1')
        all_df = pd.concat([v1_df, v2_df, v2_1_df], axis=0)
        return all_df


if __name__ == '__main__':
    q = QureyExist('1', '67831294')
    print(q.merge())
