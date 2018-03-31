# -*-coding: utf-8 -*-
# author:tyhj
# test_print_next_prime.py 2017.11.14 21:19
from unittest import TestCase

from study.readingSourceCode.tushare.primes import is_prime


class TestPrint_next_prime(TestCase):
    def test_print_next_prime(self):
        self.assertTrue(is_prime(5))


