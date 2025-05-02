"""
Preprocesses a dummy dataset containing lifestyle and behavioural features for user similarity scoring. This includes:

- Min-Max scaling of continuous fields
- One-hot and multi-hot encoding of categorical fields
- Binary conversion of Yes/No values
- Derived ordinal features for spending habits and salary range
- Cosine similarity calculation to find most similar user
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity

data = pd.read_csv('dummy_data.csv')

# Save original salary and spending values before scaling (used to derive ordinal categories)
data['weekly_spend_raw'] = data['weekly_spend']
data['salary_raw'] = data['salary']

# Normalise continuous features using Min-Max scaling
continuous_variables = ['sleep_hours', 'exercise_hours', 'caffeine_intake', 'screen_time', 'work_hours', 'outside_time', 'weekly_spend', 'step_count', 'time_with_friends', 'salary']
scaler = MinMaxScaler()
data[continuous_variables] = scaler.fit_transform(data[continuous_variables])

# One-hot encode transport type
data = pd.get_dummies(data, columns=['transport'], dtype=float)

# Split pipe-separated strings into lists for multi-hot encoding
data['hobbies'] = data['hobbies'].str.split('|')
data['applications_used'] = data['applications_used'].str.split('|')

def multi_hot_encode(df, column_name):
    all_items = set(item for sublist in df[column_name] for item in sublist)
    for item in all_items:
        col = f"{column_name}_{item.strip().lower().replace(' ', '_')}"
        df[col] = df[column_name].apply(lambda x: 1 if item in x else 0)
    return df

# Apply multi-hot encoding to hobbies and apps
data = multi_hot_encode(data, 'hobbies')
data = multi_hot_encode(data, 'applications_used')

# Drop original list columns after encoding
data.drop(columns=['hobbies', 'applications_used'], inplace=True)

# Convert Yes/No binary fields to 1/0
binary_map = {'Yes': 1, 'No': 0}
data['alcohol_usage'] = data['alcohol_usage'].map(binary_map)
data['vehicle_ownership'] = data['vehicle_ownership'].map(binary_map)

# Derive spending rate from original (unscaled) spend/salary
data['spending_rate'] = data['weekly_spend_raw'] / data['salary_raw']

def classify_spending(rate):
    if rate < 0.5:
        return "low"
    elif rate >= 0.5 and rate <= 0.7:
        return "medium"
    else:
        return "high"

# Apply spending level classification
data['spending_level'] = data['spending_rate'].apply(classify_spending)

# Define ordinal mapping for categorical levels
ordinal_map = {'low': 0, 'medium': 1, 'high':2}
data['spending_level'] = data['spending_level'].map(ordinal_map)


def get_salary_range(salary_value):
    if salary_value < 60000:
        return "low"
    elif salary_value >= 60000 and salary_value <= 120000:
        return "medium"
    else:
        return "high"

# Apply salary range classification
data['salary_range'] = data['salary_raw'].apply(get_salary_range)
data['salary_range'] = data['salary_range'].map(ordinal_map)

# Remove temporary columns used for classification
data.drop(columns=['weekly_spend_raw', 'salary_raw', 'spending_rate'], inplace=True)

# Compute cosine similarity between users
similarity_matrix = cosine_similarity(data)

for i in range(len(similarity_matrix)):
    sims = similarity_matrix[i].copy()
    sims[i] = -1
    best_match = np.argmax(sims)
    print(f"User {i} is most similar to User {best_match} (Score: {sims[best_match]:.2f})")