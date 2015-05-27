#!/usr/bin/env python3

import io_tools as bf
#import os
import random
from subprocess import check_output
import conversion as cv


def test_all():
    test_read_tsv("test/test_liftover.bed")
    test_read_tsv("test/test_augustus_gff3.gff")
    test_gff2bed("test/test_augustus_gff3.gff", "../test_out_bed")
    test_bed2gff3("test/test_liftover.bed", "../test_out_gff3")
    test_gtf2gff3("test/test_gm_es.gtf", "../test_out_gff3")

#Simple tests


def test_read_tsv(test_file):
    temp = bf.read_tsv(test_file)
    wc = int(check_output(["wc", "-l", test_file]).split()[0])
    print('testing file', test_file)
    print('line count in file', wc)
    print('object length', len(temp))
    print('checking line count:', len(temp) == wc + 1)
    print('checking field count:', len(temp[0]) == 9)  # именованный параметр
    print('printing a random line for visual check' + '\n' +
          '\t'.join(temp[random.randint(1, len(temp))]) + '\n')


def test_write_tsv():
    pass


def test_conversion_function(temp, number_of_fields):
    print('checking field count:', len(temp[0]) == number_of_fields)
    print('printing a random line of bed output for visual check')
    print(str(temp[random.randint(1, len(temp))]) + '\n')


def test_gff2bed(test_file, test_out_file):
    temp = cv.gff_to_bed(test_file, test_out_file)
    print('testing gff2bed')
    test_conversion_function(temp, 3)  # именованный параметр


def test_bed2gff3(test_file, test_out_file):
    temp = cv.bed_to_gff3(test_file, test_out_file)
    print('testing bed2gff3')
    test_conversion_function(temp, 9)
    pass


def test_gtf2gff3(test_file, test_out_file):
    temp = cv.gtf_to_gff3(test_file, test_out_file)
    print('testing gtf2gff3')
    test_conversion_function(temp, 9)


if __name__ == '__main__':
    test_all()


#Add tests for lexiconSV and compare_vcf!!! => test => commit