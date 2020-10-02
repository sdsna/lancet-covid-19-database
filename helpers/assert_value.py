# Test if the country has the correct value for the given data in the data frame
# Optionally, supply the number of decimals to round the value to
def assert_value(value, country, date, df, decimals=None):
    indicator_column = df.columns[-1]
    value_in_df = df.loc[
        (df["iso_code"] == country) & (df["date"] == date), indicator_column
    ].values[0]

    print("Value in data:", value_in_df)

    # Round value, if decimals argument was given
    if decimals:
        value_in_df = round(value_in_df, decimals)

    assert value_in_df == value
