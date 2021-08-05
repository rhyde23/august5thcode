#Reggie Hyde

#Libraries
import pygame, pickle, random, itertools, time
from os import listdir

#Imports of other functions I will need from the project
from file_path_converter import convert_path
from schedule import get_schedule
from schedule import get_games_in_a_month
from months_in_order import get_month_number
from months_in_order import get_days_in_a_month
from months_in_order import get_number_month
from team_rating_calculator import calculate_rating
from match_sim_calculator import  match_sim
from goals_randomizer import randomize_goals
from randomize_realistic_minutes import randomize_goals_minutes
from formation_coords import get_coords
from starting_team_formations import get_positions_from_formation
from outside_positions_converter import convert_outside_position_to_center


def game(save_number) :

    #The "pi" variable just represents whether or not the script is running on Linux
    pi = True

    #Initialize pygame and pygame fonts
    pygame.init()
    pygame.font.init()

    #Define fonts
    myfont = pygame.font.SysFont('Currier', 25)
    myfont2 = pygame.font.SysFont('Currier', 50)
    myfont3 = pygame.font.SysFont('Currier', 15)
    myfont4 = pygame.font.SysFont('Currier', 20)
    myfont5 = pygame.font.SysFont('Currier', 30)
    myfont6 = pygame.font.SysFont('Currier', 35)

    #Display width
    display_width = 792
    half = int(display_width/2)

    #Set up display
    display = pygame.display.set_mode((display_width, 612))
    pygame.display.set_caption('Project')

    #Define RGB Color Codes
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    green = (0, 150, 0)
    blue = (0, 0, 255)
    key_color = (58, 166, 221)
    gray = (200, 200, 200, 128)
    light_blue = (58, 166, 221, 255)
    cyan = (0, 255, 255)

    #The "teams_in_league" array contains all of the teams in alphabetical order
    teams_in_league = [
        'Arsenal',
        'Aston Villa',
        'Brighton & Hove Albion',
        'Burnley',
        'Chelsea',
        'Crystal Palace',
        'Everton',
        'Fulham',
        'Leeds United',
        'Leicester City',
        'Liverpool',
        'Manchester City',
        'Manchester United',
        'Newcastle United',
        'Sheffield United',
        'Southampton',
        'Tottenham Hotspur',
        'West Bromwich Albion',
        'West Ham United',
        'Wolverhampton Wanderers'
    ]

    #######################################################################################################################################

    #Calendar Screen

    #######################################################################################################################################

    #Temporary Save Stuff
    
    #Load the save data that the user selected, use the singular argument passed in called "save_number"
    file_path = ''.join(['C:\\Users\\rhyde23\\Desktop\\SoccerManager\\Saves', '\\File', str(save_number), '.dat'])
    if pi :
        file_path = convert_path(file_path)
    current_data = pickle.load(open(file_path, 'rb'))

    #Function to overwrite the save file with the current data from the current session
    def save_progress() :
        output_file = open(file_path, 'wb')
        pickle.dump(current_data, output_file)

    #Load the UI for the team and the manager name in the top left
    mr_manager_team, mr_manager_name = myfont.render(current_data['TeamName'], True, white), myfont3.render(current_data['ManagerName'], True, white)
    
    #The "red_cover" pygame surface is used to represent what day it is in the calendar. It is a transparent red rectangle that covers the current date on the calendar
    red_cover = pygame.Surface((71,71)) 
    red_cover.set_alpha(128)           
    red_cover.fill((255,0,0))          

    #The "coords_of_days" dictionary was produced by the commented-out loop at the bottom of the script. Each day on the calendar corresponds to a coordinate where the "red_cover" surface is drawn.
    coords_of_days = {
        '1': (55, 190),
        '2': (127, 190),
        '3': (199, 190),
        '4': (271, 190),
        '5': (343, 190),
        '6': (415, 190),
        '7': (487, 190),
        '8': (56, 262),
        '9': (128, 262),
        '10': (200, 262),
        '11': (272, 262),
        '12': (344, 262),
        '13': (416, 262),
        '14': (487, 262),
        '15': (56, 335),
        '16': (128, 335),
        '17': (200, 335),
        '18': (272, 335),
        '19': (344, 335),
        '20': (416, 335),
        '21': (487, 335),
        '22': (56, 407),
        '23': (128, 407),
        '24': (200, 407),
        '25': (272, 407),
        '26': (344, 407),
        '27': (416, 407),
        '28': (487, 407),
        '29': (56, 479),
        '30': (128, 479),
        '31': (200, 479)
    }

    #The "unpack_date" function splits up date strings into the month, day, and year
    def unpack_date(date) :
        splitted = date.split(' ') 
        return [splitted[0], int(splitted[1]), int(splitted[2])]

    #The "build_date" function is essentially the opposite of "unpack_date". It takes the month, day, and year and builds date strings
    def build_date(month, day, year) :
        return ' '.join([month, str(day), str(year)])

    #The "advance_one_day" function builds the date string one day in the future for the sim
    def advance_one_day(date) :
        month, day, year = unpack_date(date)
        month_number = get_month_number(month)
        change_screen = False
        if day == get_days_in_a_month(month) :
            if month == 'December' :
                month, day, year = 'January', 1, year+1
            else :
                month, day, year = get_number_month(month_number+1), 1, year
            change_screen = True
        else :
            month, day, year = month, day+1, year
        return build_date(month, day, year), change_screen

    #The "get_coords_of_logo_and_text" function renders the logo and the the team for the match sim screen
    def get_coords_of_logo_and_text(team, left_or_right) :
        x_difference = 35
        logo = team_simming_logos[team]
        logo_text = myfont.render(team, True, white)
        logo_text_width = logo_text.get_width()
        
        score_factor = 50
        
        if left_or_right == 0 :
            logo_full_width = sum([logo_text_width, 70, x_difference])
            logo_x = int(((half-score_factor)-logo_full_width)/2)
            logo_text_x = sum([logo_x, 40, x_difference])
        else :
            logo_full_width = sum([logo_text_width, 70])
            logo_text_x = (half+score_factor)+(int((display_width-(half+score_factor))-logo_full_width)/2)
            logo_x = sum([logo_text_x, logo_text_width])
        return logo, logo_text, logo_x, logo_text_x, 30, 57

    #The "mouse_over_button" function returns whether or not the mouse is hovering over a rectangle
    def mouse_over_button(pos, x, y, width, height) :
        return pos[0] >= x and pos[0] <= x+width and pos[1] >= y and pos[1] <= y+height

    #The "display_button" function displays a button from the buttons array and returns whether or not the mouse is hovering over it 
    def display_button(button, pos) :
        x, y, width, height = button[0], button[1], button[2], button[3]
        over_button = mouse_over_button(pos, x, y, width, height)
        if over_button :
            color = button[5]
            text = button[7]
        else :
            color = button[4]
            text = button[6]
        text_width, text_height = button[-2], button[-1]
        text_x, text_y = x+int((width-text_width)/2), y+int((height-text_height)/2)
        pygame.draw.rect(display, color, pygame.Rect(x, y, width, height))
        display.blit(text, (text_x, text_y))
        return over_button

    #The "display_score" function displays the current score of the game
    def display_score(left_score, right_score) :
        off = 30
        y = 47
        left_score_width = score_texts_width[left_score]
        display.blit(score_texts[left_score], (half-off-left_score_width, y))
        display.blit(score_texts[right_score], (half+off, y))
    
    #The "get_scorers_text_and_coords" updates the two arrays that display the scorer text in the match sim 
    def get_scorers_text_and_coords(scorers, text_x) :
        scorers_texts, scorers_texts_coordinates, already_done = [], [], []
        current_text_y = 130
        for scorer in scorers :
            if not scorer in already_done : 
                scorers_texts.append(myfont.render(scorer, True, white))
                scorers_texts_coordinates.append((text_x, current_text_y))
                already_done.append(scorer)
                current_text_y += 50
        return scorers_texts, scorers_texts_coordinates
        
    #The "standings_goal_differential" function makes sure the standings respect goal differential order
    def standings_goal_differential() :
        current_gd, current_gd_indexes = [], []
        for i, team_sio in enumerate(current_data['CurrentStandingsInOrder']) :
            if current_gd != [] :
                if current_data['CurrentStandings'][team_sio] == current_data['CurrentStandings'][current_gd[0]] :
                    current_gd.append(team_sio)
                    current_gd_indexes.append(i)
                else :
                    if len(current_gd) > 1 :
                        sorted_by_gd = sorted(current_gd, key=lambda x:current_data['StandingsData'][x][6], reverse=True)
                        for x, sorted_correct in enumerate(sorted_by_gd) :
                            current_data['CurrentStandingsInOrder'][current_gd_indexes[x]] = sorted_by_gd[x]
                    current_gd, current_gd_indexes = [team_sio], [i]
            else :
                current_gd.append(team_sio)
                current_gd_indexes.append(i)
        if len(current_gd) > 1 :
            sorted_by_gd = sorted(current_gd, key=lambda x:current_data['StandingsData'][x][6], reverse=True)
            for x, sorted_correct in enumerate(sorted_by_gd) :
                current_data['CurrentStandingsInOrder'][current_gd_indexes[x]] = sorted_by_gd[x]
    
    #The "put_standings_in_correct_order" function sorts the standings by points and then goal differential using "standings_goal_differential"   
    def put_standings_in_correct_order() :
        standings_dictionary = current_data['CurrentStandings']
        current_data['CurrentStandingsInOrder'] = sorted(standings_dictionary, key=lambda x:standings_dictionary[x], reverse=True)
        standings_goal_differential()
        
    #The "update_top_scorers" function updates the top scorers list
    def update_top_scorers(user_scorers, user_team, opponent_scorers, opponent_team) :
        top_scorers_dict, top_scorers_in_order = current_data['TopScorers'], current_data['TopScorersInOrder']
        max_top_scorers = 3
        top_scorers_added = 0
        for new_top_scorer in user_scorers :
            if not new_top_scorer in top_scorers_dict :
                top_scorers_dict[new_top_scorer] = current_data[user_team+'_Players'][new_top_scorer]['Goals']
                top_scorers_added += 1
        
        for new_top_scorer in opponent_scorers :
            if not new_top_scorer in top_scorers_dict :
                top_scorers_dict[new_top_scorer] = current_data[opponent_team+'_Players'][new_top_scorer]['Goals']
                top_scorers_added += 1
        
        new_dict = sorted(top_scorers_dict, key=lambda x:top_scorers_dict[x], reverse=True)
        if len(new_dict) >= max_top_scorers :
            new_dict = new_dict[:max_top_scorers]
        
        current_data['TopScorers'], current_data['TopScorersInOrder'] = {key:top_scorers_dict[key] for key in new_dict}, new_dict

    #The "update_standings_info" function updates all of the stats from a game with the user
    def update_standings_info(team1, team2, winner, team_one_score, team_two_score) :
        current_data['StandingsData'][team1][0] += 1
        current_data['StandingsData'][team2][0] += 1
        current_data['StandingsData'][team1][4] += team_one_score
        current_data['StandingsData'][team2][4] += team_two_score
        current_data['StandingsData'][team1][5] += team_two_score
        current_data['StandingsData'][team2][5] += team_one_score
        current_data['StandingsData'][team1][6] += (team_one_score-team_two_score)
        current_data['StandingsData'][team2][6] += (team_two_score-team_one_score)
        if winner == 'Draw' :
            current_data['StandingsData'][team1][2] += 1
            current_data['StandingsData'][team2][2] += 1
        else :
            if team1 == winner :
                current_data['StandingsData'][team1][1] += 1
                current_data['StandingsData'][team2][3] += 1
            else :
                current_data['StandingsData'][team2][1] += 1
                current_data['StandingsData'][team1][3] += 1
        
    #The "sim_other_games" function sims the other games on any given gameday
    def sim_other_games(without_year, games_in_current_month) :
        if without_year in games_in_current_month :
            games_in_day = games_in_current_month[without_year]
            for other_game in games_in_day :
                team1, team2 = other_game
                if team1 != team and team2 != team :
                    team1_players, team1_lineup, team1_formation, team2_players, team2_lineup, team2_formation = current_data[team1+'_Players'], current_data[team1+'_Lineup'], current_data[team1+'_Formation'], current_data[team2+'_Players'], current_data[team2+'_Lineup'], current_data[team2+'_Formation']
                    team1_rating = calculate_rating(team1_players, team1_lineup, team1_formation)
                    team2_rating = calculate_rating(team2_players, team2_lineup, team2_formation)
                    winner, score_difference = match_sim(team1_rating, team2_rating, team1, team2)
                    score, team1_scorers, team2_scorers = randomize_goals(team1_players, team2_players, team1_lineup, team2_lineup, team1, team2, team1_formation, team2_formation, winner, score_difference)
                    s_one, s_two = score.split('-')
                    final_team1_score, final_team2_score = int(s_one), int(s_two)
                    for nop in team1_scorers :
                        current_data[team1+'_Players'][nop]['Goals'] += 1
                        if nop in current_data['TopScorersInOrder'] :
                            current_data['TopScorers'][nop] += 1
                        
                    for nop in team2_scorers :
                        current_data[team2+'_Players'][nop]['Goals'] += 1
                        if nop in current_data['TopScorersInOrder'] :
                            current_data['TopScorers'][nop] += 1
                    
                    if winner == 'Draw' :
                        current_data['CurrentStandings'][team1] += 1
                        current_data['CurrentStandings'][team2] += 1
                    else :
                        current_data['CurrentStandings'][winner] += 3
                        current_data['StandingsData'][winner]
                    
                    put_standings_in_correct_order()
                    update_top_scorers(team1_scorers, team1, team2_scorers, team2)
                    update_standings_info(team1, team2, winner, final_team1_score, final_team2_score)

    #The "calendar_screens" array is going to be filled with every calendar month screen in order
    calendar_screens = []

    #This loop fills "calendar_screens" with every calendar month screen in order
    for i in range(12) :
        path = 'C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Month-'+str(i+1)+'.png'
        if pi :
            path = convert_path(path)
        calendar_screens.append(pygame.image.load(path).convert())

    #Get values from the save, which is fake right now
    team = current_data['TeamName']
    current_date = current_data['CurrentDate']
    month, day, year = unpack_date(current_date)
    month_number = get_month_number(month)

    #Get the current calendar month screen
    current_calendar_screen = calendar_screens[month_number]

    #The "team_logos" and "team_simming_logos" dictionaries contain the team logos on the calendar and the team logos during the sim
    team_logos = {}
    team_simming_logos = {}
    mini_team_logos = {}

    #Load up "team_logos" and "team_simming_logos" with the pygame surfaces
    for t in teams_in_league :
        path = 'C:\\Users\\rhyde23\\Desktop\\Project\\Images\\'+t+'.png'
        if pi :
            path = convert_path(path)
        loaded_image_logo = pygame.image.load(path).convert_alpha()
        team_logos[t] = pygame.transform.scale(loaded_image_logo, (40, 40))
        team_simming_logos[t] = pygame.transform.scale(loaded_image_logo, (70, 70))
        mini_team_logos[t] = pygame.transform.scale(loaded_image_logo, (18, 18))

    #The "schedule_dict" dictionary contains all of the matchdays and every game in the matchday
    schedule_dict = get_schedule()

    #The "games_in_current_month" dictionary contains every game taking place in this month
    games_in_current_month = {date:schedule_dict[date] for date in schedule_dict if date.split(' ')[0] == month}

    #The "dates_of_games_in_month" dictionary contains all of the dates of the games in the current month that the user is playing in 
    dates_of_games_in_month = get_games_in_a_month(month, schedule_dict, team)

    #These two rendered texts are for the upcoming games on the calendar
    GAME_text = myfont3.render("GAME", True, white)
    GAMEVS_text = myfont3.render("VS", True, white)

    #The "calendar_buttons" array contains all of the buttons that will be run through the "display_button" function
    calendar_buttons = [
        [300, 120, 100, 30, white, red, myfont3.render("START SIM", True, red), myfont3.render("START SIM", True, white)],
        [300, 120, 100, 30, red, white, myfont3.render("END SIM", True, white), myfont3.render("END SIM", True, red)],
        [300, 120, 100, 30, white, red, myfont3.render("PLAY MATCH", True, red), myfont3.render("PLAY MATCH", True, white)],
    ]

    #This loop adds the width and height of the text into each button in the "calendar_buttons" array
    for i, calendar_button in enumerate(calendar_buttons) :
        calendar_buttons[i] = calendar_buttons[i] + [calendar_button[-2].get_width(), calendar_button[-2].get_height()]

    #Loading the match sim background for when the user is in "match_simming"
    match_sim_background_path = 'C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Match Sim.png'
    if pi :
        match_sim_background_path = convert_path(match_sim_background_path)
    match_sim_background = pygame.image.load(match_sim_background_path).convert()

    #The "score_texts" array contains all of the rendered texts of the scoreboard for the Match Simming screen
    score_texts = [
        myfont2.render("0", True, white),
        myfont2.render("1", True, white),
        myfont2.render("2", True, white),
        myfont2.render("3", True, white),
        myfont2.render("4", True, white),
        myfont2.render("5", True, white),
        myfont2.render("6", True, white),
        myfont2.render("7", True, white),
        myfont2.render("8", True, white),
        myfont2.render("9", True, white),
    ]

    #The "score_texts_width" array contains all of the widths of the rendered scoreboard texts
    score_texts_width = [t.get_width() for t in score_texts]

    #These two arrays are the buttons for the match simming screen
    start_simming_button = [300, 575, 100, 30, white, red, myfont3.render("START MATCH", True, red), myfont3.render("START MATCH", True, white)]
    start_simming_button = start_simming_button + [start_simming_button[-2].get_width(), start_simming_button[-2].get_height()]
    start_simming_button[0] = half-int(start_simming_button[2]/2)
    return_simming_button = [300, 575, 100, 30, red, white, myfont3.render("RETURN TO MENU", True, white), myfont3.render("RETURN TO MENU", True, red)]
    return_simming_button = return_simming_button + [return_simming_button[-2].get_width(), return_simming_button[-2].get_height()]
    return_simming_button[0] = half-int(return_simming_button[2]/2)

    #The "simming_minute_texts" array contains all of the rendered texts for every minute of the game
    simming_minute_texts = [myfont.render(str(minute)+'\'', True, white) for minute in range(1, 91)]
    simming_minute_texts_widths = [simming_minute_text.get_width() for simming_minute_text in simming_minute_texts]
    simming_minute_texts_x = [half-int(simming_minute_text_width/2) for simming_minute_text_width in simming_minute_texts_widths]

    #The "simming_scoring_minutes_texts" array contains all of the rendered texts for every minute of the game for the scorers
    simming_scoring_minutes_texts = [myfont.render(str(minute)+'\'', True, white) for minute in range(1, 91)]

    #Render a comma
    comma_text = myfont.render(',', True, white)

    #The "return_available" variable whether or not we should display the Return to Calendar Screen button
    return_available = False

    #These two variables tell us if the user is hovering over the Start Match button and the Return to Menu button, respectively
    over_button1 = False
    over_button2 = False

    #The "calendar_calendar_button_index" integer picks the correct button from "calendar_buttons"
    calendar_button_index = 0

    #The "over_sim_button" variable tells us whether or not the user is hovering over the Start Simulation button
    over_sim_button = False

    #The "simming" variable tells us whether or not we are currently simming
    simming = False

    #The "stopped_on_matchday" variable tells us whether or not the next simming action will be to play the match
    stopped_on_matchday = False

    #The "simming_count" adds one every frame. When it gets to 50, one day is progressed
    simming_count = 0

    #The "match_simming" variable almost acts as a whole loop, but it is under "calendar"
    match_simming = False

    #######################################################################################################################################

    #Standings Screen

    #######################################################################################################################################


    standings_background_path = 'C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Standings Background.png'
    if pi :
        standings_background_path = convert_path(standings_background_path)
        
    standings_background = pygame.image.load(standings_background_path).convert()

    header_strings = ['GP', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts']
    header_texts = [myfont3.render(header_string, True, white) for header_string in header_strings]
    header_texts_width = [header_text.get_width() for header_text in header_texts]
    header_texts_x = []
    last_header_text_width = 0
    last_header_text_x = 235
            
    for i, header_text in enumerate(header_texts) :
        header_x_coord = last_header_text_x+last_header_text_width+20
        header_texts_x.append(header_x_coord)
        last_header_text_width = header_texts_width[i]
        last_header_text_x = header_x_coord

    standings_team_texts = {standings_team_text:myfont4.render(standings_team_text, True, white) for standings_team_text in teams_in_league}

    small_text_numbers = {i:myfont4.render(str(i), True, white) for i in range(-500, 500)}
    small_text_numbers_widths = {key:small_text_numbers[key].get_width() for key in small_text_numbers}

    def display_standings_headers() :
        for i, header_text in enumerate(header_texts) :
            display.blit(header_text, (header_texts_x[i], 125))

    def display_standings_data() :
        for i, team_in_order in enumerate(current_data['CurrentStandingsInOrder']) :
            y = (i*22)+140
            display.blit(standings_team_texts[team_in_order], (60, y))
            display.blit(mini_team_logos[team_in_order], (40, y))
            for enum, stat in enumerate(current_data['StandingsData'][team_in_order]) :
                small_stat_width = small_text_numbers_widths[stat]
                small_stat_x = header_texts_x[enum]+int((header_texts_width[enum]-small_stat_width)/2)
                if enum != 7 :
                    display.blit(small_text_numbers[stat], (small_stat_x, y+2))
                else :
                    display.blit(small_text_numbers[current_data['CurrentStandings'][team_in_order]], (small_stat_x, y+2))
        
    #######################################################################################################################################

    #Lineups Screen
    
    #######################################################################################################################################

    def get_position_rating(dictionary, x, position) :
        try :
            return dictionary[x]['Positions'][position]
        except :
            return '0'

    def get_best_players_in_given_position(team_viewing, position) :
        team_players_dict = current_data[team_viewing+'_Players']
        return sorted(team_players_dict, key=lambda x: get_position_rating(team_players_dict, x, position), reverse=True)

    all_formations = [
        '4-2-3-1 (Wide)',
        '5-3-2 (Attacking)',
        '4-4-2 (Flat)',
        '5-2-3 (Flat)',
        '4-3-3 (Defensive)',
        '4-5-1 (Defensive)',
        '4-3-3 (False 9)',
        '5-3-2 (Flat)',
        '4-3-3 (Flat)',
        '4-3-3 (Attacking)',
        '4-2-3-1 (Narrow)',
        '4-1-2-1-2 (Narrow)',
    ]

    def build_lineup_background_path(formation) :
        lineup_background_path = 'C:\\Users\\rhyde23\\Desktop\\Project\\Images\\'+formation+'.png'
        if pi :
            return convert_path(lineup_background_path)
        return lineup_background_path

    lineup_backgrounds = {lineup_bg_formation:pygame.image.load(build_lineup_background_path(lineup_bg_formation)).convert() for lineup_bg_formation in all_formations}

    user_players = current_data[team+'_Players']
    player_name_texts = {}
    player_name_texts_widths = {}
    for user_player_key in user_players :
        text = myfont3.render(user_player_key, True, white)
        player_name_texts[user_player_key] = text
        player_name_texts_widths[user_player_key] = text.get_width()

    def calculate_rgb_for_rating(x) :
        #40 is lowest, 100 is highest
        if x == 70 :
            return (255, 255, 0)
        lowest_rating, highest_rating = 40, 100
        red, green = 255, 255
        rgb_factor = int(255/int((highest_rating-lowest_rating)/2))
        deviant_value = abs(x-70)
        if x > 70 :
            red -= rgb_factor*deviant_value
            if red < 0 :
                red = 0
        else :
            green -= rgb_factor*deviant_value
            if green < 0 :
                green = 0
        return (red, green, 0)

    ratings_rgb = {r:calculate_rgb_for_rating(r) for r in range(40, 100)}
        
    rating_texts_black = {}
    rating_texts_colored = {}
    for r in range(40, 100) :
        rating_texts_black[str(r)] = myfont5.render(str(r), True, black)
        rating_texts_colored[str(r)] = myfont.render(str(r), True, ratings_rgb[r])

    rating_text = myfont3.render('Rating:', True, gray)
    rating_text_width = rating_text.get_width()

    rating_text_width = 46

    ratings_lost_texts = {rlt:myfont4.render('-'+str(rlt), True, red) for rlt in range(1, 100)}
    ratings_lost_texts[0] = myfont4.render('', True, red)
    for rlt_negative in range(1, 10) : 
        ratings_lost_texts[-rlt_negative] = myfont4.render(''+str(rlt_negative), True, red)

    def get_correct_name_coordinates(jersey_coordinates, text_width) :
        return (jersey_coordinates[0]+(int((72-text_width)/2)), jersey_coordinates[1]-22)

    def get_correct_rating_coordinates(jersey_coordinates) :
        return (jersey_coordinates[0]+(int((72-rating_text_width)/2)), jersey_coordinates[1]-10)

    jersey_coords = get_coords(current_data['CurrentFormation'])


    
    possible_player_data_values = {
        'Team':teams_in_league,
        'Rating': ['53', '54', '55', '56', '57', '58', '59', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '90', '91'], 
        'Position': ['CAM', 'CB', 'CDM', 'CF', 'CM', 'GK', 'LB', 'LM', 'LW', 'LWB', 'RB', 'RM', 'RW', 'RWB', 'ST'],
        'Age': ['17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39'],
        'Nation': ['Algeria', 'Argentina', 'Australia', 'Austria', 'Belgium', 'Bosnia & Herzegovina', 'Brazil', 'Burkina Faso', 'Cameroon', 'Canada', 'China PR', 'Colombia', 'Croatia', 'Czech Republic', 'DR Congo', 'Denmark', 'Ecuador', 'Egypt', 'England', 'Estonia', 'France', 'Gabon', 'Germany', 'Ghana', 'Greece', 'Guinea', 'Iceland', 'Iran', 'Italy', 'Ivory Coast', 'Jamaica', 'Japan', 'Korea Republic', 'Mali', 'Mexico', 'Morocco', 'Netherlands', 'New Zealand', 'Nigeria', 'North Macedonia', 'Northern Ireland', 'Norway', 'Paraguay', 'Peru', 'Poland', 'Portugal', 'Republic of Ireland', 'Romania', 'Scotland', 'Senegal', 'Serbia', 'Slovakia', 'South Africa', 'Spain', 'St Kitts Nevis', 'Sweden', 'Switzerland', 'Thailand', 'Turkey', 'Ukraine', 'United States', 'Uruguay', 'Wales', 'Zimbabwe'], 
        'Height': ['5\'10"', '5\'11"', '5\'4"', '5\'5"', '5\'6"', '5\'7"', '5\'8"', '5\'9"', '6\'0"', '6\'1"', '6\'2"', '6\'3"', '6\'4"', '6\'5"', '6\'6"', '6\'7"'], 
        'Weight': ['123 lbs', '128 lbs', '130 lbs', '132 lbs', '134 lbs', '137 lbs', '139 lbs', '141 lbs', '143 lbs', '146 lbs', '148 lbs', '150 lbs', '152 lbs', '154 lbs', '157 lbs', '159 lbs', '161 lbs', '163 lbs', '165 lbs', '168 lbs', '170 lbs', '172 lbs', '174 lbs', '176 lbs', '179 lbs', '181 lbs', '183 lbs', '185 lbs', '187 lbs', '190 lbs', '192 lbs', '194 lbs', '196 lbs', '198 lbs', '201 lbs', '203 lbs', '205 lbs', '207 lbs', '209 lbs', '212 lbs', '214 lbs', '220 lbs'],
        'Freshness': [0.5],
        'Goals': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50], 'Assists': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60],
}


    all_positions_in_order = {f:get_positions_from_formation(f) for f in all_formations}

    all_possible_positions = []
    for form in all_positions_in_order :
        all_possible_positions = all_possible_positions + all_positions_in_order[form]
    all_possible_positions = list(set(all_possible_positions))
    positions_texts = {position_string:myfont4.render(position_string, True, black) for position_string in all_possible_positions}
    positions_texts['SUB'] = myfont4.render('SUB', True, black)
    positions_texts_widths = {position_string:positions_texts[position_string].get_width() for position_string in positions_texts}


    p_positions_texts = {position_string:myfont.render(position_string, True, green) for position_string in possible_player_data_values['Position']}
    p_positions_texts_red = {position_string:myfont.render(position_string, True, red) for position_string in possible_player_data_values['Position']}
    p_positions_texts_widths = {position_string:p_positions_texts[position_string].get_width() for position_string in p_positions_texts}

    def find_position_text_x(coords, position) :
        return (coords[0]+int((72-positions_texts_widths[position])/2), coords[1]+35)

    def find_p_position_text_x(coords, position) :
        return (coords[0]+int((72-p_positions_texts_widths[position])/2), coords[1]+13)

    def display_players(player_name, player_rating, rating_coords, coords, position, p_position, ratings_lost=0) :
        display.blit(player_name_texts[player_name], get_correct_name_coordinates(coords, player_name_texts_widths[player_name]))
        display.blit(rating_text, rating_coords)
        display.blit(rating_texts_black[player_rating], (rating_coords[0]+rating_text_width-10, rating_coords[1]-1))
        display.blit(rating_texts_black[player_rating], (rating_coords[0]+rating_text_width-10, rating_coords[1]-1))
        display.blit(rating_texts_black[player_rating], (rating_coords[0]+rating_text_width-10, rating_coords[1]-4))
        display.blit(rating_texts_colored[player_rating], (rating_coords[0]+rating_text_width-8, rating_coords[1]-2))
        display.blit(ratings_lost_texts[ratings_lost], (rating_coords[0]+rating_text_width+15, rating_coords[1]-2))
        display.blit(positions_texts[position], find_position_text_x(coords, position))
        if ratings_lost > 0 :
            display.blit(p_positions_texts_red[p_position], find_p_position_text_x(coords, p_position))
        else :
            display.blit(p_positions_texts[p_position], find_p_position_text_x(coords, p_position))

    bench_coords = {
        0:(568, 181),
        1:(568, 291),
        2:(568, 401),
        3:(568, 511),
        4:(689, 181),
        5:(689, 291),
        6:(689, 401),
        7:(689, 511),
    }

    current_bench_page = 0
    current_bench_page_players = []

    def get_current_page_of_bench(current_bench_page) :
        total_players = len(current_data[team+'_Players'])-11
        str_max_page = str((total_players)/8)
        max_page_change = 0
        if str_max_page.split('.')[-1] == '0' :
            max_page_change = 1
        max_page = int(str_max_page[0])-max_page_change
        if current_bench_page > max_page :
            return None
        bench_players = sorted([p for p in current_data[team+'_Players'] if not p in current_data['CurrentLineup']], key=lambda x:current_data[team+'_Players'][x]['Rating'], reverse=True)
        s = current_bench_page*8
        if current_bench_page != max_page :
            e = (total_players-((current_bench_page+1)*8))
            if e != 0 :
                bench_players = bench_players[:-e]
        else :
            e = 0
        if s != 0 :
            bench_players = bench_players[s:]
        return bench_players

    current_bench_page_players = get_current_page_of_bench(current_bench_page)
    current_bench_page_text = myfont.render('Page Number: '+str(current_bench_page+1), True, white)
    current_bench_page_text_width = current_bench_page_text.get_width()
    current_bench_page_text_x = (625+((705-625)/2))-int((current_bench_page_text_width/2))

    currently_moving_key = None

    alpha_swapping_count = 150
    alpha_swapping_count_change = 5

    just_clicked_coords = None


    def display_starting_lineup() :
        positions_in_order = all_positions_in_order[current_data['CurrentFormation']]
        for position_index, position in enumerate(positions_in_order) :
            coords = jersey_coords[position]
            player_name = current_data['CurrentLineup'][position_index]
            player_rating = current_data[team+'_Players'][player_name]['Rating']
            player_position = current_data[team+'_Players'][player_name]['Position']
            rating_coords = get_correct_rating_coordinates(coords)
            #print(current_data[team+'_Players']['Ashley Westwood']['Positions'])
            #quit()
            display_players(player_name, player_rating, rating_coords, coords, position, player_position, ratings_lost=int(current_data[team+'_Players'][player_name]['Positions'][convert_outside_position_to_center(current_data[team+'_Players'][player_name]['Position'])]) - int(current_data[team+'_Players'][player_name]['Positions'][convert_outside_position_to_center(position)]))

    def display_bench_players() :
        for bench_index in range(len(current_bench_page_players)) :
            coords = bench_coords[bench_index]
            player_name = current_bench_page_players[bench_index]
            player_rating = current_data[team+'_Players'][player_name]['Rating']
            player_position = current_data[team+'_Players'][player_name]['Position']
            rating_coords = get_correct_rating_coordinates(coords)
            display_players(player_name, player_rating, rating_coords, coords, 'SUB', player_position)
            

    current_data['CurrentTeamRating'] = calculate_rating(current_data[team+'_Players'], current_data['CurrentLineup'], current_data['CurrentFormation'])
    current_team_rating_text = myfont6.render(str(current_data['CurrentTeamRating']), True, ratings_rgb[current_data['CurrentTeamRating']])

    hover_square, hover_square_coords, hover_square_position = False, (0, 0), ''

    def get_hover_square_coords(x, y, set_of_coordinates) :
        for pos_key in set_of_coordinates :
            pos_coordinates_x, pos_coordinates_y = set_of_coordinates[pos_key]
            if x >= pos_coordinates_x and x <= pos_coordinates_x+72 and y >= pos_coordinates_y and y <= pos_coordinates_y+72 :
                return True, (pos_coordinates_x, pos_coordinates_y), pos_key
        return False, (0, 0), ''

    alpha_lines_vertical = {}
    alpha_lines_horizontal = {}
    for alpha_level in range(1, 151) :
        alpha_vertical = pygame.Surface((5,92)) 
        alpha_vertical.set_alpha(alpha_level)           
        alpha_vertical.fill((255,255,255))
        alpha_lines_vertical[alpha_level] = alpha_vertical
        alpha_horizontal = pygame.Surface((97,5)) 
        alpha_horizontal.set_alpha(alpha_level)           
        alpha_horizontal.fill((255,255,255))
        alpha_lines_horizontal[alpha_level] = alpha_horizontal

    def display_red_square(coordinates) :
        top_left = (coordinates[0]-10, coordinates[1]-28)
        top_right = (coordinates[0]+82, coordinates[1]-28)
        bottom_left = (coordinates[0]-10, coordinates[1]+64)
        bottom_right = (coordinates[0]+82, coordinates[1]+64)
        pygame.draw.line(display, red, (top_left), (top_right), (5))
        pygame.draw.line(display, red, (top_left), (bottom_left), (5))
        pygame.draw.line(display, red, (bottom_left), (bottom_right), (5))
        pygame.draw.line(display, red, (bottom_right), (top_right), (5))

    def display_hover_square(hover_boolean, hover_coordinates, currently_moving_key, alpha_swapping_count, just_clicked_coords, jersey_coords={}) :
        if jersey_coords != {} :
            if currently_moving_key != None :
                for set_of_coords in [jersey_coords[jer_key] for jer_key in jersey_coords]+[bench_coords[jer_key] for jer_key in bench_coords] :
                    top_left = (set_of_coords[0]-12, set_of_coords[1]-30)
                    top_right = (set_of_coords[0]+80, set_of_coords[1]-30)
                    bottom_left = (set_of_coords[0]-12, set_of_coords[1]+62)
                    bottom_right = (set_of_coords[0]+80, set_of_coords[1]+66)
                    display.blit(alpha_lines_vertical[alpha_swapping_count], top_left)
                    display.blit(alpha_lines_vertical[alpha_swapping_count], top_right)
                    display.blit(alpha_lines_horizontal[alpha_swapping_count], bottom_left)
                    display.blit(alpha_lines_horizontal[alpha_swapping_count], top_left)
                display_red_square(just_clicked_coords)
        if hover_boolean :
            display_red_square(hover_coordinates)
        
        



    player_report_path = 'C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Player Report.png'
    if pi :
        player_report_path = convert_path(player_report_path)
    player_report_screen = pygame.image.load(player_report_path).convert()
    player_reporting = False

    player_reporting_coords = {
        'Rating':(603, 77),
        'Position':(149, 212),
        'Age':(330, 212),
        'Nation':(577, 212),
        'Height':(141, 300),
        'Weight':(318, 300),
        'Freshness':(570, 300),
        'Goals':(184, 410),
        'Assists':(530, 410),
        'Team':(400, 480),
        'Name':(60, 60)
    }

    player_reporting_offset_y = {
        'Rating':30,
        'Position':15,
        'Age':15,
        'Nation':15,
        'Height':15,
        'Weight':15,
        'Freshness':15,
        'Goals':20,
        'Assists':20,
        'Team':0,
        'Name':0
    }

    player_reporting_text_widths = {
        'Rating':70,
        'Position':25,
        'Age':30,
        'Nation':55,
        'Height':45,
        'Weight':45,
        'Freshness':70,
        'Goals':70,
        'Assists':90,
        'Team':0,
        'Name':0
    }

    player_reporting_fonts = {
        'Rating':myfont2,
        'Position':myfont2,
        'Age':myfont2,
        'Nation':myfont,
        'Height':myfont2,
        'Weight':myfont2,
        'Freshness':myfont2,
        'Goals':myfont2,
        'Assists':myfont2,
        'Team':myfont2,
        'Name':myfont2,
    }

    possible_player_data_texts = {key:{value:player_reporting_fonts[key].render(str(value), True, (255, 195, 116)) for value in possible_player_data_values[key]} for key in possible_player_data_values}
    possible_player_data_widths = {key:{value:possible_player_data_texts[key][value].get_width() for value in possible_player_data_values[key]} for key in possible_player_data_values}

    return_to_squads_button = [675, 550, 225, 30, white, red, myfont.render("RETURN TO LINEUP", True, red), myfont.render("RETURN TO LINEUP", True, white)]
    return_to_squads_button = return_to_squads_button + [return_to_squads_button[-2].get_width(), return_to_squads_button[-2].get_height()]
    return_to_squads_button[0] = half-int(return_to_squads_button[2]/2)

    def get_data_x(x_coord, text_width, header_width) :
        return x_coord+(int((header_width-text_width)/2))

    def display_player_data(player_selected_data, name_text) :
        for possible_key in player_selected_data :
            val = possible_player_data_texts[possible_key][player_selected_data[possible_key]]
            val_width = possible_player_data_widths[possible_key][player_selected_data[possible_key]]
            y_change = player_reporting_offset_y[possible_key]
            dis_x, dis_y = get_data_x(player_reporting_coords[possible_key][0], val_width, player_reporting_text_widths[possible_key]), player_reporting_coords[possible_key][1]+y_change
            display.blit(val, (dis_x, dis_y))
            if possible_key == 'Team' :
                display.blit(team_logos[team], (dis_x-40, dis_y))
                display.blit(team_logos[team], (dis_x+val_width, dis_y))
        display.blit(name_text, (player_reporting_coords['Name'][0], player_reporting_coords['Name'][1]))



    change_formation_button = [410, 140, 130, 30, white, red, myfont3.render("CHANGE FORMATION", True, red), myfont3.render("CHANGE FORMATION", True, white)]
    change_formation_button = change_formation_button + [change_formation_button[-2].get_width(), change_formation_button[-2].get_height()]

    last_page_button = [625, 130, 30, 20, white, red, myfont3.render("<<", True, red), myfont3.render("<<", True, white)]
    last_page_button = last_page_button + [last_page_button[-2].get_width(), last_page_button[-2].get_height()]

    next_page_button = [675, 130, 30, 20, white, red, myfont3.render(">>", True, red), myfont3.render(">>", True, white)]
    next_page_button = next_page_button + [next_page_button[-2].get_width(), next_page_button[-2].get_height()]

    changing_formation = False

    changing_formation_path = 'C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Formation Select.png'
    if pi :
        changing_formation_path = convert_path(changing_formation_path)
    changing_formation_screen = pygame.image.load(changing_formation_path).convert()

    changing_formation_coords = {
        '4-2-3-1 (Wide)':(37, 42),
        '5-3-2 (Attacking)':(221, 42),
        '4-4-2 (Flat)':(406, 42),
        '5-2-3 (Flat)':(590, 42),
        '4-3-3 (Defensive)':(37, 219),
        '4-5-1 (Defensive)':(222, 219),
        '4-3-3 (False 9)':(406, 219),
        '5-3-2 (Flat)':(589, 219),
        '4-3-3 (Flat)':(41, 394),
        '4-3-3 (Attacking)':(221, 394),
        '4-2-3-1 (Narrow)':(406, 394),
        '4-1-2-1-2 (Narrow)':(590, 394),
    }

    formation_selection_width, formation_selection_height = 162, 124
    currently_hovering_formation, hovering_formation = False, ''

    def hovering_over_formation(x, y) :
        for formation_select_key in changing_formation_coords :
            if x >= changing_formation_coords[formation_select_key][0] and x <= changing_formation_coords[formation_select_key][0]+formation_selection_width and y >= changing_formation_coords[formation_select_key][1] and y <= changing_formation_coords[formation_select_key][1]+formation_selection_height :
                return True, formation_select_key
        return False, ''

    def display_formation_square(currently_hovering_formation, hovering_formation) :
        if currently_hovering_formation :
            currently_formation_coords = changing_formation_coords[hovering_formation]
            top_left = (currently_formation_coords[0]-10, currently_formation_coords[1]-10)
            top_right = (currently_formation_coords[0]+172, currently_formation_coords[1]-10)
            bottom_left = (currently_formation_coords[0]-10, currently_formation_coords[1]+164)
            bottom_right = (currently_formation_coords[0]+172, currently_formation_coords[1]+164)
            pygame.draw.line(display, red, (top_left), (top_right), (5))
            pygame.draw.line(display, red, (top_left), (bottom_left), (5))
            pygame.draw.line(display, red, (bottom_left), (bottom_right), (5))
            pygame.draw.line(display, red, (bottom_right), (top_right), (5))

    swapping_indexes = [[], [2, 3, 4, 5, 6, 7, 8, 9, 10], [3, 4, 5, 6, 7, 8, 9, 10], [4, 5, 6, 7, 8, 9, 10], [5, 6, 7, 8, 9, 10], [6, 7, 8, 9, 10], [7, 8, 9, 10], [8, 9, 10], [9, 10], [10], []]

    def swap_two_values(array, index1, index2) :
        value1, value2 = array[index1], array[index2]
        value1_difference, value2_difference = value1-value2, value2-value1
        array[index1] = array[index1]-(value1_difference)
        array[index2] = array[index2]-(value2_difference)
        return array


    closest_position_dictionary = {
        'GK':['GK', 'CB', 'RB', 'LB', 'RWB', 'LWB', 'CDM', 'CM', 'CAM', 'CF', 'LM', 'LW', 'RM', 'RW', 'ST'],
        'CB':['CB', 'RB', 'LB', 'CDM', 'RWB', 'LWB', 'CM', 'CAM', 'CF', 'LM', 'LW', 'RM', 'RW', 'ST', 'GK'],
        'RCB':['CB', 'RB', 'LB', 'CDM', 'RWB', 'LWB', 'CM', 'CAM', 'CF', 'LM', 'LW', 'RM', 'RW', 'ST', 'GK'],
        'LCB':['CB', 'RB', 'LB', 'CDM', 'RWB', 'LWB', 'CM', 'CAM', 'CF', 'LM', 'LW', 'RM', 'RW', 'ST', 'GK'],
        'RB':['RB', 'LB', 'RWB', 'LWB', 'CB', 'RM', 'LM', 'CDM', 'CM', 'RW', 'LW', 'CAM', 'CF', 'ST', 'GK'],
        'LB':['LB', 'RB', 'LWB', 'RWB', 'CB', 'LM', 'RM', 'CDM', 'CM', 'LW', 'RW', 'CAM', 'CF', 'ST', 'GK'],
        'RWB':['RWB', 'LWB', 'RB', 'LB', 'RM', 'LM', 'CB', 'CDM', 'CM', 'RW', 'LW', 'CAM', 'CF', 'ST', 'GK'],
        'LWB':['LWB', 'RWB', 'LB', 'RB', 'LM', 'RM', 'CB', 'CDM', 'CM', 'LW', 'RW', 'CAM', 'CF', 'ST', 'GK'],
        'CDM':['CDM', 'CM', 'CB', 'RB', 'LB', 'RWB', 'LWB', 'RM', 'LM', 'CAM', 'CF', 'RW', 'LW', 'ST', 'GK'],
        'RDM':['CDM', 'CM', 'CB', 'RB', 'LB', 'RWB', 'LWB', 'RM', 'LM', 'CAM', 'CF', 'RW', 'LW', 'ST', 'GK'],
        'LDM':['CDM', 'CM', 'CB', 'LB', 'RB', 'LWB', 'RWB', 'LM', 'RM', 'CAM', 'CF', 'LW', 'RW', 'ST', 'GK'],
        'CM':['CM', 'CDM', 'CAM', 'RM', 'LM', 'RWB', 'LWB', 'RB', 'LB', 'CB', 'CF', 'ST', 'RW', 'LW', 'GK'],
        'RCM':['CM', 'CDM', 'CAM', 'RM', 'LM', 'RWB', 'LWB', 'RB', 'LB', 'CB', 'CF', 'RW', 'LW', 'ST', 'GK'],
        'LCM':['CM', 'CDM', 'CAM', 'LM', 'RM', 'LWB', 'RWB', 'LB', 'RB', 'CB', 'CF', 'LW', 'RW', 'ST', 'GK'],
        'CAM':['CAM', 'CF', 'CM', 'RM', 'LM', 'ST', 'RW', 'LW', 'CDM', 'RWB', 'LWB', 'CB', 'RB', 'LB', 'GK'],
        'RAM':['CAM', 'CF', 'CM', 'RM', 'LM', 'ST', 'RW', 'LW', 'CDM', 'RWB', 'LWB', 'CB', 'RB', 'LB', 'GK'],
        'LAM':['CAM', 'CF', 'CM', 'LM', 'RM', 'ST', 'LW', 'RW', 'CDM', 'LWB', 'RWB', 'CB', 'LB', 'RB', 'GK'],
        'RM':['RM', 'LM', 'RW', 'LW', 'RWB', 'LWB', 'CAM', 'CM', 'RB', 'LB', 'ST', 'CF', 'CDM', 'CB', 'GK'],
        'LM':['LM', 'RM', 'LW', 'RW', 'LWB', 'RWB', 'CAM', 'CM', 'LB', 'RB', 'ST', 'CF', 'CDM', 'CB', 'GK'],
        'RW':['RW', 'LW', 'RM', 'LM', 'CAM', 'ST', 'CF', 'CM', 'RWB', 'LWB', 'RB', 'LB', 'CDM', 'CB', 'GK'],
        'LW':['LW', 'RW', 'LM', 'RM', 'CAM', 'ST', 'CF', 'CM', 'LWB', 'RWB', 'LB', 'RB', 'CDM', 'CB', 'GK'],
        'ST':['ST', 'CF', 'CAM', 'RW', 'LW', 'RM', 'LM', 'CM', 'CDM', 'RWB', 'LWB', 'RB', 'LB', 'CB', 'GK'],
        'RS':['ST', 'CF', 'CAM', 'RW', 'LW', 'RM', 'LM', 'CM', 'CDM', 'RWB', 'LWB', 'RB', 'LB', 'CB', 'GK'],
        'LS':['ST', 'CF', 'CAM', 'LW', 'RW', 'LM', 'RM', 'CM', 'CDM', 'LWB', 'RWB', 'LB', 'RB', 'CB', 'GK'],
        'CF':['CF', 'CAM', 'ST', 'RW', 'LW', 'RM', 'LM', 'CM', 'CDM', 'RWB', 'LWB', 'RB', 'LB', 'CB', 'GK'],
    }

    def refine_by_swapping(attempt_lineup, new_formation, new_positions) :
        player_positions_ratings = {player_name:current_data[team+'_Players'][player_name]['Positions'] for player_name in attempt_lineup}
        while True :
            swapped_at_all = False
            for lineup_index in range(11) :
                swapping = swapping_indexes[lineup_index]
                swapped = False
                for s_index in swapping :
                    lineup_position, s_position = convert_outside_position_to_center(new_positions[lineup_index]), convert_outside_position_to_center(new_positions[s_index])
                    lineup_position_rating, s_position_rating = player_positions_ratings[attempt_lineup[lineup_index]][lineup_position], player_positions_ratings[attempt_lineup[s_index]][s_position]
                    lineup_position_srating, s_position_srating = player_positions_ratings[attempt_lineup[s_index]][lineup_position], player_positions_ratings[attempt_lineup[lineup_index]][s_position]
                    current_sum, potential_sum = lineup_position_rating+s_position_rating, lineup_position_srating+s_position_srating
                    if potential_sum > current_sum :
                        indexes_array = swap_two_values(list(range(11)), lineup_index, s_index)
                        attempt_lineup = [attempt_lineup[i] for i in indexes_array]
                        swapped = True
                        swapped_at_all = True
                        break
                if swapped :
                    break
            if not swapped_at_all :
                break
        return attempt_lineup 

    def rearrange_lineup_formation_change(new_formation, new_positions) :
        current_lineup = current_data['CurrentLineup']
        preffered_positions = {}
        for basic_position in possible_player_data_values['Position'] :
            preffered_positions[basic_position] = [player_name for player_name in current_lineup if current_data[team+'_Players'][player_name]['Position'] == basic_position]
        attempt_lineup = []
        for new_position in new_positions :
            most_likely_positions = closest_position_dictionary[new_position]
            for mlp in most_likely_positions :
                if preffered_positions[mlp] != [] :
                    first_player = preffered_positions[mlp][0]
                    attempt_lineup.append(first_player)
                    preffered_positions[mlp].remove(first_player)
                    break
        return refine_by_swapping(attempt_lineup, new_formation, new_positions)
        
    def get_rol(pos, first) :
        if pos in ['RCB', 'CB', 'LCB'] :
            return first+'CB'
        if pos in ['RDM', 'CDM', 'LDM'] :
            return first+'DM'
        if pos in ['RCM', 'CM', 'LCM'] :
            return first+'CM'
        if pos in ['RAM', 'CAM', 'LAM'] :
            return first+'AM'
        if pos in ['RB', 'LB'] :
            return first+'B'
        if pos in ['RS', 'LS'] :
            return first+'S'
        if pos in ['RM', 'LM'] :
            return first+'M'
        if pos in ['RW', 'LW'] :
            return first+'W'
        if pos in ['RWB', 'LWB'] :
            return first+'WB'


    def new_formation_lefts_and_rights(positions_in_order, lineup_in_order) :
        real_positions = {n:current_data[team+'_Players'][n]['Position'] for n in lineup_in_order}
        for i in range(11) :
            current_pos, current_player_in_lineup = positions_in_order[i], lineup_in_order[i]
            real_position = real_positions[current_player_in_lineup]
            possibility_build = None
            if real_position[0] in ['R', 'L'] :
                if current_pos[0] != real_position[0] :
                    possibility_build = get_rol(current_pos, real_position[0])
            if real_position[0] == 'C' and current_pos[0] != 'C' :
                if current_pos[1:] == ['CM'] :
                    possibility_build = 'CM'
                if current_pos[1:] == 'AM' :
                    possibility_build = 'CAM'
                if current_pos[1:] == 'CB' :
                    possibility_build = 'CB'
            if possibility_build in positions_in_order :
                index_possibility = positions_in_order.index(possibility_build)
                name_possibility = lineup_in_order[index_possibility]
                lineup_in_order[i] = name_possibility
                lineup_in_order[index_possibility] = current_player_in_lineup
        return lineup_in_order

    #######################################################################################################################################


    #The "manager_loop" variable is always True, it runs every other loop
    manager_loop = True

    #All of these variables are the loops for every screen
    calendar = True
    lineups = False
    standings = False
    transfers = False
    emails = False
    training = False


    #Temporary text
    lineups_text = myfont.render('Lineups', True, black)
    standings_text = myfont.render('Standings', True, black)
    transfers_text = myfont.render('Transfers', True, black)
    emails_text = myfont.render('Emails', True, black)
    training_text = myfont.render('Training', True, black)

    #Here is where we actually run the UI
    while manager_loop :
        while lineups :
            if player_reporting :
                display.fill(white)
                display.blit(player_report_screen, (0, 0))
                display_player_data(player_selected_data, name_text)
                x, y = pygame.mouse.get_pos()
                over_return_to_squads_button = display_button(return_to_squads_button, (x, y))
                for event in pygame.event.get() :
                    if event.type == pygame.MOUSEBUTTONDOWN :
                        if over_return_to_squads_button :
                            player_reporting = False
                            changing_formation = False
            elif changing_formation :
                display.fill(white)
                display.blit(changing_formation_screen, (0, 0))
                x, y = pygame.mouse.get_pos()
                for event in pygame.event.get() :
                    if event.type == pygame.MOUSEBUTTONDOWN :
                        if currently_hovering_formation :
                            changing_formation = False
                            player_reporting = False
                            new_posi = get_positions_from_formation(hovering_formation)
                            current_data['CurrentLineup'] = new_formation_lefts_and_rights(get_positions_from_formation(hovering_formation), rearrange_lineup_formation_change(hovering_formation, new_posi))
                            current_data['CurrentFormation'] = hovering_formation
                            current_data['CurrentTeamRating'] = calculate_rating(current_data[team+'_Players'], current_data['CurrentLineup'], current_data['CurrentFormation'])
                            current_team_rating_text = myfont6.render(str(current_data['CurrentTeamRating']), True, ratings_rgb[current_data['CurrentTeamRating']])
                            jersey_coords = get_coords(current_data['CurrentFormation'])
                            save_progress()
                currently_hovering_formation, hovering_formation = hovering_over_formation(x, y)
                display_formation_square(currently_hovering_formation, hovering_formation)
            else :
                display.fill(white)
                display.blit(lineup_backgrounds[current_data['CurrentFormation']], (0, 0))
                display.blit(team_logos[team], (10, 10))
                display.blit(mr_manager_team, (60, 10))
                display.blit(mr_manager_name, (60, 30))
                display.blit(current_team_rating_text, (210, 100))
                display.blit(current_bench_page_text, (current_bench_page_text_x, 105))
                display_starting_lineup()
                display_bench_players()
                x, y = pygame.mouse.get_pos()
                over_change_formation = display_button(change_formation_button, (x, y))
                over_last_page_button = display_button(last_page_button, (x, y))
                over_next_page_button = display_button(next_page_button, (x, y))
                hover_square, hover_square_coords, hover_square_position = get_hover_square_coords(x, y, jersey_coords)
                display_hover_square(hover_square, hover_square_coords, currently_moving_key, alpha_swapping_count, just_clicked_coords, jersey_coords=jersey_coords)
                bench_hover_square, bench_hover_square_coords, bench_hover_square_position = get_hover_square_coords(x, y, bench_coords)
                display_hover_square(bench_hover_square, bench_hover_square_coords, currently_moving_key, alpha_swapping_count, just_clicked_coords)
                alpha_swapping_count += alpha_swapping_count_change
                if alpha_swapping_count > 150 :
                    alpha_swapping_count = 150
                    alpha_swapping_count_change = -5
                elif alpha_swapping_count < 1 :
                    alpha_swapping_count = 1
                    alpha_swapping_count_change = 5
                for event in pygame.event.get() :
                    if event.type == pygame.KEYDOWN :
                        if event.key == pygame.K_RIGHT :
                            lineups = False
                            standings = True
                        if event.key == pygame.K_LEFT :
                            lineups = False
                            calendar = True
                    if event.type == pygame.MOUSEBUTTONDOWN :
                        if hover_square :
                            if event.button == 3 :
                                changing_formation = False
                                player_reporting = True
                                position_selected = all_positions_in_order[current_data['CurrentFormation']]
                                player_selected_name = current_data['CurrentLineup'][position_selected.index(hover_square_position)]
                                player_selected_info = current_data[team+'_Players'][player_selected_name]
                                player_selected_display_keys = ['Rating', 'Position', 'Age', 'Nation', 'Height', 'Weight', 'Freshness', 'Goals', 'Assists', 'Team']
                                player_selected_data = {player_selected_display_key:player_selected_info[player_selected_display_key] for player_selected_display_key in player_selected_display_keys}
                                name_text = player_reporting_fonts['Name'].render(player_selected_name, True, (255, 195, 116))
                                currently_moving_key = None
                            elif event.button == 1 :
                                position_selected = all_positions_in_order[current_data['CurrentFormation']]
                                if currently_moving_key == None :
                                    currently_moving_key = current_data['CurrentLineup'][position_selected.index(hover_square_position)]
                                    alpha_swapping_count = 150
                                    just_clicked_coords = hover_square_coords
                                else :
                                    lineup = current_data['CurrentLineup']
                                    index2 = position_selected.index(hover_square_position)
                                    if currently_moving_key in lineup :
                                        index1 = lineup.index(currently_moving_key)
                                        array = list(range(11))
                                        current_data['CurrentLineup'] = [current_data['CurrentLineup'][index] for index in swap_two_values(array, index1, index2)]
                                    else :
                                        current_data['CurrentLineup'][index2] = currently_moving_key
                                    current_data['CurrentTeamRating'] = calculate_rating(current_data[team+'_Players'], current_data['CurrentLineup'], current_data['CurrentFormation'])
                                    current_team_rating_text = myfont6.render(str(current_data['CurrentTeamRating']), True, ratings_rgb[current_data['CurrentTeamRating']])
                                    currently_moving_key = None
                                    current_bench_page_players = get_current_page_of_bench(current_bench_page)
                                    
                                    save_progress()
                        
                        elif over_change_formation :
                            changing_formation = True
                            player_reporting = False
                        elif over_last_page_button :
                            if current_bench_page != 0 :
                                current_bench_page -= 1
                                current_bench_page_players = get_current_page_of_bench(current_bench_page)
                                current_bench_page_text = myfont.render('Page Number: '+str(current_bench_page+1), True, white)
                                current_bench_page_text_width = current_bench_page_text.get_width()
                                current_bench_page_text_x = (625+((705-625)/2))-int((current_bench_page_text_width/2))
                            else :
                                #print('Cant go back page')
                                pass
                        elif over_next_page_button :
                            current_bench_page += 1
                            current_bench_page_players = get_current_page_of_bench(current_bench_page)
                            if current_bench_page_players != None :
                                current_bench_page_text = myfont.render('Page Number: '+str(current_bench_page+1), True, white)
                                current_bench_page_text_width = current_bench_page_text.get_width()
                                current_bench_page_text_x = (625+((705-625)/2))-int((current_bench_page_text_width/2))
                            else :
                                #print('Cant go forward page')
                                pass
                                current_bench_page -= 1
                                current_bench_page_players = get_current_page_of_bench(current_bench_page)
                        elif bench_hover_square :
                            if event.button == 3 :
                                changing_formation = False
                                player_reporting = True
                                position_selected = all_positions_in_order[current_data['CurrentFormation']]
                                for bench_coords_key in bench_coords :
                                    if bench_hover_square_coords == bench_coords[bench_coords_key] :
                                        player_selected_name = current_bench_page_players[bench_coords_key]
                                        break
                                player_selected_info = current_data[team+'_Players'][player_selected_name]
                                player_selected_display_keys = ['Rating', 'Position', 'Age', 'Nation', 'Height', 'Weight', 'Freshness', 'Goals', 'Assists', 'Team']
                                player_selected_data = {player_selected_display_key:player_selected_info[player_selected_display_key] for player_selected_display_key in player_selected_display_keys}
                                name_text = player_reporting_fonts['Name'].render(player_selected_name, True, (255, 195, 116))
                                currently_moving_key = None
                            elif event.button == 1 :
                                position_selected = all_positions_in_order[current_data['CurrentFormation']]
                                if currently_moving_key == None :
                                    for bench_coords_key in bench_coords :
                                        if bench_hover_square_coords == bench_coords[bench_coords_key] :
                                            currently_moving_key = current_bench_page_players[bench_coords_key]
                                            break
                                    alpha_swapping_count = 150
                                    just_clicked_coords = bench_hover_square_coords
                                else :
                                    lineup = current_data['CurrentLineup']
                                    if currently_moving_key in lineup :
                                        index1 = lineup.index(currently_moving_key)
                                        for bench_coords_key in bench_coords :
                                            if bench_hover_square_coords == bench_coords[bench_coords_key] :
                                                lineup[index1] = current_bench_page_players[bench_coords_key]
                                                break
                                        current_data['CurrentLineup'] = lineup
                                        current_data['CurrentTeamRating'] = calculate_rating(current_data[team+'_Players'], current_data['CurrentLineup'], current_data['CurrentFormation'])
                                        current_team_rating_text = myfont6.render(str(current_data['CurrentTeamRating']), True, ratings_rgb[current_data['CurrentTeamRating']])
                                        current_bench_page_players = get_current_page_of_bench(current_bench_page)
                                        
                                        save_progress()
                                        
                                    currently_moving_key = None
            pygame.display.update()
        while training :
            display.fill(white)
            display.blit(training_text, (0, 0))
            for event in pygame.event.get() :
                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_RIGHT :
                        training = False
                        calendar = True
                    if event.key == pygame.K_LEFT :
                        training = False
                        emails = True
            pygame.display.update()
        while emails :
            display.fill(white)
            display.blit(emails_text, (0, 0))
            for event in pygame.event.get() :
                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_RIGHT :
                        emails = False
                        training = True
                    if event.key == pygame.K_LEFT :
                        emails = False
                        transfers = True
            pygame.display.update()
        
        while transfers :
            display.fill(white)
            display.blit(transfers_text, (0, 0))
            for event in pygame.event.get() :
                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_RIGHT :
                        transfers = False
                        emails = True
                    if event.key == pygame.K_LEFT :
                        transfers = False
                        standings = True
            pygame.display.update()
        
        while standings :
            display.fill(white)
            display.blit(standings_background, (0, 0))
            display.blit(team_logos[team], (10, 10))
            display.blit(mr_manager_team, (60, 10))
            display.blit(mr_manager_name, (60, 30))
            display_standings_headers()
            display_standings_data()
            for event in pygame.event.get() :
                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_RIGHT :
                        standings = False
                        transfers = True
                    if event.key == pygame.K_LEFT :
                        standings = False
                        lineups = True
            pygame.display.update()
        
        #Calendar Screen
        while calendar :
            
            #Fill background with white
            display.fill(white)
            
            #If the user simming a match
            if match_simming :
                
                #Get mouse position
                x, y = pygame.mouse.get_pos()
                
                #Display the Match Sim Background
                display.blit(match_sim_background, (0, 0))
                
                #Display the text that tells the user what the stadium is playing at
                display.blit(stadium_text, (stadium_text_x, 500))
                
                #Display the logo of the user's team logo
                display.blit(user_logo, (user_logo_x, user_logo_y))
                
                #Display the name of the user's team 
                display.blit(user_logo_text, (user_logo_text_x, user_logo_text_y))
                
                #Display the logo of the opponent's team logo
                display.blit(opponent_logo, (opponent_logo_x, opponent_logo_y))
                
                #Display the name of the opponent's team 
                display.blit(opponent_logo_text, (opponent_logo_text_x, opponent_logo_text_y))
                
                #Display the minute of the game
                display.blit(simming_minute_texts[current_minute-1], (simming_minute_texts_x[current_minute-1], 80))
                
                for sc_texts in currently_displaying :
                    t, c = sc_texts
                    display.blit(t, c)
                
                #Display the scoreboard. If the variable "next_left_or_right" variable == 0, it means that the user is the home
                if next_left_or_right == 0 :
                    display_score(current_user_score, opponent_score)
                else :
                    display_score(opponent_score, current_user_score)
                
                #If the user is currently simming
                if currently_simming :
                    
                    #This frame count variable adds one to the current minute when it reaches 20
                    current_minute_count += 1
                    
                    #If the frames get to 20, add a minute 
                    if current_minute_count == current_minute_max_count :
                        current_minute_count = 0
                        current_minute += 1
                        
                        #Accounts for if user's team scores in the current_minute
                        if current_minute in user_score_minutes :
                            current_user_score += 1
                            user_scorer = user_scorers[user_score_minutes.index(current_minute)]
                            if not user_scorer in user_names_already_displayed :
                                next_scorer_coords = user_scorers_texts_coords[user_ind]
                                next_scorer_text = user_scorers_texts[user_ind]
                                currently_displaying.append([next_scorer_text, next_scorer_coords])
                                l_x = next_scorer_coords[0]+next_scorer_text.get_width()+10
                                minn_text = simming_scoring_minutes_texts[current_minute-1]
                                currently_displaying.append([minn_text, (l_x, next_scorer_coords[1])])
                                user_scorers_texts_last_x.append(l_x+minn_text.get_width())
                                user_names_already_displayed.append(user_scorer)
                                user_ind += 1
                            else :
                                bruh_index = user_names_already_displayed.index(user_scorer)
                                comma_text_x = user_scorers_texts_last_x[bruh_index]
                                currently_displaying.append([comma_text, (comma_text_x, user_scorers_texts_coords[bruh_index][1])])
                                another_minute_x = comma_text_x+10
                                minn_text = simming_scoring_minutes_texts[current_minute-1]
                                currently_displaying.append([minn_text, (another_minute_x, user_scorers_texts_coords[bruh_index][1])])
                                user_scorers_texts_last_x[bruh_index] = another_minute_x+minn_text.get_width()

                        #Accounts for if opponent scores in the current_minute
                        if current_minute in opponent_score_minutes :
                            opponent_score += 1
                            opponent_scorer = opponent_scorers[opponent_score_minutes.index(current_minute)]
                            if not opponent_scorer in opponent_names_already_displayed :
                                next_scorer_coords = opponent_scorers_texts_coords[opponent_ind]
                                next_scorer_text = opponent_scorers_texts[opponent_ind]
                                currently_displaying.append([next_scorer_text, next_scorer_coords])
                                l_x = next_scorer_coords[0]+next_scorer_text.get_width()+10
                                minn_text = simming_scoring_minutes_texts[current_minute-1]
                                currently_displaying.append([minn_text, (l_x, next_scorer_coords[1])])
                                opponent_scorers_texts_last_x.append(l_x+minn_text.get_width())
                                opponent_names_already_displayed.append(opponent_scorer)
                                opponent_ind += 1
                            else :
                                bruh_index = opponent_names_already_displayed.index(opponent_scorer)
                                comma_text_x = opponent_scorers_texts_last_x[bruh_index]
                                currently_displaying.append([comma_text, (comma_text_x, opponent_scorers_texts_coords[bruh_index][1])])
                                another_minute_x = comma_text_x+10
                                minn_text = simming_scoring_minutes_texts[current_minute-1]
                                currently_displaying.append([minn_text, (another_minute_x, opponent_scorers_texts_coords[bruh_index][1])])
                                opponent_scorers_texts_last_x[bruh_index] = another_minute_x+minn_text.get_width()
                        
                        #If the game reaches 90 minutes, display the return button 
                        if current_minute == 90 :
                            currently_simming = False
                            return_available = True
                    
                #These two instances are seeing if the user is hovering over the return button and the start simming button, respectively
                elif return_available :
                    over_button2 = display_button(return_simming_button, (x, y))
                else :
                    over_button1 = display_button(start_simming_button, (x, y))
                
                #This is the event loop detects for button clicks
                for event in pygame.event.get() :
                    if event.type == pygame.MOUSEBUTTONDOWN :
                        
                        #If the user is hovering over the Start Sim Button, start the sim
                        if over_button1 :
                            currently_simming = True
                            over_button1 = False
                        
                        #If the user is hovering over the return button, reset all of the variables and go back to calendar screen
                        if over_button2 :
                            
                            #If the user clicks the Return Button, reset all of the variables for this screen for next time
                            
                            #Make the "match_simming" variable False so the user returns back to the normal calendar screen
                            match_simming = False
                            
                            #The "return_available" variable whether or not we should display the Return to Calendar Screen button
                            return_available = False

                            #These two variables tell us if the user is hovering over the Start Match button and the Return to Menu button, respectively
                            over_button1 = False
                            over_button2 = False

                            #The "calendar_calendar_button_index" integer picks the correct button from "calendar_buttons"
                            calendar_button_index = 0

                            #The "over_sim_button" variable tells us whether or not the user is hovering over the Start Simulation button
                            over_sim_button = False

                            #The "simming" variable tells us whether or not we are currently simming
                            simming = False

                            #The "stopped_on_matchday" variable tells us whether or not the next simming action will be to play the match
                            stopped_on_matchday = False

                            #The "simming_count" adds one every frame. When it gets to 50, one day is progressed
                            simming_count = 0

                            #The "match_simming" variable almost acts as a whole loop, but it is under "calendar"
                            match_simming = False
            else :
                display.blit(current_calendar_screen, (0, 0))
                display.blit(team_logos[team], (10, 10))
                display.blit(mr_manager_team, (60, 10))
                display.blit(mr_manager_name, (60, 30))
                x, y = pygame.mouse.get_pos()
                for game_date in dates_of_games_in_month :
                    opponent, stadium, left_or_right = dates_of_games_in_month[game_date]
                    m, d = game_date.split(' ')
                    display_coords = coords_of_days[d]
                    display_coords_logo = (display_coords[0]+15, display_coords[1]+30)
                    display_coords_text = (display_coords[0]+22, display_coords[1]+10)
                    display_coords_text2 = (display_coords[0]+30, display_coords[1]+20)
                    display.blit(team_logos[opponent], display_coords_logo)
                    display.blit(GAME_text, display_coords_text)
                    display.blit(GAMEVS_text, display_coords_text2)
                for event in pygame.event.get() :
                    if event.type == pygame.KEYDOWN :
                        if event.key == pygame.K_RIGHT :
                            calendar = False
                            lineups = True
                        if event.key == pygame.K_LEFT :
                            calendar = False
                            training = True
                    if event.type == pygame.MOUSEBUTTONDOWN :
                        if over_sim_button :
                            if stopped_on_matchday :
                                match_simming = True
                                stadium_text = myfont.render(next_stadium, True, white)
                                stadium_text_width = stadium_text.get_width()
                                stadium_text_x = int((display_width-stadium_text_width)/2)
                                user_logo, user_logo_text, user_logo_x, user_logo_text_x, user_logo_y, user_logo_text_y = get_coords_of_logo_and_text(team, next_left_or_right)
                                if next_left_or_right == 0 :
                                    opponent_lor = 1
                                else :
                                    opponent_lor = 0
                                opponent_logo, opponent_logo_text, opponent_logo_x, opponent_logo_text_x, opponent_logo_y, opponent_logo_text_y = get_coords_of_logo_and_text(next_opponent, opponent_lor)

                                
                                user_formation = current_data['CurrentFormation']
                                user_players = current_data[team+'_Players']
                                user_lineup = current_data['CurrentLineup']

                                opponent_formation = current_data[next_opponent+'_Formation']
                                opponent_players = current_data[next_opponent+'_Players']
                                opponent_lineup = current_data[next_opponent+'_Lineup']
                                
                                
                                user_rating = current_data['CurrentTeamRating']
                                opponent_rating = calculate_rating(opponent_players, opponent_lineup, opponent_formation)
                                print(user_rating, opponent_rating)

                                if next_left_or_right == 0 :
                                    winner, score_difference = match_sim(user_rating, opponent_rating, team, next_opponent)
                                    score, user_scorers, opponent_scorers = randomize_goals(user_players, opponent_players, user_lineup, opponent_lineup, team, next_opponent, user_formation, opponent_formation, winner, score_difference)
                                    s_one, s_two = score.split('-')
                                    final_user_score, final_opponent_score = int(s_one), int(s_two)
                                    user_scorers_text_x, opponent_scorers_text_x = 75, half+20
                                    update_standings_info(team, next_opponent, winner, final_user_score, final_opponent_score)
                                else :
                                    winner, score_difference = match_sim(opponent_rating, user_rating, next_opponent, team)
                                    score, opponent_scorers, user_scorers = randomize_goals(opponent_players, user_players, opponent_lineup, user_lineup, next_opponent, team, opponent_formation, user_formation, winner, score_difference)
                                    s_one, s_two = score.split('-')
                                    final_opponent_score, final_user_score = int(s_one), int(s_two)
                                    opponent_scorers_text_x, user_scorers_text_x = 75, half+20
                                    update_standings_info(next_opponent, team, winner, final_opponent_score, final_user_score)
                                
                                user_scorers_texts, user_scorers_texts_coords = get_scorers_text_and_coords(user_scorers, user_scorers_text_x)
                                opponent_scorers_texts, opponent_scorers_texts_coords = get_scorers_text_and_coords(opponent_scorers, opponent_scorers_text_x)
                                user_scorers_texts_last_x, opponent_scorers_texts_last_x = [], []
                                
                                user_ind, opponent_ind = 0, 0
                                
                                currently_displaying = []
                                user_names_already_displayed = []
                                opponent_names_already_displayed = []
                                
                                current_user_score, opponent_score = 0, 0
                                current_minute = 1
                                current_minute_count = 0
                                current_minute_max_count = 1
                                user_score_minutes, opponent_score_minutes = randomize_goals_minutes(final_user_score), randomize_goals_minutes(final_opponent_score)
                                
                                user_score_minutes = sorted(user_score_minutes)
                                opponent_score_minutes = sorted(opponent_score_minutes)
                                
                                currently_simming = False
                                
                                for nop in user_scorers :
                                    current_data[team+'_Players'][nop]['Goals'] += 1
                                    if nop in current_data['TopScorersInOrder'] :
                                        current_data['TopScorers'][nop] += 1
                                        
                                for nop in opponent_scorers :
                                    current_data[next_opponent+'_Players'][nop]['Goals'] += 1
                                    if nop in current_data['TopScorersInOrder'] :
                                        current_data['TopScorers'][nop] += 1
                                
                                if winner == 'Draw' :
                                    current_data['CurrentStandings'][team] += 1
                                    current_data['CurrentStandings'][next_opponent] += 1
                                else :
                                    current_data['CurrentStandings'][winner] += 3
                                
                                put_standings_in_correct_order()
                                update_top_scorers(user_scorers, team, opponent_scorers, next_opponent)
                                
                                save_progress()

                                
                            else :
                                if not simming :
                                    simming = True
                                    calendar_button_index += 1
                                else :
                                    simming = False
                                    calendar_button_index -= 1
                                    simming_count = 0
                display.blit(red_cover, coords_of_days[str(day)])
                over_sim_button = display_button(calendar_buttons[calendar_button_index], (x, y))
                if simming :
                    simming_count += 1
                    if simming_count == 5 :
                        current_date, next_month = advance_one_day(current_date)
                        current_data['CurrentDate'] = current_date
                        month, day, year = unpack_date(current_date)
                        without_year = ' '.join([month, str(day)])
                        if next_month :
                            month_number = get_month_number(month)
                            current_calendar_screen = calendar_screens[month_number]
                            dates_of_games_in_month = get_games_in_a_month(month, schedule_dict, team)
                            games_in_current_month = {date:schedule_dict[date] for date in schedule_dict if date.split(' ')[0] == month}
                        if without_year in games_in_current_month :
                            sim_other_games(without_year, games_in_current_month)
                        try :
                            next_opponent, next_stadium, next_left_or_right = dates_of_games_in_month[without_year]
                            
                            stopped_on_matchday = True

                            simming = False
                            calendar_button_index = 2
                            simming_count = 0
                        except :
                            pass
                        simming_count = 0
                        save_progress()
            pygame.display.update()

#game(1)
