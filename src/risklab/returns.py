from functools import partial
from typing import TypeVar

import numpy as np
import pandas as pd

T = TypeVar("T", pd.Series, pd.DataFrame)


def compsum(returns):
    """Calculates rolling compounded returns"""
    return returns.add(1).cumprod() - 1


def __fill_first_value_with_zero(series: pd.Series) -> pd.Series:
    series.iloc[0] = 0.0
    return series


def __apply_clip(data: T, clip: float | None) -> T:
    if clip is not None:
        return data.clip(lower=-clip, upper=clip)
    return data


def to_log_returns(data: T, clip: float | None) -> T:
    return __apply_clip(np.log1p(to_returns(data, clip=None)), clip=clip)


def to_returns(data: T, clip: float | None) -> T:
    if isinstance(data, pd.DataFrame):
        return data.apply(partial(to_returns, clip=clip))
    if data.min() < 0:
        return __apply_clip(
            __fill_first_value_with_zero(data.diff() / data.shift(1).abs()), clip=clip
        )
    return __apply_clip(
        __fill_first_value_with_zero(data / data.shift(1) - 1), clip=clip
    )


TPandas = TypeVar("TPandas", pd.DataFrame, pd.Series)


def to_prices(returns: pd.Series, base=1.0) -> pd.Series:
    """Arithcmetic returns to price series"""
    returns = returns.copy().fillna(0).replace([np.inf, -np.inf], float("NaN"))
    return base + base * compsum(returns)
