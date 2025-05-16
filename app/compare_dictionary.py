"""
This module handles data twin logic for comparing the current user's most recent UserData entry with their friends. 
It finds the data twin (friend with highest similarity score) and the similarity scores for each feature, using normalised comparison for numerical values, categorical equality, & circular time comparison.

Exports:
- find_data_twin(current_user): Finds the current user's most similar friend, based on the average similarity score (of all features)
- get_twin_feature_comparisons(user, twin): Returns a dictionary containing similarity scores for all features.
"""

from app.models import UserData
from datetime import datetime

# Defines the feature types and normalisation bounds
numerical_fields = {
    "sleep_hours": 24,
    "coffee_intake": 20,
    "daily_steps": 100000,
    "screen_time": 24,
    "work_time": 24,
    "study_time": 24,
    "social_time": 24,
    "money_spent": 1000,
    "exercise_hours": 24,
    "alcohol": 20
}
nominal_fields = ["social_media", "transportation", "mood"]
time_fields = ["wake_up_time", "bed_time"]
all_features = list(numerical_fields.keys()) + nominal_fields + time_fields

def get_latest_data(user):
    return UserData.query.filter_by(user_id=user.id).order_by(UserData.date.desc()).first()

# Overall similarity score is a float between 0 & 1
def find_data_twin(current_user):
    current_data = get_latest_data(current_user)
    if not current_data:
        return None, 0

    current_data_dict = current_data.__dict__.copy()
    current_data_dict.pop("_sa_instance_state", None)

    best_match = None
    highest_similarity = -1

    for friend in current_user.get_user_friends():
        friend_data = get_latest_data(friend)
        if not friend_data:
            continue

        friend_data_dict = friend_data.__dict__.copy()
        friend_data_dict.pop("_sa_instance_state", None)

        score = calculate_similarity(current_data_dict, friend_data_dict)
        if score > highest_similarity:
            highest_similarity = score
            best_match = friend

    return best_match, highest_similarity

def calculate_similarity(user1_data, user2_data):
    total_similarity = 0
    count = 0
    for field in all_features:
        if field not in user1_data or field not in user2_data:
            continue

        val1, val2 = user1_data[field], user2_data[field]
        sim = get_similarity_score(field, val1, val2)
        total_similarity += sim
        count += 1
    return total_similarity / count if count else 0

# Generates per-feature comparisons between current user & their data twin.
# Returns a dictionary in the following form: {'you': val, 'twin': val, 'match': %}
def get_twin_feature_comparisons(user, twin):
    user_data = get_latest_data(user)
    twin_data = get_latest_data(twin)

    if not user_data or not twin_data:
        return {}

    u_dict, t_dict = user_data.__dict__, twin_data.__dict__
    comparison = {}

    for field in all_features:
        user_val = u_dict.get(field)
        twin_val = t_dict.get(field)
        if user_val is None or twin_val is None:
            continue
        match_score = get_similarity_score(field, user_val, twin_val)
        comparison_key = get_ui_key(field)
        comparison[comparison_key] = {
            'you': user_val,
            'twin': twin_val,
            'match': round(match_score * 100, 1)
        }

    return comparison

# Route similarity logic based on the feature type (i.e. numerical, nominal, time)
def get_similarity_score(field, val1, val2):
    if field in numerical_fields:
        return numerical_similarity(val1, val2, numerical_fields[field])
    elif field in nominal_fields:
        return 1 if val1 == val2 else 0
    elif field in time_fields:
        return time_similarity(val1, val2)
    return 0

# Normalise numerical difference between two values based on a max_diff scale
def numerical_similarity(val1, val2, max_diff):
    try:
        diff = abs(float(val1) - float(val2))
        return max(0, min(1 - (diff / max_diff), 1))
    except:
        return 0

# Compares two time strings (HH:MM) using circular wrap around logic.
# Returns similarity from 0 to 1
def time_similarity(time1, time2):
    def to_minutes(t):
        try:
            h, m = map(int, t.split(':'))
            return h * 60 + m
        except:
            return 0
    t1, t2 = to_minutes(time1), to_minutes(time2)
    diff = abs(t1 - t2)
    circ_diff = min(diff, 1440 - diff)
    return max(0, min(1 - (circ_diff / 720), 1))

# Map internal field names to frontend keys that are used in HTML & JS
def get_ui_key(field):
    return {
        "sleep_hours": "sleep",
        "coffee_intake": "coffee",
        "daily_steps": "steps",
        "wake_up_time": "wakeup",
        "bed_time": "bed",
        "exercise_hours": "exercise",
        "money_spent": "money",
        "screen_time": "screen",
        "social_time": "social",
        "study_time": "study",
        "alcohol": "alcohol",
        "work_time": "work",
        "mood": "mood",
        "social_media": "app",
        "transportation": "transport"
    }.get(field, field)
