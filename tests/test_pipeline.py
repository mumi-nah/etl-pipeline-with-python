import pandas as pd
from src.transform import unnest, get_cols, transform


def test_unnest_creates_dataframe():
    raw_data = [
        {"name": {"common": "Vatican City", "official": "Vatican City State"},
            "languages": {"ita": "Italian", "lat": "Latin"}}
        ]
    df = unnest(raw_data)
    assert isinstance(df, pd.DataFrame)
    assert 'official_name' in df.columns
    assert df.loc[0, 'lang_count'] == 2


def get_cols_calling_code():
    df = pd.DataFrame([{
        "root": "+3",
        "suffixes": ["906698", "79"]
      }])
    df = get_cols(df)
    assert 'calling_code' in df.columns


def transform_handles_missing_file():
    path = 'temp/missing.json'
    result = transform(path)
    assert result is None
