# -*- coding: utf-8 -*-

from functools import lru_cache
import bisect

from experta.abstract import Strategy


class DepthStrategy(Strategy):
    """将activation更新到agenda中 ."""
    @lru_cache()
    def get_key(self, activation):
        # 获得规则的优先级
        salience = activation.rule.salience
        # 将匹配的facts按ID逆序
        facts = sorted((f['__factid__'] for f in activation.facts),
                       reverse=True)
        return salience, facts

    def _update_agenda(self, agenda, added, removed):
        for act in removed:
            # 设置activation的key
            act.key = self.get_key(act)
            # 从agenda.activations有序数组中删除act
            idx = bisect.bisect_left(agenda.activations, act)
            for o in (0, 1, -1):
                try:
                    if agenda.activations[idx+o] == act:
                        del agenda.activations[idx+o]
                    else:
                        continue
                except IndexError:
                    pass
                else:
                    break

        for act in added:
            # 设置activation的key
            act.key = self.get_key(act)
            # 有序插入：排序方式是根据key
            bisect.insort(agenda.activations, act)
