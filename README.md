# Quadratic Equations Solver

This script uses git hook pre-commit for autorun unit tests

Copy file pre-commit into dir .../our_project/.git/hooks

check script

```#!bash
$ cp pre-commit .../our_project/.git/hooks
$ chmod +x .../our_project/.git/hooks/pre-commit


```

after command git commit ... If our project consist of tests.py, they will run, befor commit.
If tests exec with error, you will see errors and commit will not exec.


# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
