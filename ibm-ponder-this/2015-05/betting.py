
from __future__ import print_function
import itertools
import collections
import sys

class BettingGame(object):
    def __init__(self, max_value=256, num_players=3):
        self.max_value = max_value
        self.num_players = num_players
        self.STOP_STATE = tuple(0 for i in xrange(self.num_players))

    def do_all(self):
        print('Creating states', file=sys.stderr)
        states = set(itertools.imap(self.makestate, itertools.product(xrange(1, self.max_value + 1), repeat=self.num_players)))
        print('Done creating states', file=sys.stderr)
        reverse_edges = collections.defaultdict(set)
        for state in states:
            for target in self.transitions(state):
                reverse_edges[target].add(state)
        print('Done adding all transitions', file=sys.stderr)
        self.breadth_first(reverse_edges, self.STOP_STATE)

    def makestate(self, s):
        return tuple(sorted(s))

    def transitions(self, state):
        """
        Possible transitions from a state.
        """
        if len(set(state)) < len(state):
            yield self.STOP_STATE
            return
        for hidx in xrange(self.num_players):
            for lidx in xrange(hidx):
                (lower, higher) = (state[lidx], state[hidx])
                yield self.makestate(((2*lower) if (i == lidx) else ((higher - lower) if (i == hidx) else s)) for (i, s) in enumerate(state))

    def breadth_first(self, edges, start):
        # worklist contains (element, distance_from_start)
        worklist = collections.deque()
        worklist.appendleft((start, 0))
        # already_seen contains elements
        already_seen = set([ start ])
        while worklist:
            (element, distance) = (last_seen, _) = worklist.pop()
#             print('Element, Distance, ', element, distance, file=sys.stderr)
            for neighbor in edges[element]:
                if (neighbor in already_seen):
                    continue
                already_seen.add(neighbor)
                worklist.appendleft((neighbor, distance+1))
        print('Last seen: {}'.format(last_seen))
        print('Distance: {}'.format(distance))

BettingGame(max_value=256).do_all()
