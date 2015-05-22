
from __future__ import print_function

import sys
import collections
import operator
import itertools

def translate(square, direction, scale):
    return tuple(map(operator.add, square, map(lambda x: x * scale, direction)))

class PeterPan(object):
    """
    A program to solve: http://domino.research.ibm.com/Comm/wwwr_ponder.nsf/Challenges/April2015.html
    """
    def __init__(self, numdimensions, size):
        self.numdimensions = numdimensions
        self.size = size

    def do_all(self):
        self.initialize()
        self.populate_mapping()
        self.add_wendies()
        self.print_output()

    def initialize(self):
        self.directions = set(itertools.product((-1, 0, 1), repeat=self.numdimensions))
        self.squares = set(itertools.product(xrange(0, self.size), repeat=self.numdimensions))
        self.hooks = set(itertools.product(xrange(-1, self.size+1), repeat=self.numdimensions)) - self.squares
        self.wendies = set()

    def populate_mapping(self):
        self.hooks2squares = collections.defaultdict(set)
        self.squares2hooks = collections.defaultdict(set)
        for h in self.hooks:
            for d in self.directions:
                for i in itertools.count(start=1):
                    square = translate(h, d, i)
                    print('square', square, file=sys.stderr)
                    if (square not in self.squares):
                        break
                    self.hooks2squares[(h, d)].add(square)
                    self.squares2hooks[square].add((h, d))

    def remove_hook(self, hook):
        for square in self.hooks2squares[hook]:
            self.squares2hooks[square].remove(hook)
        del self.hooks2squares[hook]

    def remove_square(self, square):
        for hook in self.squares2hooks[square]:
            for sq in self.hooks2squares[hook]:
                if (sq == square):
                    continue
                self.squares2hooks[sq].remove(hook)
            del self.hooks2squares[hook]
#             self.remove_hook(hook)
        del self.squares2hooks[square]

    def best_square(self, criterion=lambda x: True):
        """
        Get the square (among those satisfy criterion) that can block the
        most number of hooks.
        """
        (l, square) = max((len(v), k) for (k, v) in self.squares2hooks.iteritems() if criterion(k))
        if (l == 0):
            return None
        return square

    def add_wendies(self):
        while True:
            (l, hook) = min((len(v), k) for (k, v) in self.hooks2squares.iteritems())
            if (l > 1):
                break
            square = self.best_square(lambda s: (s in self.hooks2squares[hook]))
            if not square:
                break
            # (square,) = self.hooks2squares[hook]
            print('Added a wendy', square, file=sys.stderr)
            self.wendies.add(square)
            self.remove_square(square)
        print('Entering square loop', file=sys.stderr)
        while True:
            square = self.best_square()
            if not square:
                break
            print('Added a wendy', square, file=sys.stderr)
            self.wendies.add(square)
            self.remove_square(square)

    def print_output(self):
        num_wendies = len(self.wendies)
        print('Number of Wendies: {}'.format(num_wendies), file=sys.stderr)
        print('Number of Peter pans: {}'.format(len(self.squares) - num_wendies), file=sys.stderr)
        print(''.join(('W' if (square in self.wendies) else 'P') for square in sorted(self.squares)))

p = PeterPan(numdimensions=3, size=7)
p.do_all()
