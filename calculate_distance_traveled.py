import pandas as pd
import csv

distances = pd.read_csv(r"C:\Users\rober\OneDrive\Documents\Roberts Side Projects\May 22 output\all_distances.csv")
output_file_path = r"C:\Users\rober\OneDrive\Documents\Roberts Side Projects\May 22 output\jul_11_2021_distance_output.csv"
schedule_df = pd.read_csv(r"C:\Users\rober\OneDrive\Documents\Roberts Side Projects\May 22 output\full_schedule_jul_11_2021.csv")

def calculate_road_trip(road_trip_list):
    trip_count = 0
    road_trip_distance = 0
    road_trip_distances = []
    print(road_trip_list)
    for trip in road_trip_list:

        game_list = trip.split("@")
        home_team = game_list[1]
        away_team = game_list[0]

        print(trip)
        if trip_count == 0:

            distance = distances.loc[distances.prev_team == home_team, away_team].values[0]
            road_trip_distances.append(distance)
            road_trip_distance += distance
            prev_team = home_team

        else:
            print(prev_team)
            distance = distances.loc[distances.prev_team == prev_team, home_team].values[0]
            road_trip_distances.append(distance)
            road_trip_distance += distance
            prev_team = home_team

        if trip_count == len(road_trip_list) - 1:
            distance = distances.loc[distances.prev_team == away_team, home_team].values[0]
            road_trip_distances.append(distance)
            road_trip_distance += distance


        trip_count += 1

    return road_trip_distance, road_trip_distances


def get_road_trip(schedule_df, v_count, h_count):
    '''
    :return: full road trip when beginning of road trip is identified
    '''

    road_trip_list = []

    road_trip_list.append(schedule_df.iloc[v_count, h_count])
    # because a game is every other day, we go up and down by 2 to find when the road trip ends
    h_count += 2
    while str(schedule_df.iloc[v_count, h_count]) != "nan":
        road_trip_list.append(schedule_df.iloc[v_count, h_count])
        h_count += 2

    return road_trip_list


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

    return away_list, home_list



def get_road_trip_may_10(schedule_df, v_count, h_count):

    '''

    :return: above function relies on games every other day, I need something more flexible for actual nba schedule
    '''
    road_trip_list = []

    h_inc = h_count
    while h_inc < len(schedule_df.columns) - 1:

        if str(schedule_df.iloc[vertical_count, h_count]) != "nan" and "@" in str(
                schedule_df.iloc[vertical_count, h_count]):

            schedule_day_plus_one = list(schedule_df.iloc[:, h_inc + 1])
            schedule_day_plus_one = [x for x in schedule_day_plus_one if str(x) != 'nan']
            schedule_day_plus_two = list(schedule_df.iloc[:, h_inc + 2])
            schedule_day_plus_two = [x for x in schedule_day_plus_two if str(x) != 'nan']
            schedule_day_plus_three = list(schedule_df.iloc[:, h_inc + 3])
            schedule_day_plus_three = [x for x in schedule_day_plus_three if str(x) != 'nan']

            away_plus_one, home_plus_one = home_and_away_one_day(schedule_day_plus_one)
            away_plus_two, home_plus_two = home_and_away_one_day(schedule_day_plus_two)
            away_plus_three, home_plus_three = home_and_away_one_day(schedule_day_plus_three)

            # quick loop to find index of next away game
            next_game_int = 0

            next_four_days = list(schedule_df.iloc[v_count, h_inc+1:h_inc + 5])

            for day in next_four_days:

                if str(day) != "nan":
                    break

                next_game_int += 1

            if next_game_int == 1 and away_team in home_plus_one:
                if str(schedule_df.iloc[v_count, h_inc]) != "nan":
                    road_trip_list.append(schedule_df.iloc[v_count, h_inc])

                break

                # if away team is in either of the last two days
            elif next_game_int == 2 and (away_team in home_plus_one or away_team in home_plus_two):
                if str(schedule_df.iloc[v_count, h_inc]) != "nan":
                    road_trip_list.append(schedule_df.iloc[v_count, h_inc])

                break
            elif next_game_int == 3 and (away_team in home_plus_one or away_team in home_plus_two or away_team in home_plus_three):
                if str(schedule_df.iloc[v_count, h_inc]) != "nan":
                    road_trip_list.append(schedule_df.iloc[v_count, h_inc])

                break

            # don't want to append null values...
            if str(schedule_df.iloc[v_count, h_inc]) != "nan":
                road_trip_list.append(schedule_df.iloc[v_count, h_inc])

            if str(list(schedule_df.iloc[v_count, h_inc+1:h_inc + 5])) == "[nan, nan, nan, nan]":

                break

        h_inc += 1

    return road_trip_list


vertical_count = 0
horizontal_count = 0
final_output = []
final_output.append(["day", "away_team", "road_trip_list", "road_trip_distance"])
road_trip_list = []

while horizontal_count < len(schedule_df.columns):

    while vertical_count < 30:
        # getting pass team labels

        schedule_day_minus_one = list(schedule_df.iloc[:,horizontal_count - 1])
        schedule_day_minus_one = [x for x in schedule_day_minus_one if str(x) != 'nan']
        schedule_day_minus_two = list(schedule_df.iloc[:, horizontal_count - 2])
        schedule_day_minus_two = [x for x in schedule_day_minus_two if str(x) != 'nan']
        schedule_day_minus_three = list(schedule_df.iloc[:, horizontal_count - 3])
        schedule_day_minus_three = [x for x in schedule_day_minus_three if str(x) != 'nan']
        schedule_day_minus_four = list(schedule_df.iloc[:, horizontal_count - 4])
        schedule_day_minus_four = [x for x in schedule_day_minus_four if str(x) != 'nan']

        if str(schedule_df.iloc[vertical_count, horizontal_count]) != "nan" and "@" in str(schedule_df.iloc[vertical_count, horizontal_count]):
            game_list = str(schedule_df.iloc[vertical_count, horizontal_count]).split("@")
            home_team = game_list[1]
            away_team = game_list[0]

            # if no away game in previous 4 days, then it's the beginning of a road trip according to our logic
            if str(list(schedule_df.iloc[vertical_count, horizontal_count - 4: horizontal_count])) == "[nan, nan, nan, nan]":
                individual_output_row = []
                road_trip_list = get_road_trip_may_10(schedule_df, vertical_count, horizontal_count)
                road_trip_distance, distance_list = calculate_road_trip(road_trip_list)
                game = schedule_df.iloc[vertical_count, horizontal_count]
                team_list = game.split("@")
                away_team = team_list[0]
                individual_output_row.append(horizontal_count)
                individual_output_row.append(away_team)
                individual_output_row.append(road_trip_list)
                individual_output_row.append(road_trip_distance)
                individual_output_row.append(distance_list)
                final_output.append(individual_output_row)

                pass

            else:
                # if there's a home game in between
                schedule_day_minus_one = list(schedule_df.iloc[:, horizontal_count - 1])
                schedule_day_minus_one = [x for x in schedule_day_minus_one if str(x) != 'nan']
                schedule_day_minus_two = list(schedule_df.iloc[:, horizontal_count - 2])
                schedule_day_minus_two = [x for x in schedule_day_minus_two if str(x) != 'nan']
                schedule_day_minus_three = list(schedule_df.iloc[:, horizontal_count - 3])
                schedule_day_minus_three = [x for x in schedule_day_minus_three if str(x) != 'nan']

                away_minus_one, home_minus_one = home_and_away_one_day(schedule_day_minus_one)
                away_minus_two, home_minus_two = home_and_away_one_day(schedule_day_minus_two)
                away_minus_three, home_minus_three = home_and_away_one_day(schedule_day_minus_three)

                # quick loop to find index of previous game
                prev_game_int = 0
                # have to reverse list so it considers the previous day in the first index
                prev_four_days = list(schedule_df.iloc[vertical_count, horizontal_count - 4: horizontal_count])
                prev_four_days.reverse()
                for day in prev_four_days:

                    if str(day) != "nan" and "@" in str(day):
                        break

                    prev_game_int += 1
                # custom logic for first few days of the season
                if horizontal_count == 1:
                    individual_output_row = []
                    road_trip_list = get_road_trip_may_10(schedule_df, vertical_count, horizontal_count)
                    road_trip_distance, distance_list = calculate_road_trip(road_trip_list)
                    game = schedule_df.iloc[vertical_count, horizontal_count]
                    team_list = game.split("@")
                    away_team = team_list[0]
                    individual_output_row.append(horizontal_count)
                    individual_output_row.append(away_team)
                    individual_output_row.append(road_trip_list)
                    individual_output_row.append(road_trip_distance)
                    individual_output_row.append(distance_list)
                    final_output.append(individual_output_row)

                elif horizontal_count == 2 and str(schedule_df.iloc[vertical_count, horizontal_count - 1]) == "nan":
                    individual_output_row = []
                    road_trip_list = get_road_trip_may_10(schedule_df, vertical_count, horizontal_count)
                    road_trip_distance, distance_list = calculate_road_trip(road_trip_list)
                    game = schedule_df.iloc[vertical_count, horizontal_count]
                    team_list = game.split("@")
                    away_team = team_list[0]
                    individual_output_row.append(horizontal_count)
                    individual_output_row.append(away_team)
                    individual_output_row.append(road_trip_list)
                    individual_output_row.append(road_trip_distance)
                    individual_output_row.append(distance_list)
                    final_output.append(individual_output_row)

                    # third day. either first two days must be no away or day 1 is away and day 2 is home
                elif (horizontal_count == 3 and str(list(schedule_df.iloc[vertical_count, horizontal_count - 2: horizontal_count])) == "[nan, nan]") or \
                        (horizontal_count == 3 and str(schedule_df.iloc[vertical_count, horizontal_count - 2]) != "nan" and away_team in home_minus_one):

                    individual_output_row = []
                    road_trip_list = get_road_trip_may_10(schedule_df, vertical_count, horizontal_count)
                    road_trip_distance, distance_list = calculate_road_trip(road_trip_list)
                    game = schedule_df.iloc[vertical_count, horizontal_count]
                    team_list = game.split("@")
                    away_team = team_list[0]
                    individual_output_row.append(horizontal_count)
                    individual_output_row.append(away_team)
                    individual_output_row.append(road_trip_list)
                    individual_output_row.append(road_trip_distance)
                    individual_output_row.append(distance_list)
                    final_output.append(individual_output_row)

                elif (horizontal_count == 4 and str(list(schedule_df.iloc[vertical_count, horizontal_count - 3: horizontal_count])) == "[nan, nan, nan]") or \
                        (horizontal_count == 4 and str(schedule_df.iloc[vertical_count, horizontal_count - 2]) != "nan" and away_team in home_minus_one) or \
                        (horizontal_count == 4 and str(schedule_df.iloc[vertical_count, horizontal_count - 3]) != "nan" and (away_team in home_minus_one or away_team in home_minus_two)):
                    individual_output_row = []
                    road_trip_list = get_road_trip_may_10(schedule_df, vertical_count, horizontal_count)
                    road_trip_distance, distance_list = calculate_road_trip(road_trip_list)
                    game = schedule_df.iloc[vertical_count, horizontal_count]
                    team_list = game.split("@")
                    away_team = team_list[0]
                    individual_output_row.append(horizontal_count)
                    individual_output_row.append(away_team)
                    individual_output_row.append(road_trip_list)
                    individual_output_row.append(road_trip_distance)
                    individual_output_row.append(distance_list)
                    final_output.append(individual_output_row)

                # if the previous day was an away game, this is definitely not the start of a trip
                elif prev_game_int == 0:
                    pass
                elif prev_game_int == 1 and away_team in home_minus_one:
                    individual_output_row = []
                    road_trip_list = get_road_trip_may_10(schedule_df, vertical_count, horizontal_count)
                    road_trip_distance, distance_list = calculate_road_trip(road_trip_list)
                    game = schedule_df.iloc[vertical_count, horizontal_count]
                    team_list = game.split("@")
                    away_team = team_list[0]
                    individual_output_row.append(horizontal_count)
                    individual_output_row.append(away_team)
                    individual_output_row.append(road_trip_list)
                    individual_output_row.append(road_trip_distance)
                    final_output.append(individual_output_row)
                    individual_output_row.append(distance_list)

                    # if away team is in either of the last two days
                elif prev_game_int == 2 and (away_team in home_minus_one or away_team in home_minus_two):
                    individual_output_row = []
                    road_trip_list = get_road_trip_may_10(schedule_df, vertical_count, horizontal_count)
                    road_trip_distance, distance_list = calculate_road_trip(road_trip_list)
                    game = schedule_df.iloc[vertical_count, horizontal_count]
                    team_list = game.split("@")
                    away_team = team_list[0]
                    individual_output_row.append(horizontal_count)
                    individual_output_row.append(away_team)
                    individual_output_row.append(road_trip_list)
                    individual_output_row.append(road_trip_distance)
                    individual_output_row.append(distance_list)
                    final_output.append(individual_output_row)

                elif prev_game_int == 3 and (away_team in home_minus_one or away_team in home_minus_two or away_team in home_minus_three):
                    individual_output_row = []
                    road_trip_list = get_road_trip_may_10(schedule_df, vertical_count, horizontal_count)
                    road_trip_distance, distance_list = calculate_road_trip(road_trip_list)
                    game = schedule_df.iloc[vertical_count, horizontal_count]
                    team_list = game.split("@")
                    away_team = team_list[0]
                    individual_output_row.append(horizontal_count)
                    individual_output_row.append(away_team)
                    individual_output_row.append(road_trip_list)
                    individual_output_row.append(road_trip_distance)
                    individual_output_row.append(distance_list)
                    final_output.append(individual_output_row)

        away_minus_one, home_minus_one = home_and_away_one_day(schedule_day_minus_one)

        vertical_count += 1

    vertical_count = 0
    horizontal_count += 1

with open(output_file_path, "w", newline = '') as csv_output:
    wr = csv.writer(csv_output)

    wr.writerows(final_output)


