#!/usr/bin/env python3

import conversion as cv
import io_tools as io
import random
import unittest
from tempfile import NamedTemporaryFile
from subprocess import check_output


class TestConversionFunction(unittest.TestCase):
    def check_number_of_fields(self):
        self.assertEqual(len())


class TestGtf2ToGff3Conversion(unittest.TestCase):

    def setUp(self):
        self.test_input = [
            ['NODE_487', 'GeneMark.hmm', 'exon', '1487', '1693', '0', '+', '.', 'gene_id "98_g"; transcript_id "98_t";'],
            ['NODE_487', 'GeneMark.hmm', 'start_codon', '1487', '1489', '.', '+', '0', 'gene_id "98_g"; transcript_id "98_t";'],
            ['NODE_487', 'GeneMark.hmm', 'CDS', '1487', '1693', '.', '+', '0', 'gene_id "98_g"; transcript_id "98_t";'],
            ['NODE_487', 'GeneMark.hmm', 'exon', '1894', '2097', '0', '+', '.', 'gene_id "98_g"; transcript_id "98_t";'],
            ['NODE_487', 'GeneMark.hmm', 'CDS', '1894', '2097', '.', '+', '0', 'gene_id "98_g"; transcript_id "98_t";'],
            ['NODE_487', 'GeneMark.hmm', 'exon', '2223', '3429', '0', '+', '.', 'gene_id "98_g"; transcript_id "98_t";'],
            ['NODE_487', 'GeneMark.hmm', 'CDS', '2223', '3429', '.', '+', '0', 'gene_id "98_g"; transcript_id "98_t";'],
            ['NODE_487', 'GeneMark.hmm', 'exon', '3693', '4305', '0', '+', '.', 'gene_id "98_g"; transcript_id "98_t";'],
            ['NODE_487', 'GeneMark.hmm', 'CDS', '3693', '4305', '.', '+', '2', 'gene_id "98_g"; transcript_id "98_t";'],
            ['NODE_487', 'GeneMark.hmm', 'exon', '4337', '6176', '0', '+', '.', 'gene_id "98_g"; transcript_id "98_t";'],
            ['NODE_487', 'GeneMark.hmm', 'CDS', '4337', '6176', '.', '+', '1', 'gene_id "98_g"; transcript_id "98_t";'],
            ['NODE_487', 'GeneMark.hmm', 'stop_codon', '6174', '6176', '.', '+', '0', 'gene_id "98_g"; transcript_id "98_t";'],
            ['NODE_487', 'GeneMark.hmm', 'exon', '6612', '7946', '0', '-', '.', 'gene_id "99_g"; transcript_id "99_t";']]

        self.cds_count = self.calc_cds(self.test_input)
        self.records_count = len(self.test_input)

    def calc_cds(self, data):
        return sum(line[2] == 'CDS'
                   for line in data)

    def test_default_mode(self):
        with NamedTemporaryFile() as out:
            gff = cv.gtf_to_gff3(self.test_input, out.name)
            self.assertEqual(len(gff), self.records_count)

    def test_cds_only(self):
        with NamedTemporaryFile() as out:
            gff = cv.gtf_to_gff3(self.test_input, out.name, cds_only=True)
            print(gff)
            self.assertEqual(len(gff), self.cds_count)
            for line in gff:
                self.assertFalse('gene_id' in line[-1])

if __name__ == '__main__':
    unittest.main()