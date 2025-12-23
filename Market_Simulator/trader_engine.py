from Algorithmic_Trading.Market_Simulator.level2data import Level2Data
from Algorithmic_Trading.Market_Simulator.trader import LiquidityAbsorber, MarketMaker, AgressiveTraders, \
    LiquidityAbsorber2, Bears, Company,Whales
from trader import RandomTrader,Level1Trader,Level2Trader
import data

class TraderEngine:
    def __init__(self):
        pass

    @classmethod
    def initialize_random_traders(cls,traders : list,level2_data : Level2Data):
        for _ in range(data.RANDOM_TRADERS):
            trader = RandomTrader(level2_data,data.TRADER_ID)
            data.TRADER_ID += 1
            traders.append(trader)

    @classmethod
    def initialize_level1_traders(cls,traders : list,level_2_data : Level2Data):
        for _ in range(data.LEVEL1_TRADERS):
            trader = Level1Trader(level_2_data,data.TRADER_ID)
            data.TRADER_ID += 1
            traders.append(trader)

    @classmethod
    def initialize_level2_traders(cls,traders : list,indicators,level_2_data : Level2Data):
        for _ in range(data.LEVEL2_TRADERS):
            trader = Level2Trader(level_2_data,indicators,data.TRADER_ID)
            data.TRADER_ID += 1
            traders.append(trader)

    @classmethod
    def initialize_level3_traders(cls,traders : list,indicators,level_2_data):
        for _ in range(data.LIQUIDITY_TRADERS):
            trader = LiquidityAbsorber(indicators,level_2_data,data.TRADER_ID)
            traders.append(trader)
            data.TRADER_ID += 1

            trader = LiquidityAbsorber2(indicators,level_2_data,data.TRADER_ID)
            traders.append(trader)
            data.TRADER_ID += 1

        for _ in range(data.MARKET_MAKER):
            trader = MarketMaker(indicators,level_2_data,data.TRADER_ID)
            traders.append(trader)
            data.TRADER_ID += 1

        # for _ in range(100):
        for _ in range(data.BEARS_TRADERS):
            trader = Bears(indicators,level_2_data,data.TRADER_ID)
            traders.append(trader)
            data.TRADER_ID += 1

        # trader = MarketMaker(indicators,level_2_data,data.TRADER_ID)
        # traders.append(trader)
        # data.TRADER_ID += 1

        for _ in range(data.AGRESSIVE_TRADER):
            trader = AgressiveTraders(indicators,level_2_data,data.TRADER_ID)
            traders.append(trader)
            data.TRADER_ID += 1

        for _ in range(data.WHALES):
            trader = Whales(level_2_data,data.TRADER_ID)
            traders.append(trader)
            data.TRADER_ID += 1



        company = Company(8)
        traders.append(company)
        data.TRADER_ID += 1

        # trader = BigHedgeFund(indicators,level_2_data,data.TRADER_ID)
        # traders.append(trader)
        # data.TRADER_ID += 1
        #
        # trader = BigHedgeFund(indicators,level_2_data,data.TRADER_ID)
        # traders.append(trader)
        # pass
        # data.TRADER_ID += 1

