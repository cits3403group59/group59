import pandas as pd

# Create dummy user dataset with a mix of continuous and categorical (one-hot, multi-hot, ordinal, binary) variables
df = pd.DataFrame({
    'sleep_hours': [5, 6, 7],
    'exercise_hours': [0.5, 1, 2],
    'caffeine_intake': [1, 2, 10],
    'screen_time': [1, 2, 3],
    'work_hours':[5, 10, 15],
    'outside_time': [0.2, 1, 10],
    'weekly_spend': [10, 100, 1000],
    'step_count': [20000, 500, 8000],
    'time_with_friends': [2, 5, 10],
    'salary': [70000, 100000, 20000],
    'transport': ['bicycle', 'car', 'walking'],
    'hobbies': [['computer programming', 'cooking'], ['creative writing'], ['musical intruments', 'sport']], 
    'applications_used': [['Facebook', 'Instagram'], ['TikTok'], ['YouTube', 'WhatsApp']],
    'alcohol_usage': ['Yes', 'No', 'Yes'],
    'vehicle_ownership': ['Yes', 'Yes', 'No']
})

# Convert list-type columns to pipe-separated strings for CSV storage (only applicable to dummy data)
df['hobbies'] = df['hobbies'].apply(lambda x: '|'.join(x))
df['applications_used'] = df['applications_used'].apply(lambda x: '|'.join(x))

df.to_csv('dummy_data.csv', index=False)