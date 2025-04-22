import numpy as np
import pandas as pd

from src.finml_utils.dataframes import (
    add_last_day_if_different,
    concat_on_index_without_duplicates,
    rebase,
    remove_constant_columns,
    trim_initial_nans,
)


def test_trim_initial_nans():
    X = pd.DataFrame(
        {
            "a": [np.nan, np.nan, 3, 4, 5],
            "b": [np.nan, np.nan, np.nan, 4, 5],
        }
    )

    assert trim_initial_nans(X).equals(X.iloc[2:])

    X = pd.DataFrame(
        {
            "a": [0.0, 0.0, 3, 4, 5],
            "b": [np.nan, np.nan, 0.1, 4, 5],
        }
    )

    assert trim_initial_nans(X).equals(X)


def list_the_same(a: pd.Series, b: list):
    return (~(a.replace(np.nan, None).to_numpy() == np.array(b))).sum() == 0


def test_concat_on_index_without_duplicates():
    df1 = pd.DataFrame({"col_a": [11, 12, None], "col_b": [5, 6, 7]}, index=[2, 3, 4])
    df2 = pd.DataFrame({"col_a": [1, None, 3, 4]}, index=[1, 2, 3, 4])

    df_last = concat_on_index_without_duplicates([df1, df2], keep="last")
    df_first = concat_on_index_without_duplicates([df1, df2], keep="first")

    assert len(df_last) == 4
    assert list_the_same(df_last["col_b"], [None, 5.0, 6.0, 7.0])
    assert list_the_same(df_last["col_a"], [1.0, 11.0, 3.0, 4.0])
    assert df_last.columns.to_list() == ["col_a", "col_b"]
    assert isinstance(df_last, pd.DataFrame)

    assert len(df_first) == 4
    assert list_the_same(df_first["col_b"], [None, 5.0, 6.0, 7.0])
    assert list_the_same(df_first["col_a"], [1.0, 11.0, 12.0, 4.0])
    assert df_first.columns.to_list() == ["col_a", "col_b"]
    assert isinstance(df_first, pd.DataFrame)

    ds_1 = pd.Series([11, 12, None], index=[2, 3, 4])
    ds_2 = pd.Series([1, None, 3, 4], index=[1, 2, 3, 4])
    ds_last = concat_on_index_without_duplicates([ds_1, ds_2], keep="last")
    ds_first = concat_on_index_without_duplicates([ds_1, ds_2], keep="first")

    assert isinstance(ds_last, pd.Series)
    assert isinstance(ds_first, pd.Series)
    assert ds_last.isna().sum() == 0
    assert ds_first.isna().sum() == 0

    df1 = pd.DataFrame({"col_a": [11, 12, None], "col_b": [5, 6, 7]}, index=[2, 3, 4])
    df2 = pd.DataFrame({"col_a": [1, None, 3, 4]}, index=[1, 2, 3, 4])
    df3 = pd.DataFrame(
        {"col_a": [21, 22, 23, None, 24], "col_b": [21, 22, 23, 24, 25]},
        index=[3, 4, 5, 6, 7],
    )

    df_last_multiple = concat_on_index_without_duplicates([df1, df2, df3], keep="last")
    df_first_multiple = concat_on_index_without_duplicates(
        [df1, df2, df3], keep="first"
    )

    assert len(df_last_multiple) == 7
    assert list_the_same(df_last_multiple["col_a"], [1, 11, 21, 22, 23, None, 24])
    assert list_the_same(df_last_multiple["col_b"], [None, 5, 21, 22, 23, 24, 25])
    assert df_last_multiple.columns.to_list() == ["col_a", "col_b"]
    assert isinstance(df_last_multiple, pd.DataFrame)

    assert len(df_first_multiple) == 7
    assert list_the_same(df_first_multiple["col_a"], [1, 11, 12, 4, 23, None, 24])
    assert df_first_multiple.columns.to_list() == ["col_a", "col_b"]
    assert isinstance(df_first_multiple, pd.DataFrame)

    for d in [
        ds_last,
        ds_first,
        df_last,
        df_first,
        df_first_multiple,
        df_last_multiple,
    ]:
        assert d.index.duplicated().sum() == 0
        assert d.index.is_monotonic_increasing


def test_rebase():
    ds = pd.Series(np.random.rand(100) * 1000)

    rebased_ds = rebase(ds)

    assert rebased_ds.iloc[0] == 1.0


def test_add_last_day_if_different():
    data = pd.DataFrame(
        {"col1": [1, 2, 3, 4, 5]},
        index=pd.date_range("2024-05-13", periods=5, freq="D"),
    )
    underlying = pd.Series(
        [11, 22, 33, 44, 55], index=pd.date_range("2024-05-13", periods=5, freq="D")
    )

    data_adjusted, underlying_adjusted = add_last_day_if_different(
        data, underlying.iloc[:-1]
    )
    assert data_adjusted.index[-1] == underlying_adjusted.index[-1]

    data_adjusted, underlying_adjusted = add_last_day_if_different(
        data.iloc[:-1], underlying
    )
    assert data_adjusted.index[-1] == underlying_adjusted.index[-1]

    data_adjusted, underlying_adjusted = add_last_day_if_different(data, underlying)
    assert data_adjusted.index[-1] == underlying_adjusted.index[-1]


def test_remove_constant_columns():
    df = pd.DataFrame(
        {
            "col1": [1, 2, 3, 4, 5],
            "col2": [1, 1, 1, 1, 1],
            "col3": [1, 2, 3, 4, 5],
        }
    )
    df = remove_constant_columns(df)

    assert df.columns.to_list() == ["col1", "col3"]
    assert df.equals(pd.DataFrame({"col1": [1, 2, 3, 4, 5], "col3": [1, 2, 3, 4, 5]}))

    df = pd.DataFrame(
        {
            "col1": [1, 2, 3, 4, 5],
            "col2": [1, 1, 1, 1, 1],
            "col3": [np.nan, np.nan, np.nan, np.nan, np.nan],
        }
    )
    df = remove_constant_columns(df)
    assert df.columns.to_list() == ["col1"]

    df = pd.DataFrame(
        {
            "col1": [1, 2, 3, 4, 5],
            "col2": [np.nan, 0, 0, 0, 0],
            "col3": [np.nan, 1, 1, 1, 1],
            "col4": [np.nan, np.nan, np.nan, np.nan, np.nan],
        }
    )
    df = remove_constant_columns(df)
    assert df.columns.to_list() == ["col1"]
