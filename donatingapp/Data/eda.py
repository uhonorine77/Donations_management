import pandas as pd
import requests as req

def fetch_data(url):
    try:
        response = req.get(url)
        response.raise_for_status()
        return response.json() 
    except req.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None

def split_and_save_csv(df, file_name_part1, file_name_part2):
    df['id'] = df['users'].apply(lambda x: x.get('id', None))
    df['username'] = df['users'].apply(lambda x: x.get('username', None))
    df['email'] = df['users'].apply(lambda x: x.get('email', None))

    columns_part1 = ['id', 'username']
    columns_part2 = ['email']

    df_part1 = df[columns_part1]
    df_part2 = df[columns_part2]

    df_part1.to_csv(file_name_part1, index=False)
    df_part2.to_csv(file_name_part2, index=False)
    print(f"Data saved as {file_name_part1} and {file_name_part2}.")
    
def concatenate_and_print_csv(file_name_part1, file_name_part2):
    df_part1 = pd.read_csv(file_name_part1)
    df_part2 = pd.read_csv(file_name_part2)

    print(f"Part 1 (Columns: {df_part1.columns}):")
    print(df_part1.head(), "\n")

    print(f"Part 2 (Columns: {df_part2.columns}):")
    print(df_part2.head(), "\n")

    concatenated_df = pd.concat([df_part1, df_part2], axis=1)
    print("Concatenated DataFrame (Full Data):")
    print(f"All parts combined (Columns :{concatenated_df.columns}):")
    return concatenated_df

users_api_url = 'http://127.0.0.1:8000/user_list/'
users_data = fetch_data(users_api_url)

if users_data:
    users_df = pd.DataFrame(users_data)
    print(f"DataFrame shape (rows, columns): {users_df.shape}")
    print("\nData preview (first 5 rows):")
    print(users_df.head())
    
    split_and_save_csv(users_df, 'users_part1.csv', 'users_part2.csv')
    concatenated_df = concatenate_and_print_csv('users_part1.csv', 'users_part2.csv')
    
    concatenated_df.to_csv("combined_users.csv", index=False)
else:
    print("Failed to load user data!")
