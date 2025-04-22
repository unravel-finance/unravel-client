import pandas as pd
import numpy as np

from risklab import scale_to_target_volatility


def test_volatility_targeting_noop():
    returns = pd.Series(np.random.randn(100))
    target_volatility = 0.2
    window = 20
    result = scale_to_target_volatility(
        target_volatility=target_volatility,
        rolling_window=window,
        returns=returns,
        upper_limit=1.0,
        lag=0,
        fill_initial_period_with_mean=False,
        annualization_period=252,
    )
    assert result.shape == returns.shape
