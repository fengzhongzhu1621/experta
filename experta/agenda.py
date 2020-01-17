# -*- coding: utf-8 -*-


class Agenda:
    """
    议程管理模式匹配器挑选出来的规则的执行次序

    Collection of activations that handles its execution state.

    .. note::
       Extracted from clips documentation: ``The agenda is a collection
       of activations which are those rules which match pattern entities``

    """
    def __init__(self):
        # Ordered list of activations, rightmost activation is the next to run.
        self.activations = list()

    def __repr__(self):  # pragma: no cover
        return "\n".join(
            "{idx}: {rule} {facts}".format(idx=idx,
                                           rule=getattr(act.rule,
                                                        '__name__',
                                                        '[anonymous]'),
                                           facts=act.facts)
            for idx, act in enumerate(self.activations))

    def get_next(self):
        """Returns the next activation, removes it from activations list."""

        try:
            return self.activations.pop()
        except IndexError:
            return None
