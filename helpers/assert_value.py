# Test if the country has the correct value for the given data in the data frame
def assert_value(value, country, date, df):
    assert df.loc[(df['country'] == country) & (df['date'] == date), 'value'].values[0] == value
