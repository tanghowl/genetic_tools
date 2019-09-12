from db.mongo import MongoDB
from pprint import pprint
from itertools import chain


class QueryNgsQc(object):

    def __init__(self, barcodes):
        self.barcodes = barcodes
        self.qc_info = self.get_ngs_info()

    @property
    def barcode_lst(self):
        bar_lst = self.barcodes.strip().split('\r\n')
        return bar_lst

    def get_ngs_info(self):
        with MongoDB() as mdb:
            return list(mdb.find_barcode_info(self.barcode_lst))

    def get_reads_qc_info(self):
        reads_qc_info = list()
        info_head = self._get_reads_qc_head()
        heads = ['ProjectName', 'Bracode', 'Type'] + info_head

        for each in self.qc_info:
            before_filter = self._get_each_qc_info('before_filtering', each, info_head)
            after_filter = self._get_each_qc_info('after_filtering', each, info_head)
            reads_qc_info.append(before_filter)
            reads_qc_info.append(after_filter)
        return heads, reads_qc_info

    @staticmethod
    def _get_each_qc_info(type_info, infos, info_head):
        barcode = infos.get('Barcode')
        project_name = infos.get('ProjectName')
        temp = [project_name, barcode, type_info]
        for head in info_head:
            temp.append(round(infos.get('ReadsQC').get('TotalReads').get(type_info).get(head), 4))
        return temp

    def _get_reads_qc_head(self):
        all_head = set(list(
            chain(*[list(i.get('ReadsQC').get('TotalReads').get('before_filtering').keys()) for i in self.qc_info])))
        return sorted(all_head)

    def get_match_interval_info(self):
        info_head = ['PCT_TARGET_BASES_1X',
                     'PCT_TARGET_BASES_2X',
                     'PCT_TARGET_BASES_10X',
                     'PCT_TARGET_BASES_20X',
                     'PCT_TARGET_BASES_30X',
                     'PCT_TARGET_BASES_40X',
                     'PCT_TARGET_BASES_50X',
                     'PCT_TARGET_BASES_100X',
                     'FOLD_80_BASE_PENALTY']
        match_interval_info = list()
        heads = ['ProjectName', 'Bracode'] + info_head

        for each in self.qc_info:
            each_info = []
            project_name = each.get('ProjectName')
            barcode = each.get('Barcode')
            each_info.append(project_name)
            each_info.append(barcode)
            for head in info_head:
                info = each.get('MatchInterval').get(head)
                value = round(float(info), 4)
                each_info.append(value)
            match_interval_info.append(each_info)
        return heads, match_interval_info

    def get_unmap_info(self):
        unmap_info = list()
        info_head = self._get_unmap_head()
        heads = ['ProjectName', 'Bracode'] + info_head

        for each in self.qc_info:
            each_info = []
            project_name = each.get('ProjectName')
            barcode = each.get('Barcode')
            each_info.append(project_name)
            each_info.append(barcode)

            tmp_info = {}
            for tmp_e in each.get('UnMapped'):
                species = tmp_e.get('species')
                mapped_rate = tmp_e.get('mapped_rate')
                tmp_info[species] = mapped_rate

            for head in info_head:
                info = tmp_info.get(head)
                each_info.append(info)

            unmap_info.append(each_info)
        return heads, unmap_info

    def _get_unmap_head(self):
        all_head = set([i.get('species') for t in self.qc_info for i in t.get('UnMapped')])
        return sorted(all_head)
