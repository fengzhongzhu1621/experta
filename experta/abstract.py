# -*- coding: utf-8 -*-
"""
推理引擎包括三部分：
 - 模式匹配器（Pattern Matcher）
 - 议程（Agenda）
 - 执行引擎（Execution Engine）。

推理引擎通过决定哪些规则满足事实或目标，并授予规则优先级，满足事实或目标的规则被加入议程。
模式匹配器决定选择执行哪个规则，何时执行规则；
议程管理模式匹配器挑选出来的规则的执行次序；
执行引擎负责执行规则和其他动作。
"""

import abc

from experta import watchers


class Matcher(metaclass=abc.ABCMeta):
    """Pattern模式匹配器 ."""
    def __init__(self, engine):
        self.engine = engine

    @abc.abstractmethod
    def changes(self, adding=None, deleting=None):  # pragma: no cover
        """
        Main interface with the matcher.

        Called by the knowledge engine when changes are made in the
        working memory and return a set of activations.

        """
        pass

    @abc.abstractmethod
    def reset(self):  # pragma: no cover
        """Reset the matcher memory."""
        pass


class Strategy(metaclass=abc.ABCMeta):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resolved = dict()

    @abc.abstractmethod
    def _update_agenda(self, agenda, added, removed):  # pragma: no cover
        pass

    def update_agenda(self, agenda, added, removed):
        # 议程（Agenda）管理PatternMatcher挑选出来的规则的执行次序
        # 执行所有规则的RHS
        if watchers.worth('ACTIVATIONS', 'INFO'):  # pragma: no cover
            # 打印需要删除的已经激活的规则
            for act in removed:
                watchers.ACTIVATIONS.info(
                    " <== %r: %s %s",
                    getattr(act.rule, '__name__', None),
                    ", ".join(str(f) for f in act.facts),
                    "[EXECUTED]" if act not in agenda.activations else "")
            # 打印需要添加到agenda中的规则
            for act in added:
                watchers.ACTIVATIONS.info(
                    " ==> %r: %s",
                    getattr(act.rule, '__name__', None),
                    ", ".join(str(f) for f in act.facts))

        self._update_agenda(agenda, added, removed)
