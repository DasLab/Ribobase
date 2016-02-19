from abc import ABCMeta, abstractmethod
import os
import options

class Wrapper(object):

    __slots__ = ['_name', '_program_path', '_options']

    def __init__(self, program_path, **cmd_options):
        self._name = "Wrapper"
        self._program_path = program_path
        if not os.path.exists(self._program_path):
            raise ValueError("program path : " + program_path + " does not exist")
        self._options = options.Options()

    def add_option(self, name, value):
        self._options.add(name, value)

    def set_option(self, name, value):
        self._options.set(name, value)

    def get_command(self, **options):
        self._options.dict_set(options)




    def get_output(self):
        raise NotImplementedError
