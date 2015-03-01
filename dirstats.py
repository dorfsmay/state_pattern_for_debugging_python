#!/usr/bin/env python3

import os
import inspect
import argparse
import operator
import statistics

# WARNING
# This is only for the purpose of showing my state pattern, there is
# no consideration for memory constraint.
#

'''
The idea, which I think is effectively a state pattern, is to prevent:

  * Using global variables that could leak into the local functions.
    ==> The variables are local to the __init__ method.

  * The usual main function which prevent access to the variable from the repl.
    ==> All the variables are accessible from the repl via the object, and
        can be manipulated and used by the functions.

  * Make the functions aware of the class/object, which you need to when using
    a class as a structure.
    ==> You pass the variables directly with no reference to either a class
        nor an object.


Ref:
  - http://en.wikipedia.org/wiki/State_pattern
'''

def calculate_average(all_values):
    return statistics.mean(all_values)

def calculate_median(all_values):
    return statistics.median(all_values)

def find_largest(all):
    return max(all, key=all.get)
    
def find_smallest(all):
    return min(all, key=all.get)

def get_all_files(directory):
    all_files = dict()
    for root, dirs, files in os.walk(directory):
        for fn in files:
            abs_path = os.path.join(root, fn)
            all_files[abs_path] = os.path.getsize(abs_path)
    return all_files


class DirStat(object):
    def __init__(self, directory):
        self.all_files = get_all_files(directory)
        self.average = calculate_average(self.all_files.values())
        self.median = calculate_median(self.all_files.values())
        self.largest = find_largest(self.all_files)
        self.smallest = find_smallest(self.all_files)

    def print(self):
        print("mean: {:.2f}".format(self.average))
        print("median: {:.2f}".format(self.median))
        print("smallest file: {}".format(self.smallest))
        print("largest file: {}".format(self.largest))

    def __repr__(self):
        return self.__dict__.__repr__()




if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Show some basic stats about a directory.",
    )
    parser.add_argument("directory", help="Directory for which the stats will be calculated.")
    args = parser.parse_args()


stats = DirStat(**vars(args))
stats.print()

