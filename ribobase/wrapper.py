from abc import ABCMeta, abstractmethod
import os
import options

class Wrapper(object):

    __slots__ = ['__name',
                 '__program_path',
                 '__options',
                 '__cmd_options',
                 '__default_cmd_options']

    def __init__(self, program_path, **cmd_options):
        self.__name = "Wrapper"
        self.__program_path = program_path
        if not os.path.exists(self.__program_path):
            raise ValueError("program path : " + program_path + " does not exist")
        self.__cmd_options = options.Options()
        self.__default_cmd_options = {}

        self.__options = options.Options()
        self.__options.add("ignore_defaults", True)

    def add_cmd_option(self, name, value):
        self.__cmd_options.add(name, value)
        self.__default_cmd_options[name] = value

    def set_cmd_option(self, name, value):
        self.__options.set(name, value)

    def get_command(self, **options):
        self.__cmd_options.dict_set(options)

        s = self.__program_path + " "
        for k, opt in self.__cmd_options:
            print k
        return s






    def get_output(self):
        raise NotImplementedError
