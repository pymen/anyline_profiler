anyline_profiler
================

I often need to find a bottle-neck in some code, and most easiest way to use profiling. Of course you can use internal Cprofile, but it does not allow to quickly understand which function or method takes 90% of processing time.

But there is a nice package - line_profiler for python 2.7 https://pypi.python.org/pypi/line_profiler
To use it you should add decorator @profile to your code and run your python module with python -m and will return you results after exiting from script, which is not usefull for example if you need to profile your webserver.

I made it a bit more simplier - all you need to import AnyLineProfiler, define your output function, that will be used as postprocessing output (by default - result will be printed) and use it as any other decorator. Also AnyLineProfiler collects all results to StringIO and it can be used in Threaded scripts

==============================================================
    from any_line_profiler import AnyLineProfiler
    profile =  AnyLineProfiler( ) #or profile =  AnyLineProfiler(your_function_to_post_process )

    @profile
    def long_function()
       do_1()
       do_2()
       do_3()

For example we have 2 functions - test1 and test2 and we want to print profile results for first and to log (using logging module) for second. So we need to define two different profilers based on AnyLineProfiler and define logging function

==============================================================
    import time
    from any_line_profiler import AnyLineProfiler

    def example_logging_profile(a):
        """example of logging function"""
        import logging
        log = logging.getLogger()
        formatter = logging.Formatter(u'%(asctime)s %(name)-8s %(levelname)-8s %(filename)s [line:%(lineno)d]: %(message)s\n-------\n')
        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        log.addHandler(sh)
        log.error(a)

    profile = AnyLineProfiler() #base profiler, that will print to output
    profileLog = AnyLineProfiler(user_func=example_logging_profile) #profiler that will log

    @profile
    def test1():
        time.sleep(0.1)
        time.sleep(0.2)

    @profileLog
    def test2():
        time.sleep(0.1)
        time.sleep(0.2)


After executing this script you will see following results: first from logging, second basic print

    ==============================================================
    2013-08-30 21:16:15,878 root     ERROR    test_profile.py [line:42]: Timer unit: 3.19979e-07 s

    Function: test1 at line 47
    Total time: 0.299973 s

    Line #      Hits         Time  Per Hit   % Time  Line Contents
        47                                           @profileLog
        48                                           def test1():
        49         1       312418 312418.0     33.3      time.sleep(0.1)
        50         1       625060 625060.0     66.7      time.sleep(0.2)


    Timer unit: 3.19979e-07 s
    Function: test2 at line 52
    Total time: 0.300138 s

    Line #      Hits         Time  Per Hit   % Time  Line Contents
        52                                           @profile
        53                                           def test2():
        54         1       312256 312256.0     33.3      time.sleep(0.1)
        55         1       625736 625736.0     66.7      time.sleep(0.2)

