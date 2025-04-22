from collections.abc import Callable

import pandas as pd
from pandas.core.indexers.objects import (
    FixedForwardWindowIndexer,
    VariableOffsetWindowIndexer,
)
from pandas.tseries.offsets import BaseOffset


def variable_rolling(
    df: pd.Series | pd.DataFrame,
    window: int,
    offset: type[BaseOffset],
    min_periods: int | None,
) -> pd.core.window.rolling.Rolling:
    if offset == pd.offsets.Day:
        return df.rolling(window=f"{window}D", min_periods=min_periods)

    return df.rolling(
        window=VariableOffsetWindowIndexer(index=df.index, offset=offset(window)),
        min_periods=min_periods,
    )


def create_forward_rolling(
    transformation_func: Callable | None,
    agg_func: Callable,
    series: pd.Series,
    period: int,
    extra_shift_by: int | None,
    offset: type[BaseOffset] | None,
    min_periods: int,
) -> pd.Series:
    assert period > 0
    extra_shift_by = abs(extra_shift_by) if extra_shift_by is not None else 0
    transformation_func = transformation_func if transformation_func else lambda x: x

    transformed = transformation_func(series)

    rolled = (
        variable_rolling(
            transformed,
            window=period,
            offset=offset,
            min_periods=min_periods,
        )
        if offset is not None
        else transformed.shift(-extra_shift_by - 1).rolling(
            window=FixedForwardWindowIndexer(window_size=period)
        )
    )

    return agg_func(rolled)
