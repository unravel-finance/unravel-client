from random import choices

import numpy as np
import pandas as pd


def generate_sine_wave_data(
    cycles: int = 2, length: int = 1000, freq: str = "min"
) -> tuple[pd.DataFrame, pd.Series]:
    end_value = np.pi * 2 * cycles
    my_wave = np.sin(np.linspace(0, end_value, length + 1))
    series = pd.Series(
        my_wave,
        name="sine",
        index=pd.date_range(end="2022", periods=len(my_wave), freq=freq),
    ).round(4)
    X = series.to_frame()
    y = series.shift(-1)[:-1]
    X = X[:-1]
    return X, y


def generate_all_zeros(length: int = 1000) -> tuple[pd.DataFrame, pd.Series]:
    length += 1
    series = pd.Series(
        [0] * length,
        index=pd.date_range(end="2022", periods=length, freq="m"),
    )
    X = series.to_frame()
    y = series.shift(-1)[:-1]
    X = X[:-1]
    return X, y


def generate_zeros_and_ones(
    length: int = 1000, labels=None
) -> tuple[pd.DataFrame, pd.Series]:
    if labels is None:
        labels = [1, 0]
    return generate_zeros_and_ones_skewed(length, labels, weights=[0.5, 0.5])


def generate_zeros_and_ones_skewed(
    length: int = 1000, labels=None, weights: list[float] | None = None
) -> tuple[pd.DataFrame, pd.Series]:
    if weights is None:
        weights = [0.2, 0.8]
    if labels is None:
        labels = [1, 0]
    length += 1
    series = pd.Series(
        choices(population=labels, weights=weights, k=length),
        index=pd.date_range(end="2022", periods=length, freq="s"),
    )
    X = series.to_frame()
    y = series.shift(-1)[:-1]
    X = X[:-1]
    return X, y


def generate_monotonous_data(
    length: int = 1000, freq: str = "m"
) -> tuple[pd.DataFrame, pd.Series]:
    values = np.linspace(0, 1, num=length + 1)
    series = pd.Series(
        values,
        name="linear",
        index=pd.date_range(end="2022", periods=len(values), freq=freq),
    )
    X = series.to_frame()
    y = series.shift(-1)[:-1]
    X = X[:-1]
    return X, y
