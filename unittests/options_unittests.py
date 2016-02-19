import unittest
import os
from ribobase.options import *

class OptionUnittests(unittest.TestCase):
    def test_creation(self):
        opt1 = Option("test", OptionType.STRING)
        opt2 = Option(2     , OptionType.NUMBER)
        opt3 = Option(False , OptionType.BOOL)

        try:
            opt = Option(2, OptionType.STRING)
            raise RuntimeError
        except OptionException:
            pass
        except:
            self.fail("did not get expected error")

    def test_value_assignement_str(self):
        opt = Option("test", OptionType.STRING)
        opt.value = "passed!"

        try:
            opt.value = 2
            raise RuntimeError
        except OptionException:
            pass
        except:
            self.fail("did not get expected error")

        try:
            opt.value = False
            raise RuntimeError
        except OptionException:
            pass
        except:
            self.fail("did not get expected error")

    def test_value_assignemnt_num(self):
        opt = Option(2, OptionType.NUMBER)
        opt.value = 5

        try:
            opt.value = "test"
            raise RuntimeError
        except OptionException:
            pass
        except:
            self.fail("did not get expected error")

        try:
            opt.value = False
            raise RuntimeError
        except OptionException:
            pass
        except:
            self.fail("did not get expected error")

    def test_value_assignment_bool(self):
        opt = Option(False, OptionType.BOOL)
        opt.value = True

        try:
            opt.value = "test"
            raise RuntimeError
        except OptionException:
            pass
        except:
            self.fail("did not get expected error")

        try:
            opt.value = 2
            raise RuntimeError
        except OptionException:
            pass
        except:
            self.fail("did not get expected error")


class OptionsUnittests(unittest.TestCase):

    def test_creation(self):
        opts = Options()

    def test_add(self):
        opts = Options()
        opts.add("test", 5)

        if opts['test'] != 5:
            self.fail("did not set option correctly")

        opts['test'] = 2

        try:
            opts['test'] = "test2"
            raise RuntimeError
        except OptionException:
            pass
        except:
            self.fail("did not get expected error")



def main():
    unittest.main()

if __name__ == '__main__':
    main()
