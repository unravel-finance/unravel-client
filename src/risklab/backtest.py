from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


ReturnsDataFrame = pd.DataFrame
Returns = pd.Series
Signal = pd.Series


@dataclass
class BacktestResult:
    returns: Returns
    transaction_costs: pd.Series


def backtest_signal(
    signal: Signal,
    underlying: Returns,
    transaction_cost: float,
    lag: int,
) -> BacktestResult:
    """
    Create returns from a signal and a target.
    """
    assert isinstance(signal, pd.Series), "Signal must be a Series"
    signal = signal.ffill()
    underlying = underlying[signal.index[0] :]
    delta_pos = signal.diff(1).abs().fillna(0.0)
    costs = transaction_cost * delta_pos
    returns = (underlying * signal.shift(1 + lag)) - costs
    if returns.var() == 0.0:
        return BacktestResult(
            pd.Series(0.0, index=returns.index),
            transaction_costs=pd.Series(0.0, index=returns.index),
        )
    return BacktestResult(returns=returns, transaction_costs=costs)


@dataclass
class PortfolioBacktestResult:
    portfolio_returns: Returns
    component_returns: ReturnsDataFrame
    lag: int

    def split(self, start_date, end_date) -> PortfolioBacktestResult:
        return PortfolioBacktestResult(
            portfolio_returns=self.portfolio_returns[start_date:end_date],
            component_returns=self.component_returns[start_date:end_date],
            lag=self.lag,
        )


def backtest_portfolio(
    weights: pd.DataFrame,
    underlying: ReturnsDataFrame,
    transaction_cost: float,
    high_watermark_performance_fee: float | None,
    lag: int,
    fee_accounting_period: str = "ME",
) -> PortfolioBacktestResult:
    """
    Create returns from a signal and a target.
    """
    assert weights.columns.equals(underlying.columns), "Columns must match"
    underlying = underlying.loc[weights.index]
    weights = weights.ffill().reindex(underlying.index).ffill().copy()
    weights.columns = underlying.columns
    delta_pos = weights.diff(1).abs().fillna(0.0)
    costs = transaction_cost * delta_pos
    returns = (underlying * weights.shift(1 + lag)) - costs
    portfolio_returns = returns.sum(axis="columns")


    return PortfolioBacktestResult(
        portfolio_returns=portfolio_returns,
        component_returns=returns,
        portfolio_returns_after_fees=portfolio_returns - fees,
        lag=lag,
    )

