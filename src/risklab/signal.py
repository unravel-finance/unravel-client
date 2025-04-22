import pandas as pd


ReturnsDataFrame = pd.DataFrame
VolScaledSignal = pd.Series


def scale_to_target_volatility(
    target_volatility: float,  # percentage of the returns's standard deviation, if 0.0, no scaling is done
    rolling_window: int,
    returns: pd.Series,
    upper_limit: float,
    delay: int,
    fill_initial_period_with_mean: bool,
) -> VolScaledSignal:
    rolling_vol = (
        returns.rolling(rolling_window, min_periods=rolling_window).std()
    ).shift(delay)
    output = (target_volatility / rolling_vol).clip(lower=0.0, upper=upper_limit)
    if fill_initial_period_with_mean:
        output.iloc[:rolling_window] = output.mean()
    return output
