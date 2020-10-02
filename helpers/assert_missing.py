# Test if the country has a missing value for the given data in the data frame
def assert_missing(country, date, df):
    indicator_column = df.columns[-1]
    value_in_df = df.loc[
        (df["iso_code"] == country) & (df["date"] == date), indicator_column
    ].values

    print("Value in data:", value_in_df)

    assert len(value_in_df) == 0
