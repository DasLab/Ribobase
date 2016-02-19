import unittest
import os
from ribobase import wrapper


class WrapperUnittests(unittest.TestCase):
    def test_creation(self):
        w = wrapper.Wrapper("/usr/local/bin/RNAFold")

        try:
            w = wrapper.Wrapper("/test/test/fail")
            raise RuntimeError
        except ValueError:
            pass
        except:
            self.fail("did not throw error for improper path")

    def test_add_option(self):
        program_path = os.environ.get('RNAMAKE') + \
                       "/rnamake/lib/RNAMake/cmake/build/simulate_tectos"
        w = wrapper.Wrapper(program_path)
        w.add_cmd_option("cseq", "")
        w.get_command()







def main():
    unittest.main()

if __name__ == '__main__':
    main()
