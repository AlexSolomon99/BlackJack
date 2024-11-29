import strategies


class StrategyFactory:

    def __init__(self):
        pass

    @classmethod
    def instantiate_strategy(cls, strat_name: str, strat_attr: dict):
        strategy_map = cls.get_strategy_map()
        if strat_name in strategy_map.keys():
            return strategy_map[strat_name](**strat_attr)
        else:
            raise NotImplementedError(f"Strategy {strat_name} is not implemented")

    @staticmethod
    def get_strategy_map():
        return {
            "dealer": strategies.DealerStrategy,
            "random": strategies.RandomStrategy
        }
