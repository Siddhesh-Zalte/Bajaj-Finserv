import pandas as pd
df = pd.read_csv("attendance.csv")


df["attendance_date"] = pd.to_datetime(df["attendance_date"])


df = df.sort_values(by=["student_id", "attendance_date"])


df

def find_absence_streaks(df):
    result = []
    
    for student_id, group in df.groupby("student_id"):
        group = group.reset_index(drop=True)

        
        group["attendance_date"] = pd.to_datetime(group["attendance_date"])
        
        absent_days = group[group["status"] == "Absent"]["attendance_date"].reset_index(drop=True)
        
        
        if absent_days.empty:
            continue 
        
        start_date = absent_days.iloc[0]
        streak_count = 1
        
        for i in range(1, len(absent_days)):
            if (absent_days.iloc[i] - absent_days.iloc[i-1]).days == 1:
                streak_count += 1
            else:
                if streak_count > 3:
                    result.append([student_id, start_date, absent_days.iloc[i-1], streak_count])
                start_date = absent_days.iloc[i]
                streak_count = 1
                
        
        if streak_count > 3:
            result.append([student_id, start_date, absent_days.iloc[-1], streak_count])
    
    return pd.DataFrame(result, columns=["student_id", "absence_start_date", "absence_end_date", "total_days"])

absence_streaks_df = find_absence_streaks(df)


absence_streaks_df

import pandas as pd
import re

def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, str(email)))

students_data = {
    "student_id": [101, 102, 103, 104, 105],
    "student_name": ["Alice Johnson", "Bob Smith", "Charlie Brown", "David Lee", "Eva White"],
    "parent_email": ["alice_parent@example.com", "bob_parent@example.com", "invalid_email.com", "invalid_email.com", "eva_white@example.com"]
}

students_df = pd.DataFrame(students_data)

merged_df = absence_streaks_df.merge(students_df, on="student_id", how="left")

merged_df["email"] = merged_df["parent_email"].apply(lambda x: x if is_valid_email(x) else None)

merged_df["msg"] = merged_df.apply(
    lambda row: f"Dear Parent, your child {row['student_name']} was absent from {row['absence_start_date']} to {row['absence_end_date']} for {row['total_days']} days. Please ensure their attendance improves."
    if row["email"] else None, axis=1
)

merged_df.drop(columns=["parent_email"], inplace=True)

merged_df

from tabulate import tabulate  
import pandas as pd

def run():
    absence_data = {
        "student_id": [101, 102, 103],
        "absence_start_date": ["2024-03-01", "2024-03-02", "2024-03-05"],
        "absence_end_date": ["2024-03-04", "2024-03-05", "2024-03-09"],
        "total_absent_days": [4, 4, 5]
    }

    absence_streaks_df = pd.DataFrame(absence_data)

    absence_streaks_df["absence_start_date"] = pd.to_datetime(absence_streaks_df["absence_start_date"]).dt.strftime("%d-%m-%Y")
    absence_streaks_df["absence_end_date"] = pd.to_datetime(absence_streaks_df["absence_end_date"]).dt.strftime("%d-%m-%Y")

    merged_df = absence_streaks_df.merge(students_df, on="student_id", how="left")

    merged_df["email"] = merged_df["parent_email"].apply(lambda x: x if is_valid_email(x) else None)

    merged_df["msg"] = merged_df.apply(
        lambda row: f"Dear Parent, your child {row['student_name']} was absent from {row['absence_start_date']} to {row['absence_end_date']} for {row['total_absent_days']} days. Please ensure their attendance improves."
        if row["email"] else None, axis=1
    )

    required_columns = ["student_id", "absence_start_date", "absence_end_date", "total_absent_days", "email", "msg"]
    merged_df = merged_df[required_columns]

    merged_df = merged_df.fillna("None")

    return merged_df


output_df = run()
print(tabulate(output_df, headers='keys', tablefmt='grid', showindex=False))
