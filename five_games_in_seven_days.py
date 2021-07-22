import pandas as pd
import csv

schedule_df = pd.read_csv(r"C:\Users\rober\OneDrive\Documents\Roberts Side Projects\May 22 output\2018-2019 actual_schedule_different_format.csv")
output_file_path = r"C:\Users\rober\OneDrive\Documents\Roberts Side Projects\May 22 output\five_games_in_seven_days_output.csv"

def home_and_away_one_day(list):

    home_list = []
    away_list = []
    for game in list:
        if '@' in game:
            game_list = game.split("@")
            away_team = game_list[0]
            away_list.append(away_team)
            home_team = game_list[1]
            home_list.append(home_team)

    teams_playing = away_list + home_list
    return teams_playing


team_list = list(schedule_df.iloc[:,0])
print(team_list)
final_output = []
final_output.append(["day", "five_games_in_seven_days_team"])
for col in range(len(schedule_df.columns)):
    # preventing out of bounds error
    if col < 177:
        schedule_day = list(schedule_df.iloc[:, col])
        schedule_day = [x for x in schedule_day if str(x) != 'nan']
        teams_playing = home_and_away_one_day(schedule_day)
        schedule_day_plus_one = list(schedule_df.iloc[:, col + 1])
        schedule_day_plus_one = [x for x in schedule_day_plus_one if str(x) != 'nan']
        teams_playing_plus_one = home_and_away_one_day(schedule_day_plus_one)
        schedule_day_plus_two = list(schedule_df.iloc[:, col + 2])
        schedule_day_plus_two = [x for x in schedule_day_plus_two if str(x) != 'nan']
        teams_playing_plus_two = home_and_away_one_day(schedule_day_plus_two)
        schedule_day_plus_three = list(schedule_df.iloc[:, col + 3])
        schedule_day_plus_three = [x for x in schedule_day_plus_three if str(x) != 'nan']
        teams_playing_plus_three = home_and_away_one_day(schedule_day_plus_three)
        schedule_day_plus_four = list(schedule_df.iloc[:, col + 4])
        schedule_day_plus_four = [x for x in schedule_day_plus_four if str(x) != 'nan']
        teams_playing_plus_four = home_and_away_one_day(schedule_day_plus_four)
        schedule_day_plus_five = list(schedule_df.iloc[:, col + 5])
        schedule_day_plus_five = [x for x in schedule_day_plus_five if str(x) != 'nan']
        teams_playing_plus_five = home_and_away_one_day(schedule_day_plus_five)
        schedule_day_plus_six = list(schedule_df.iloc[:, col + 6])
        schedule_day_plus_six = [x for x in schedule_day_plus_six if str(x) != 'nan']
        teams_playing_plus_six = home_and_away_one_day(schedule_day_plus_six)

    all_teams_playing_seven_days = teams_playing + teams_playing_plus_one + teams_playing_plus_two + teams_playing_plus_three + teams_playing_plus_four + teams_playing_plus_five + teams_playing_plus_six
    for team in team_list:
        games_in_next_seven_days_count = 0
        for team_playing in all_teams_playing_seven_days:
            if team == team_playing:
                games_in_next_seven_days_count += 1

        if games_in_next_seven_days_count > 4:
            inner_output_list = []
            inner_output_list.append(col)
            inner_output_list.append(team)
            final_output.append(inner_output_list)



with open(output_file_path, "w", newline = '') as csv_output:
    wr = csv.writer(csv_output)

    wr.writerows(final_output)

