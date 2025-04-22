from functools import partial
from math import isnan, sqrt
from typing import Literal

import numpy as np
import pandas as pd

from .returns import to_prices


def sharpe(returns: pd.Series, annualization_period: int) -> float:
    divisor = returns.std(ddof=1)
    res = returns.mean() / divisor

    if isnan(res):
        return -10.0

    return res * sqrt(annualization_period)


def beta(returns: pd.Series, underlying: pd.Series) -> float:
    matrix = np.cov(returns, underlying)
    return matrix[0, 1] / matrix[1, 1]


def alpha(
    returns: pd.Series, underlying: pd.Series, annualization_period: int | None = None
) -> float:
    return (returns.mean() - abs(beta(returns, underlying)) * underlying.mean()) * (
        annualization_period or 1
    )


def geometric_alpha(
    returns: pd.Series, underlying: pd.Series, annualization_period: int | None = None
) -> float:
    return (
        np.log1p(returns) - abs(beta(returns, underlying)) * np.log1p(underlying).mean()
    ) * (annualization_period or 1)


def sortino(returns, annualization_period: int) -> float:
    downside = np.sqrt((returns[returns < 0] ** 2).sum() / len(returns))
    res = returns.mean() / downside
    return res * sqrt(annualization_period)


def get_avg_timestamps_per_day(index: pd.DatetimeIndex) -> float:
    return len(index) / len(np.unique(index.date))


def get_frequency_of_change(df: pd.DataFrame) -> pd.Series:
    return get_number_of_observations(df) / df.notna().sum()


def information_ratio(returns, benchmark):
    """
    Calculates the information ratio
    (basically the risk return ratio of the net profits)
    """
    diff_rets = returns - benchmark

    return diff_rets.mean() / diff_rets.std()


def is_outlier(points: pd.DataFrame, thresh: int) -> pd.Series:
    """
    Returns a boolean array with True if points are outliers and False
    otherwise.

    Parameters:
    -----------
        points : An numobservations by numdimensions array of observations
        thresh : The modified z-score to use as a threshold. Observations with
            a modified z-score (based on the median absolute deviation) greater
            than this value will be classified as outliers.

    Returns:
    --------
        mask : A numobservations-length boolean array.

    """
    median = points.median()
    diff = (points - median).abs()
    med_deviation = diff.median()

    modified_z_score = 0.6745 * diff / med_deviation

    return modified_z_score > thresh


def get_number_of_observations(df: pd.DataFrame) -> pd.Series:
    return (df.diff().abs() > 0).sum()


def comp(returns):
    """Calculates total compounded returns"""
    return returns.add(1).prod(axis=0) - 1


def to_drawdown_series(returns: pd.Series) -> pd.Series:
    """Convert returns series to drawdown series"""
    prices = to_prices(returns)
    dd = prices / np.maximum.accumulate(prices) - 1.0
    return dd.replace([np.inf, -np.inf, -0], 0)


def ulcer_index(returns: pd.Series) -> float:
    """Calculates the ulcer index score (downside risk measurment)"""
    dd = to_drawdown_series(returns)
    return np.sqrt(np.divide((dd**2).sum(), returns.shape[0] - 1))


def ulcer_performance_index(returns: pd.Series, rf=0) -> float:
    """
    Calculates the ulcer index score
    (downside risk measurment)
    """
    return (comp(returns) - rf) / ulcer_index(returns)


def safe_pearson(x: pd.Series, y: pd.Series) -> float:
    """
    Safely calculate the pearson correlation coefficient
    """
    not_na_mask = x.notna() & y.notna()
    x = x[not_na_mask]
    y = y[not_na_mask]
    if x.var() == 0 or y.var() == 0:
        return 0
    return x.corr(y, method="pearson")


def cagr(returns, rf=0.0, compounded=True, periods=252):
    """
    Calculates the communicative annualized growth return
    (CAGR%) of access returns

    If rf is non-zero, you must specify periods.
    In this case, rf is assumed to be expressed in yearly (annualized) terms
    """
    total = comp(returns)
    years = (returns.index[-1] - returns.index[0]).days / periods
    return abs(total + 1.0) ** (1.0 / years) - 1


def get_rolling_sharpe(
    returns: pd.Series,
    window: int,
    step: int,
    annualization_period: int,
) -> pd.Series:
    return (
        returns.rolling(window, min_periods=window, step=step)
        .apply(partial(sharpe, annualization_period=annualization_period))
        .dropna()
        .rename(f"rolling_sharpe_{window}")
    )


def idiosyncratic_sharpe(
    returns: pd.Series, underlying: pd.Series, annualization_period: int
) -> float:
    correlation_to_underlying = abs(returns.corr(underlying)) or 1.0
    return sharpe(returns, annualization_period) * (1 - correlation_to_underlying)


def get_rolling(
    returns: pd.Series,
    underlying: pd.Series,
    window: int,
    mode: Literal[
        "alpha", "geometric_alpha", "beta", "pearson_corr", "idiosyncratic_sharpe"
    ],
    step: int,
    annualization_period: int,
    min_periods: int | None = None,
) -> pd.Series:
    min_periods = min_periods if min_periods is not None else window
    func = partial(geometric_alpha, annualization_period=annualization_period)
    if mode == "alpha":
        func = partial(alpha, annualization_period=annualization_period)
    elif mode == "beta":
        func = beta
    elif mode == "pearson_corr":
        func = safe_pearson
    elif mode == "idiosyncratic_sharpe":
        func = lambda x, y: idiosyncratic_sharpe(x, y, annualization_period)  # noqa

    def func_to_apply(x, y):
        if len(x) < window:
            return 0
        return func(x, y)

    output = pd.Series(
        {
            returns.index[-1]: func_to_apply(returns, underlying)
            for returns, underlying in zip(
                returns.rolling(window, min_periods=min_periods, step=step),
                underlying.rolling(window, min_periods=min_periods, step=step),
                strict=True,
            )
        },
    ).iloc[int(min_periods / step) :]

    return output.dropna().rename(f"rolling_{mode}_{window}")


def get_rolling_greeks(
    returns: pd.Series,
    underlying: pd.Series,
    window: int,
    step: int,
    annualization_period: int,
) -> pd.Series:
    df = pd.DataFrame(
        data={
            "returns": returns,
            "underlying": underlying,
        }
    )
    df = df.fillna(0)
    corr = (
        df.rolling(window, min_periods=window)  # step=step)
        .corr()
        .unstack()["returns"]["underlying"]
    )
    std = df.rolling(window, min_periods=window).std()  # step=step
    beta = corr * std["returns"] / std["underlying"]
    alpha = df["returns"].mean() - abs(beta) * df["underlying"].mean() * sqrt(
        annualization_period
    )
    return pd.DataFrame(
        index=returns.index,
        data={f"rolling_beta_{window}": beta, f"rolling_alpha_{window}": alpha},
    )


Sharpe = float


def __prepare_one_sides_returns_underlying(
    returns: pd.Series, underlying: pd.Series, side: Literal["upside", "downside"]
) -> tuple[pd.Series, pd.Series]:
    if side == "upside":
        intersection = underlying[underlying > 0].index.intersection(returns.index)
    elif side == "downside":
        intersection = underlying[underlying < 0].index.intersection(returns.index)
    else:
        raise ValueError("side must be either 'upside' or 'downside'")

    one_side_underlying = underlying.loc[intersection]
    one_side_returns = returns.loc[intersection]

    return one_side_returns, one_side_underlying


def weighted_downside_beta(returns: pd.Series, underlying: pd.Series) -> float:
    downside_returns, downside_underlying = __prepare_one_sides_returns_underlying(
        returns, underlying, "downside"
    )
    weights = downside_underlying / downside_underlying.sum()

    matrix = np.cov(downside_returns, downside_underlying, aweights=weights)
    return matrix[0, 1] / matrix[1, 1]


def downside_beta(returns: pd.Series, underlying: pd.Series) -> float:
    downside_returns, downside_underlying = __prepare_one_sides_returns_underlying(
        returns, underlying, "downside"
    )
    return beta(downside_returns, downside_underlying)


def upside_beta(returns: pd.Series, underlying: pd.Series) -> float:
    upside_returns, upside_underlying = __prepare_one_sides_returns_underlying(
        returns, underlying, "upside"
    )
    return beta(upside_returns, upside_underlying)


def upside_correlation(
    returns: pd.Series,
    underlying: pd.Series,
    method: Literal["pearson", "kendall", "spearman"] = "pearson",
) -> float:
    upside_returns, upside_underlying = __prepare_one_sides_returns_underlying(
        returns, underlying, "upside"
    )
    return upside_returns.corr(upside_underlying, method=method)


def downside_correlation(
    returns: pd.Series,
    underlying: pd.Series,
    method: Literal["pearson", "kendall", "spearman"] = "pearson",
) -> float:
    downside_returns, downside_underlying = __prepare_one_sides_returns_underlying(
        returns, underlying, "downside"
    )
    return downside_returns.corr(downside_underlying, method=method)
