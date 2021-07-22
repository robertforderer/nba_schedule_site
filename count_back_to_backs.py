import pandas as pd
import csv

schedule_df = pd.read_csv(r"C:\Users\rober\OneDrive\Documents\Roberts Side Projects\May 22 output\2018-2019 actual_schedule_different_format.csv")
output_file_path = r"C:\Users\rober\OneDrive\Documents\Roberts Side Projects\May 22 output\back_to_back_output.csv"

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
final_output = []
final_output.append(["day", "back_to_back_team"])
for col in range(len(schedule_df.columns)):

    for team in team_list:
        schedule_day = list(schedule_df.iloc[:,col])
        schedule_day = [x for x in schedule_day if str(x) != 'nan']
        teams_playing = home_and_away_one_day(schedule_day)
        # so out of bounds does not occur
        if col < len(schedule_df.columns)-1:
            schedule_day_plus_one = list(schedule_df.iloc[:,col+1])
            schedule_day_plus_one = [x for x in schedule_day_plus_one if str(x) != 'nan']
            teams_playing_tomorrow = home_and_away_one_day(schedule_day_plus_one)


        if team in teams_playing and team in teams_playing_tomorrow and col > 0:
            inner_output = []
            inner_output.append(col)
            inner_output.append(team)
            final_output.append(inner_output)


with open(output_file_path, "w", newline = '') as csv_output:
    wr = csv.writer(csv_output)

    wr.writerows(final_output)

