import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import math
from scipy.stats import chisquare


def load_data(input_file, sep='\t'):
    df = pd.read_csv(input_file, sep=sep)
    return df

def clean_data(df, col_name='7_2009'):
    """Remove NaN values and zeros from Dataframe column copy."""
    #TODO: input column requirements
    numbers = df[col_name].copy().dropna()
    numbers = numbers[numbers != 0]
    return numbers

def extract_leading_digits(numbers):
    return numbers.astype(str).str[:1].astype(int)

def count_frequency(digits):
    """Returns: Series with leading digit frequency in input data."""
    #TODO: always count 9 digits
    observed_freq = digits.value_counts(normalize=True)
    observed_freq.name = 'observed'
    return observed_freq

def count_benford_frequency():
    """Returns: Series with leading digit frequency according to Benford's Law."""
    data = [math.log10(1+1/x) for x in range(1, 10)]
    return pd.Series(data=data, index=range(1,10), name='expected')

def concat_into_df(observed, expected):
    """Returns: Dataframe with observed and expected data."""
    return pd.concat([observed, expected], axis=1)

def plot_frequencies(freq_df):
    """Saves bar plot of observed and expected leading digit frequency."""
    sns.set(font_scale=1)
    freq_df.plot(kind='bar', figsize=(7,6), rot=0)
    plt.title("Leading digit distribution", y=1.04)
    plt.xlabel('Leading digit')
    plt.ylabel('Relative frequency of occurrence')
    plt.savefig('./static/images/plot.png')
    return

def benford_test(input_fpath):
    """
    Plots data and runs chi square test of observed against expected data.

    Returns:
        Boolean:
            True: statistically relevant (observed data differs from expected data)
            False: statistically irrelevant
    """
    df = load_data(input_fpath)
    data = clean_data(df)
    digits = extract_leading_digits(data)
    observed_len = len(digits)
    observed = count_frequency(digits)
    expected = count_benford_frequency()
    frequencies = concat_into_df(observed, expected)
    chisq, pvalue = chisquare(observed.multiply(observed_len), expected.multiply(observed_len))
    plot_frequencies(frequencies)
    if pvalue < 0.05:
        return True
    else:
        return False

if __name__ == '__main__':
    input_fpath = '/Users/khaili/benford_flaskapp/uploads/census_2009b'
    benford_test(input_fpath)
