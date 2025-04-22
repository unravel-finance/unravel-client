import pandas as pd
import numpy as np

ReturnsDataFrame = pd.DataFrame
VolScaledSignal = pd.Series


def scale_to_target_volatility(
    target_volatility: float,  # percentage of the returns's standard deviation, if 0.0, no scaling is done
    rolling_window: int,
    returns: pd.Series,
    upper_limit: float,
    lag: int,
    fill_initial_period_with_mean: bool,
    annualization_period: int,
) -> VolScaledSignal:
    """
    Scale a signal to a target volatility.
    Parameters:
        target_volatility: float
            The annualized target volatility.
        rolling_window: int
            The rolling window to use.
        returns: pd.Series
            The underlying returns.
        upper_limit: float
            The maximum leverage to use during low-volatility periods.
        lag: int
            The lag to apply to the signal. When `0` is used, the volatility from the current period is used, which may or may not be realistic.
        fill_initial_period_with_mean: bool
            Whether to fill the initial period with the mean. This uses data from future periods, but it's not optimized to any objective.
        annualization_period: int
            The annualization period to use.
    Returns:
        VolScaledSignal
    """
    rolling_vol = (
        returns.rolling(rolling_window, min_periods=rolling_window).std()
        * np.sqrt(annualization_period)
    ).shift(lag)

    output = (target_volatility / rolling_vol).clip(lower=0.0, upper=upper_limit)

    if fill_initial_period_with_mean:
        output.iloc[:rolling_window] = output.mean()

    return output
