#!/usr/bin/env python
# -*- coding utf-8 -*-

from cStringIO import StringIO
from line_profiler import LineProfiler

class AnyLineProfiler(LineProfiler):
    def __init__(self, user_func=None):
        """
        @user_func - can be supplied in keyword args  and will be used for post processing output, for example printing/logging/writing to ..
        """
        self.user_func = user_func or self.print_io
        LineProfiler.__init__(self)

    def wrap_function(self, func):
        """ Wrap a function to profile it.
        """
        def f(*args, **kwds):
            self.enable_by_count()
            self.output = StringIO()
            try:
                result = func(*args, **kwds)
            finally:
                self.disable_by_count()
                self.print_stats(stream=self.output)
                self.user_func(self.output.getvalue())
            return result
        return f

    def print_io(self, output):
        """Internal print function for viewing results of profile"""
        print output

