import unittest
import os
from ribobase.options import *


class OptionsUnittests(unittest.TestCase):
    def test_creation(self):
        opt = Option("test", OptionType.STRING)



def main():
    unittest.main()

if __name__ == '__main__':
    main()
