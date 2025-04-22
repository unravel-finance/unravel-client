from risklab.backtest import BacktestResult, backtest_signal
import pandas as pd
import numpy as np


def test_backtest_signal():
    signal = pd.Series(np.random.randn(100))
    underlying = pd.Series(np.random.randn(100))
    transaction_cost = 0.001
    lag = 1
    result = backtest_signal(signal, underlying, transaction_cost, lag)
    assert isinstance(result, BacktestResult)
