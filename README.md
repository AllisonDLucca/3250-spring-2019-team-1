# JVPM

This repo is a JVM written in Python. This will execute .class files.  
 To run the program, do
```
$ python __main__.py <path to class file>
```
We have a few class files provided as examples:
- Foo.class  
    - Prints out an integer
- AddTwo.class  
    - Adds two numbers and prints the result and HelloWorld


Here is our current coverage
```
$ coverage report
Name                          Stmts   Miss  Cover
-------------------------------------------------
jvpm\ClassFile.py               134      2    99%
jvpm\OpCodes.py                 419     24    94%
jvpm\__init__.py                  0      0   100%
jvpm\test\__init__.py             0      0   100%
jvpm\test\test_ClassFile.py      64      1    98%
jvpm\test\test_OpCodes.py       587      0   100%
-------------------------------------------------
TOTAL                          1204     27    98%                            13      1    92%
```
We used other analysis tools. Here is a link to what we are using:

[SonarCloud](https://sonarcloud.io/dashboard?id=AllisonDLucca_3250-spring-2019-team-1)

[CodeCov](https://codecov.io/gh/AllisonDLucca/3250-spring-2019-team-1)

[Travis-CI](https://travis-ci.com/AllisonDLucca/3250-spring-2019-team-1)