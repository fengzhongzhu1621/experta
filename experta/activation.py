# -*- coding: utf-8 -*-
"""
Activations represent rules that matches against a specific factlist.

"""
from functools import total_ordering


@total_ordering
class Activation:
    """
    Activation object 满足事实或目标的规则，需要放到Agenda中
    """
    def __init__(self, rule, facts, context=None):
        # 定义的规则
        self.rule = rule
        # 规则匹配的Facts
        self.facts = set(facts)
        self.key = None
        if context is None:
            self.context = dict()
        else:
            self.context = context

    def __repr__(self):  # pragma: no cover
        return "Activation(rule={}, facts={}, context={})".format(
            self.rule, self.facts, self.context)

    def __eq__(self, other):
        try:
            return (self.context == other.context
                    and self.facts == other.facts
                    and self.rule == other.rule
                    and self.key == other.key)
        except AttributeError:
            return False

    def __lt__(self, other):
        return self.key < other.key

    def __hash__(self):
        return hash((self.rule,
                     frozenset(self.facts),
                     frozenset(self.context.items())))
