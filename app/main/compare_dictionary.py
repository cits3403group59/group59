from app.models import UserData
from datetime import datetime

def get_latest_data(user):
    return UserData.query.filter_by(user_id=user.id).order_by(UserData.date.desc()).first()

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
    num_compared_fields = 0

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
    }
    nominal_fields = ["social_media", "transportation", "mood"]
    time_fields = ["wake_up_time", "bed_time"]

    for field in user1_data:
        if field in user2_data:
            val1 = user1_data[field]
            val2 = user2_data[field]
            
            similarity = 0

            if field in numerical_fields:
                similarity = numerical_similarity(val1, val2, numerical_fields[field])
            elif field in nominal_fields:
                similarity = 1 if val1 == val2 else 0
            elif field in time_fields:
                similarity = time_similarity(val1, val2)
            else:
                continue
            
            total_similarity += similarity
            num_compared_fields += 1
    
    return total_similarity / num_compared_fields if num_compared_fields else 0

def numerical_similarity(val1, val2, max_diff):
    try:
        diff = abs(float(val1) - float(val2))
        similarity = 1 - (diff / max_diff)
        return max(0, similarity)
    except:
        return 0
        
def time_similarity(time1, time2):
    def time_to_minutes(time):
        try:
            hours, minutes = map(int, time.split(':'))
            return hours * 60 + minutes
        except:
            return 0
    
    t1 = time_to_minutes(time1)
    t2 = time_to_minutes(time2)
    diff = abs(t1 - t2)
    circular_diff = min(diff, 1440 - diff)
    similarity = 1 - (circular_diff / 720)
    return similarity

