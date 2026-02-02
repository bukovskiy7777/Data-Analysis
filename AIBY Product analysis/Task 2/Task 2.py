import pandas as pd
from scipy.stats import chi2_contingency

# 1. Scenario: Testing two different website layouts (A and B) and recording conversions
n_A = 500000 # Number of visitors in Group A
n_B = 500000 # Number of visitors in Group B
conversions_A = 6798 # Number of conversions in Group A
conversions_B = 8008 # Number of conversions in Group B

# Create the contingency table
# The table should have rows for each group (A/B) and columns for the outcomes (Converted/Not Converted)
contingency_table = pd.DataFrame({
    'Converted': [conversions_A, conversions_B],
    'Not Converted': [n_A - conversions_A, n_B - conversions_B]
}, index=['Group A', 'Group B'])

print("Contingency Table:")
print(contingency_table)

# 2. Perform the Chi-Squared test
# The function returns the chi2 test statistic, the p-value, degrees of freedom, and expected frequencies
chi2_stat, p_value, dof, expected_freq = chi2_contingency(contingency_table)

print(f"\nChi-Squared Statistic: {chi2_stat}")
print(f"P-value: {p_value}")
print(f"Degrees of Freedom: {dof}")
print(f"Expected Frequencies Table:")
print(expected_freq)

# 3. Interpret the results
alpha = 0.05 # Significance level

if p_value < alpha:
    print("\nResult: Reject the null hypothesis.")
    print("Conclusion: There is a statistically significant difference in conversion rates between Group A and Group B (the change had an effect).")
else:
    print("\nResult: Fail to reject the null hypothesis.")
    print("Conclusion: There is no statistically significant difference in conversion rates between Group A and Group B (the difference is likely due to chance).")