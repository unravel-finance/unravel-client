from collections.abc import Callable
from enum import Enum

import pandas as pd

from .window import calculate_window_size

ReturnsDataFrame = pd.DataFrame
VolScaledSignal = pd.Series


class TargetCalculation(Enum):
    relative = "relative"
    absolute = "absolute"


def scale_to_target_volatility(
    target_volatility: float,  # percentage of the returns's standard deviation, if 0.0, no scaling is done
    rolling_window: int,
    returns: pd.Series,
    upper_limit: float,
    method: TargetCalculation,
    delay: int,
    fill_initial_period_with_mean: bool,
) -> VolScaledSignal:
    if target_volatility == 0.0:
        return pd.Series(1.0, index=returns.index)
    if method == TargetCalculation.relative:
        target_volatility = returns.expanding().std().mul(target_volatility)

    rolling_vol = (
        returns.rolling(rolling_window, min_periods=rolling_window).std()
    ).shift(delay)
    output = (target_volatility / rolling_vol).clip(lower=0.0, upper=upper_limit)
    if fill_initial_period_with_mean:
        output.iloc[:rolling_window] = output.mean()
    return output


def rolling_drawdown(window: int | None) -> Callable:
    def _rolling_drawdown(series: pd.Series) -> pd.Series:
        rolling_or_expanding = (
            series.expanding()
            if window is None
            else series.rolling(
                calculate_window_size(window, len(series)), min_periods=0
            )
        )
        return series / rolling_or_expanding.max()

    return _rolling_drawdown
