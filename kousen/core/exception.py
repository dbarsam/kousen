# -*- coding: utf-8 -*-
"""
This module provides all utility functions and class defintions for extending Python native exception functionality.
"""
import os
import sys
import traceback

class ExceptionMessage(object):
    """
    The Exception Message class implements a more verbose string representation of a Python system exception.
    """
    def __init__(self, exception):
        """
        Constructor.

        @param exception The system exception.
        """
        super(ExceptionMessage, self).__init__()

        self._message = self._extract(exception)

    def __repr__(self):
        """
        Generates the "official" string representation of the Exception Message

        @returns A string representation of the Exception Message
        """
        return "{0}:\n{1}".format(self.__class__.__name__, self._message)

    def __str__(self):
        """
        Generates the "informal" string representation of the Vector3D.

        @returns A string representation of the Exception Message
        """
        return self._message

    def _extract(self, exception):
        """
        Extracts the relavant information from a system exception

        @param exception The system exception.
        @returns The respective message.
        """
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        tbInfo = traceback.extract_tb(exc_tb)
        filename, line, func, text = tbInfo[-1]
        message = [
            "****************************",
            " EXCEPTION: {0}".format(exception),
            "    File: {0}, Line: {1}, Exception: {2})".format(fname, str(exc_tb.tb_lineno), str(exc_type)),
            "----------------------------",
            " STATEMENT:",
            "    File: {0}".format(filename),
            "    Line: {0}".format(str(line)),
            "    Func: {0}".format(func),
            "    Text: {0}".format(text),
            " TRACEBACK:",
            " {0}".format(" ".join(traceback.format_exception(exc_type, exc_obj, exc_tb))),
            "****************************"]
        return "\n".join(message)

if __name__ == "__main__":
    try:
        raise ArithmeticError()
    except Exception as e:
        print(ExceptionMessage(e))
