# Test if the country has the correct value for the given data in the data frame
def assert_value(value, country, date, df):
    print(df.columns)
    indicator_column = df.columns[-1]
    print(indicator_column)
    value_in_df = df.loc[(df['country'] == country) & (df['date'] == date), indicator_column].values[0]
    assert value_in_df == value
