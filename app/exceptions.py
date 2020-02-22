# define Python user-defined exceptions
class Error(Exception):
   """Base class for other exceptions"""
   pass


class NotAPythonFile(Error):
   """Raised when the input file is not a Python File"""
   pass


class ArgumentError(Error):
   """Raised when both the --folder and --file argument gets passed """
   pass
