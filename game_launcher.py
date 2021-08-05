#!/usr/bin/env python3

import pygame, pickle, game
from os import listdir
from file_path_converter import convert_path

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

def mouse_over_button(pos, x, y, width, height) :
	return pos[0] >= x and pos[0] <= x+width and pos[1] >= y and pos[1] <= y+height

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

#Saves Screen Stuff

#######################################################################################################################################

#The "save_number" is the variable that dictates which save the user is hovering over
save_number = 0

#Function that loads the save screen given the save number
def get_save_image(save_number) :
	path = ''.join(['C:\\Users\\rhyde23\\Desktop\\Project\\Images\\', 'Save', str(save_number), '.png'])
	if pi :
		path = convert_path(path)
	return pygame.image.load(path).convert()

#The "save_background_images" array is an array of loaded images that will light up each save button when the mouse is over it
save_background_images = []
for i in range(10) :
	current_save_image = get_save_image(i+1)
	save_background_images.append(current_save_image)

#The current image from "save_background_images"
current_save_image = save_background_images[save_number]

#Same basic concept of loading saves, but this time it's loading the basic information for each save like the save name
save_names = []
not_empty_saves = []
for i in range(10) :
	path = ''.join(['C:\\Users\\rhyde23\\Desktop\\Project\\Saves\\', 'File', str(i+1), 'BasicInfo.dat'])
	if pi :
		path = convert_path(path)
	basic_info = pickle.load(open(path, 'rb'))
	if basic_info['Opened'] :
		not_empty_saves.append(i)
	save_names.append(basic_info['SaveName'])
#Render the fonts for each button 
save_names_texts = []
for save_name in save_names :
	save_names_texts.append(myfont.render(save_name, True, (0, 0, 0)))

#"clicker_mode" indicates the coordinates of where the user clicked, I used this for early development
clicker_mode = False
current_clicked = (0, 0)

#Forming the array "buttons", which is an array of the y coordinates that dictates whether the user is hovering over a button
y_difference = 37
x_start, x_end = 43, 761
buttons = []
for i in range(10) :
	first_y = 154+(i*y_difference)
	second_y = first_y+y_difference
	buttons.append([first_y, second_y])

#"offset" is to make the y coordinates of text centered
offset = [12, 13, 14, 16, 17, 19, 20, 22, 23, 25]

#"save_selected" is final variable of this screen, and it's set to None right now
save_selected = None

#######################################################################################################################################

#Name Save Stuff

#IMPORTANT NOTE: THIS LOOP CONTROLS THE USER INPUT FOR THE NAME OF THE SAVE AND THE MANAGER NAME

#######################################################################################################################################


#The "keyboard_order" dictionary loads all of the images that light up the keys on the virtual keyboard 
if not pi :
	keyboard_order = {
		pygame.K_m:pygame.image.load('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-002.png').convert(),
		pygame.K_n:pygame.image.load('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-003.png').convert(),
		pygame.K_b:pygame.image.load('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-004.png').convert(),
		pygame.K_v:pygame.image.load('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-005.png').convert(),
		pygame.K_c:pygame.image.load('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-006.png').convert(),
		pygame.K_x:pygame.image.load('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-007.png').convert(),
		pygame.K_z:pygame.image.load('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-008.png').convert(),
		pygame.K_l:pygame.image.load('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-009.png').convert(),
		pygame.K_k:pygame.image.load('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-010.png').convert(),
		pygame.K_j:pygame.image.load('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-011.png').convert(),
		pygame.K_h:pygame.image.load('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-012.png').convert(),
		pygame.K_g:pygame.image.load('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-013.png').convert(),
		pygame.K_f:pygame.image.load('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-014.png').convert(),
		pygame.K_d:pygame.image.load('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-015.png').convert(),
		pygame.K_s:pygame.image.load('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-016.png').convert(),
		pygame.K_a:pygame.image.load('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-017.png').convert(),
		pygame.K_p:pygame.image.load('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-018.png').convert(),
		pygame.K_o:pygame.image.load('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-019.png').convert(),
		pygame.K_i:pygame.image.load('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-020.png').convert(),
		pygame.K_u:pygame.image.load('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-021.png').convert(),
		pygame.K_y:pygame.image.load('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-022.png').convert(),
		pygame.K_t:pygame.image.load('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-023.png').convert(),
		pygame.K_r:pygame.image.load('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-024.png').convert(),
		pygame.K_e:pygame.image.load('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-025.png').convert(),
		pygame.K_w:pygame.image.load('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-026.png').convert(),
		pygame.K_q:pygame.image.load('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-027.png').convert(),
		pygame.K_BACKSPACE:pygame.image.load('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-028.png').convert(),
		pygame.K_0:pygame.image.load('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-029.png').convert(),
		pygame.K_9:pygame.image.load('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-030.png').convert(),
		pygame.K_8:pygame.image.load('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-031.png').convert(),
		pygame.K_7:pygame.image.load('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-032.png').convert(),
		pygame.K_6:pygame.image.load('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-033.png').convert(),
		pygame.K_5:pygame.image.load('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-034.png').convert(),
		pygame.K_4:pygame.image.load('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-035.png').convert(),
		pygame.K_3:pygame.image.load('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-036.png').convert(),
		pygame.K_2:pygame.image.load('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-037.png').convert(),
		pygame.K_1:pygame.image.load('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-038.png').convert(),
	}
	
if pi :
	keyboard_order = {
		pygame.K_m:pygame.image.load(convert_path('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-002.png')).convert(),
		pygame.K_n:pygame.image.load(convert_path('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-003.png')).convert(),
		pygame.K_b:pygame.image.load(convert_path('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-004.png')).convert(),
		pygame.K_v:pygame.image.load(convert_path('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-005.png')).convert(),
		pygame.K_c:pygame.image.load(convert_path('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-006.png')).convert(),
		pygame.K_x:pygame.image.load(convert_path('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-007.png')).convert(),
		pygame.K_z:pygame.image.load(convert_path('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-008.png')).convert(),
		pygame.K_l:pygame.image.load(convert_path('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-009.png')).convert(),
		pygame.K_k:pygame.image.load(convert_path('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-010.png')).convert(),
		pygame.K_j:pygame.image.load(convert_path('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-011.png')).convert(),
		pygame.K_h:pygame.image.load(convert_path('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-012.png')).convert(),
		pygame.K_g:pygame.image.load(convert_path('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-013.png')).convert(),
		pygame.K_f:pygame.image.load(convert_path('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-014.png')).convert(),
		pygame.K_d:pygame.image.load(convert_path('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-015.png')).convert(),
		pygame.K_s:pygame.image.load(convert_path('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-016.png')).convert(),
		pygame.K_a:pygame.image.load(convert_path('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-017.png')).convert(),
		pygame.K_p:pygame.image.load(convert_path('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-018.png')).convert(),
		pygame.K_o:pygame.image.load(convert_path('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-019.png')).convert(),
		pygame.K_i:pygame.image.load(convert_path('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-020.png')).convert(),
		pygame.K_u:pygame.image.load(convert_path('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-021.png')).convert(),
		pygame.K_y:pygame.image.load(convert_path('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-022.png')).convert(),
		pygame.K_t:pygame.image.load(convert_path('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-023.png')).convert(),
		pygame.K_r:pygame.image.load(convert_path('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-024.png')).convert(),
		pygame.K_e:pygame.image.load(convert_path('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-025.png')).convert(),
		pygame.K_w:pygame.image.load(convert_path('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-026.png')).convert(),
		pygame.K_q:pygame.image.load(convert_path('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-027.png')).convert(),
		pygame.K_BACKSPACE:pygame.image.load(convert_path('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-028.png')).convert(),
		pygame.K_0:pygame.image.load(convert_path('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-029.png')).convert(),
		pygame.K_9:pygame.image.load(convert_path('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-030.png')).convert(),
		pygame.K_8:pygame.image.load(convert_path('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-031.png')).convert(),
		pygame.K_7:pygame.image.load(convert_path('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-032.png')).convert(),
		pygame.K_6:pygame.image.load(convert_path('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-033.png')).convert(),
		pygame.K_5:pygame.image.load(convert_path('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-034.png')).convert(),
		pygame.K_4:pygame.image.load(convert_path('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-035.png')).convert(),
		pygame.K_3:pygame.image.load(convert_path('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-036.png')).convert(),
		pygame.K_2:pygame.image.load(convert_path('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-037.png')).convert(),
		pygame.K_1:pygame.image.load(convert_path('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-038.png')).convert(),
	}

#The "keyboard_letters" dictionary matches each key pressed with a letter to add to the string of user input
keyboard_letters = {
	pygame.K_m:'M',
	pygame.K_n:'N',
	pygame.K_b:'B',
	pygame.K_v:'V',
	pygame.K_c:'C',
	pygame.K_x:'X',
	pygame.K_z:'Z',
	pygame.K_l:'L',
	pygame.K_k:'K',
	pygame.K_j:'J',
	pygame.K_h:'H',
	pygame.K_g:'G',
	pygame.K_f:'F',
	pygame.K_d:'D',
	pygame.K_s:'S',
	pygame.K_a:'A',
	pygame.K_p:'P',
	pygame.K_o:'O',
	pygame.K_i:'I',
	pygame.K_u:'U',
	pygame.K_y:'Y',
	pygame.K_t:'T',
	pygame.K_r:'R',
	pygame.K_e:'E',
	pygame.K_w:'W',
	pygame.K_q:'Q',
	pygame.K_0:'0',
	pygame.K_9:'9',
	pygame.K_8:'8',
	pygame.K_7:'7',
	pygame.K_6:'6',
	pygame.K_5:'5',
	pygame.K_4:'4',
	pygame.K_3:'3',
	pygame.K_2:'1',
	pygame.K_1:'1',
}

#The "get_x_value" function basically just centers text or buttons or anything based on its width 
def get_x_value(width) :
	return int((display_width-width)/2)

#Setting the typed as an empty string and rendering the text and setting the x position
current_typed = ""
current_typed_text = myfont2.render(current_typed, True, light_blue)
current_typed_x = get_x_value(current_typed_text.get_width())

#Page-001.png is the default state of no keyboard presses
if pi :
	default_typed_screen = pygame.image.load(convert_path('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-001.png')).convert()

if not pi :
	default_typed_screen = pygame.image.load('C:\\Users\\rhyde23\\Desktop\\Project\\Images\\Page-001.png').convert()

#Setting the current keyboard screen as the default one
current_typed_screen = default_typed_screen

#"space_bar_down" controls whether or not to display the space bar pressed image
space_bar_down = False

#The strings "enter_extension_string" and "string2" control what the user sees as they're naming either the save or the manager. These will change to "manager" because the Name Save screen is multipurpose
enter_extension_string = "the Save"
string2 = "save"

#This is rendering the text for the header of the screen that tells the user to enter a name for either the save or manager
name_save_header = myfont2.render("Enter a Name for "+enter_extension_string, True, light_blue)

#The x position is using the "get_x_value" function from earlier
name_save_header_x = get_x_value(name_save_header.get_width())

#This is rendering the text for the warning at the bottom of the screen that tells the user that they've reached 20 characters
too_many_chars_text = myfont.render("You've reached the max amount of characters!", True, red)

#The x position is using the "get_x_value" function from earlier
too_many_chars_x = get_x_value(too_many_chars_text.get_width())

#The "too_many_chars" variable will indicate if the user
too_many_chars = False

#The "enter_or_submit" variable will control if the user sees the text "Enter a name" or "Submit a name" on the multipurpose text location/button
enter_or_submit = True

#The "over_submit" variable represents whether or not the user is hovering over the submit button for naming the save or manager
over_submit = False

#When "entering_save" is True, the user is entering a save name. When it is False, the user is entering their manager name 
entering_save = True

#The "new_save_name" string is the product of this screen when "entering_save" is True
new_save_name = ''

team_selection_index = 0
current_team_selection = teams_in_league[team_selection_index]

def load_ts_bg(tn) :
	path = ''.join(['C:\\Users\\rhyde23\\Desktop\\Project\\Images\\', tn, '_Selection.png'])
	if pi :
		path = convert_path(path)
	return pygame.image.load(path).convert()
	
current_ts_background = load_ts_bg(current_team_selection)

shortened_version_til = {
	'Arsenal':'Arsenal',
	'Aston Villa':'Villa',
	'Brighton & Hove Albion':'Brighton',
	'Burnley':'Burnley',
	'Chelsea':'Chelsea',
	'Crystal Palace':'Palace',
	'Everton':'Everton',
	'Fulham':'Fulham',
	'Leeds United':'Leeds',
	'Leicester City':'Leicester',
	'Liverpool':'Liverpool',
	'Manchester City':'Man City',
	'Manchester United':'Man United',
	'Newcastle United':'Newcastle',
	'Sheffield United':'Sheffield',
	'Southampton':'Southampton',
	'Tottenham Hotspur':'Spurs',
	'West Bromwich Albion':'West Brom',
	'West Ham United':'West Ham',
	'Wolverhampton Wanderers':'Wolves'
}

ts_next_page_button = [700, 550, 50, 30, white, red, myfont.render(">>", True, red), myfont.render(">>", True, white)]
ts_next_page_button = ts_next_page_button + [ts_next_page_button[-2].get_width(), ts_next_page_button[-2].get_height()]

ts_last_page_button = [430, 550, 50, 30, white, red, myfont.render("<<", True, red), myfont.render("<<", True, white)]
ts_last_page_button = ts_last_page_button + [ts_last_page_button[-2].get_width(), ts_last_page_button[-2].get_height()]

ts_select_button = [500, 550, 180, 30, white, red, myfont.render("Select "+shortened_version_til[current_team_selection], True, red), myfont.render("Select "+shortened_version_til[current_team_selection], True, white)]
ts_select_button = ts_select_button + [ts_select_button[-2].get_width(), ts_select_button[-2].get_height()]

final_team_selection = ''

main_loop = True
saves_menu = True
name_save = False
select_team = False

while main_loop :
	while select_team :
		display.fill(white)
		display.blit(current_ts_background, (0, 0))
		x, y = pygame.mouse.get_pos()
		over_ts_next_page_button = display_button(ts_next_page_button, (x, y))
		over_ts_last_page_button = display_button(ts_last_page_button, (x, y))
		over_ts_select_button = display_button(ts_select_button, (x, y))
		for event in pygame.event.get() :
			if event.type == pygame.MOUSEBUTTONDOWN :
				if over_ts_next_page_button :
					team_selection_index += 1
					if team_selection_index == 20 :
						team_selection_index = 0
					current_team_selection = teams_in_league[team_selection_index]
					current_ts_background = load_ts_bg(current_team_selection)
					ts_select_button = [500, 550, 180, 30, white, red, myfont.render("Select "+shortened_version_til[current_team_selection], True, red), myfont.render("Select "+shortened_version_til[current_team_selection], True, white)]
					ts_select_button = ts_select_button + [ts_select_button[-2].get_width(), ts_select_button[-2].get_height()]
				elif over_ts_last_page_button :
					team_selection_index -= 1
					if team_selection_index == -1 :
						team_selection_index = 19
					current_team_selection = teams_in_league[team_selection_index]
					current_ts_background = load_ts_bg(current_team_selection)
					ts_select_button = [500, 550, 180, 30, white, red, myfont.render("Select "+shortened_version_til[current_team_selection], True, red), myfont.render("Select "+shortened_version_til[current_team_selection], True, white)]
					ts_select_button = ts_select_button + [ts_select_button[-2].get_width(), ts_select_button[-2].get_height()]
				elif over_ts_select_button :
					final_team_selection = current_team_selection
					
					current_data = {
						'TeamName':'',
						'ManagerName':'Reggie Hyde',
						'CurrentLineup':[],
						'CurrentFormation':'',
						'CurrentTeamRating':0,
						'CurrentBudget':100000000,
						'CurrentTeamOverall':79,
						'CurrentDate':'September 1 2021',
						'CurrentEmails':[['Welcome to Arsenal, Manager Hyde. Here is your email inbox where you will receive important messages. Be sure to check your email to stay updated on the Premier League.', 'urmom', '6/1/2020']],
						'UnreadEmails':0,
						'CurrentStandings':{team_name_for_standings:0 for team_name_for_standings in teams_in_league},
						'CurrentStandingsInOrder':teams_in_league,
						'StandingsData':{},
						'TopScorers':{},
						'TopScorersInOrder':[],
						'TopAssistors':{},
						'TopAssistorsInOrder':[],
						'Arsenal_Players':{},
						'Arsenal_Formation':'4-2-3-1 (Wide)',
						'Aston Villa_Players':{},
						'Aston Villa_Formation':'4-2-3-1 (Wide)',
						'Brighton & Hove Albion_Players':{},
						'Brighton & Hove Albion_Formation':'5-3-2 (Attacking)',
						'Burnley_Players':{},
						'Burnley_Formation':'4-4-2 (Flat)',
						'Chelsea_Players':{},
						'Chelsea_Formation':'5-2-3 (Flat)',
						'Crystal Palace_Players':{},
						'Crystal Palace_Formation':'4-3-3 (Defensive)',
						'Everton_Players':{},
						'Everton_Formation':'4-2-3-1 (Wide)',
						'Fulham_Players':{},
						'Fulham_Formation':'4-2-3-1 (Wide)',
						'Leeds United_Players':{},
						'Leeds United_Formation':'4-5-1 (Defensive)',
						'Leicester City_Players':{},
						'Leicester City_Formation':'5-3-2 (Attacking)',
						'Liverpool_Players':{},
						'Liverpool_Formation':'4-3-3 (False 9)',
						'Manchester City_Players':{},
						'Manchester City_Formation':'4-3-3 (Defensive)',
						'Manchester United_Players':{},
						'Manchester United_Formation':'4-2-3-1 (Wide)',
						'Newcastle United_Players':{},
						'Newcastle United_Formation':'5-3-2 (Flat)',
						'Sheffield United_Players':{},
						'Sheffield United_Formation':'5-3-2 (Flat)',
						'Southampton_Players':{},
						'Southampton_Formation':'4-4-2 (Flat)',
						'Tottenham Hotspur_Players':{},
						'Tottenham Hotspur_Formation':'4-2-3-1 (Wide)',
						'West Bromwich Albion_Players':{},
						'West Bromwich Albion_Formation':'4-5-1 (Defensive)',
						'West Ham United_Players':{},
						'West Ham United_Formation':'4-2-3-1 (Wide)',
						'Wolverhampton Wanderers_Players':{},
						'Wolverhampton Wanderers_Formation':'5-2-3 (Flat)',
						'Arsenal_Lineup': ['Bernd Leno', 'Héctor Bellerín', 'David Luiz', 'Gabriel', 'Kieran Tierney', 'Thomas Partey', 'Granit Xhaka', 'Bukayo Saka', 'Gabriel Martinelli', 'Martin Ødegaard', 'Alexandre Lacazette'],
						'Aston Villa_Lineup': ['Emiliano Martínez', 'Matty Cash', 'Ezri Konsa', 'Tyrone Mings', 'Matt Targett', 'Douglas Luiz', 'John McGinn', 'Bertrand Traoré', 'Anwar El Ghazi', 'Jack Grealish', 'Ollie Watkins'],
						'Brighton & Hove Albion_Lineup': ['Robert Sanchéz', 'Joël Veltman', 'Ben White', 'Lewis Dunk', 'Adam Webster', 'Dan Burn', 'Pascal Groß', 'Yves Bissouma', 'Leandro Trossard', 'Neal Maupay', 'Danny Welbeck'],
						'Burnley_Lineup': ['Nick Pope', 'Matthew Lowton', 'James Tarkowski', 'Ben Mee', 'Charlie Taylor', 'Jóhann Berg Guðmundsson', 'Ashley Westwood', 'Josh Brownhill', 'Dwight McNeil', 'Chris Wood', 'Matěj Vydra'],
						'Chelsea_Lineup': ['Édouard Mendy', 'Reece James', 'Azpilicueta', 'Thiago Silva', 'Antonio Rüdiger', 'Ben Chilwell', "N'Golo Kanté", 'Jorginho', 'Mason Mount', 'Timo Werner', 'Christian Pulisic'],
						'Crystal Palace_Lineup': ['Guaita', 'Joel Ward', 'Cheikhou Kouyaté', 'Gary Cahill', 'Patrick van Aanholt', 'Luka Milivojević', 'Eberechi Eze', 'Jaïro Riedewald', 'Andros Townsend', 'Christian Benteke', 'Wilfried Zaha'],
						'Everton_Lineup': ['Jordan Pickford', 'Séamus Coleman', 'Yerry Mina', 'Michael Keane', 'Lucas Digne', 'Abdoulaye Doucouré', 'Allan', 'James Rodríguez', 'Richarlison', 'Gylfi Sigurðsson', 'Dominic Calvert-Lewin'],
						'Fulham_Lineup': ['Alphonse Areola', 'Kenny Tete', 'Joachim Andersen', 'Tosin Adarabioyo', 'Ola Aina', 'Mario Lemina', 'André-Franck Zambo Anguissa', 'Bobby Decordova-Reid', 'Ademola Lookman', 'Ruben Loftus-Cheek', 'Ivan Cavaleiro'],
						'Leeds United_Lineup': ['Illan Meslier', 'Luke Ayling', 'Diego Llorente', 'Liam Cooper', 'Ezgjan Alioski', 'Kalvin Phillips', 'Raphinha', 'Stuart Dallas', 'Tyler Roberts', 'Jack Harrison', 'Patrick Bamford'],
						'Leicester City_Lineup': ['Kasper Schmeichel', 'Ricardo Pereira', 'Wesley Fofana', 'Jonny Evans', 'Çağlar Söyüncü', 'Timothy Castagne', 'Youri Tielemans', 'Wilfred Ndidi', 'James Maddison', 'Kelechi Iheanacho', 'Jamie Vardy'],
						'Liverpool_Lineup': ['Alisson', 'Trent Alexander-Arnold', 'Nathaniel Phillips', 'Ozan Kabak', 'Andrew Robertson', 'Fabinho', 'Thiago', 'Georginio Wijnaldum', 'Roberto Firmino', 'Mohamed Salah', 'Sadio Mané'],
						'Manchester City_Lineup': ['Ederson', 'João Cancelo', 'John Stones', 'Rúben Dias', 'Oleksandr Zinchenko', 'Rodri', 'Kevin De Bruyne', 'İlkay Gündoğan', 'Riyad Mahrez', 'Gabriel Jesus', 'Phil Foden'],
						'Manchester United_Lineup': ['Dean Henderson', 'Aaron Wan-Bissaka', 'Victor Lindelöf', 'Harry Maguire', 'Luke Shaw', 'Scott McTominay', 'Fred', 'Mason Greenwood', 'Marcus Rashford', 'Bruno Fernandes', 'Edinson Cavani'],
						'Newcastle United_Lineup': ['Martin Dúbravka', 'Jacob Murphy', 'Federico Fernández', 'Jamaal Lascelles', 'Paul Dummett', 'Matt Ritchie', 'Miguel Almirón', 'Isaac Hayden', 'Jonjo Shelvey', 'Allan Saint-Maximin', 'Joelinton'],
						'Sheffield United_Lineup': ['Aaron Ramsdale', 'George Baldock', 'Chris Basham', 'John Egan', 'Kean Bryan', 'Enda Stevens', 'Sander Berge', 'Oliver Norwood', 'John Fleck', 'Oliver Burke', 'David McGoldrick'],
						'Southampton_Lineup': ['Alex McCarthy', 'Kyle Walker-Peters', 'Jan Bednarek', 'Jannik Vestergaard', 'Ryan Bertrand', 'Stuart Armstrong', 'James Ward-Prowse', 'Oriol Romeu', 'Moussa Djenepo', 'Danny Ings', 'Ché Adams'],
						'Tottenham Hotspur_Lineup': ['Hugo Lloris', 'Serge Aurier', 'Toby Alderweireld', 'Eric Dier', 'Reguilón', 'Giovani Lo Celso', 'Pierre-Emile Højbjerg', 'Gareth Bale', 'Heung Min Son', 'Dele Alli', 'Harry Kane'],
						'West Bromwich Albion_Lineup': ['Sam Johnstone', 'Darnell Furlong', 'Semi Ajayi', 'Kyle Bartley', 'Conor Townsend', 'Okay Yokuşlu', 'Matheus Pereira', 'Conor Gallagher', 'Ainsley Maitland-Niles', 'Matt Phillips', 'Mbaye Diagne'],
						'West Ham United_Lineup': ['Łukasz Fabiański', 'Vladimír Coufal', 'Craig Dawson', 'Angelo Ogbonna', 'Aaron Cresswell', 'Tomáš Souček', 'Declan Rice', 'Pablo Fornals', 'Saïd Benrahma', 'Jesse Lingard', 'Michail Antonio'],
						'Wolverhampton Wanderers_Lineup': ['Rui Patrício', 'Nélson Semedo', 'Willy Boly', 'Conor Coady', 'Romain Saïss', 'Rayan Aït Nouri', 'Rúben Neves', 'João Moutinho', 'Adama Traoré', 'Fábio Silva', 'Pedro Neto'],
					}

					test_for_game = final_team_selection
					current_data['TeamName'] = test_for_game
					current_data['CurrentLineup'] = current_data[test_for_game+'_Lineup']
					current_data['CurrentFormation'] = current_data[test_for_game+'_Formation']
					current_data['ManagerName'] = new_manager_name
					
					for t in teams_in_league :
						if pi :
							team_path = convert_path('C:\\Users\\rhyde23\\Desktop\\Project\\Team Database\\'+t+'.dat')
						else :
							team_path = 'C:\\Users\\rhyde23\\Desktop\\Project\\Team Database\\'+t+'.dat'
						key = t+'_Players'
						current_data[key] = pickle.load(open(team_path, 'rb'))
						current_data['StandingsData'][t] = [0, 0, 0, 0, 0, 0, 0, 0]
					
					file_path = ''.join(['C:\\Users\\rhyde23\\Desktop\\SoccerManager\\Saves', '\\File', str(save_number+1), '.dat'])
					if pi :
						file_path = convert_path(file_path)
					output_file = open(file_path, 'wb')
					
					pickle.dump(current_data, output_file)
					
					basic_info_dictionary = {
						'SaveName':new_save_name,
						'Opened':True,
					}
					
					file_path = ''.join(['C:\\Users\\rhyde23\\Desktop\\SoccerManager\\Saves', '\\File', str(save_number+1), 'BasicInfo.dat'])
					if pi :
						file_path = convert_path(file_path)
					output_file = open(file_path, 'wb')
					
					pickle.dump(basic_info_dictionary, output_file)
					
					file_path = ''.join(['C:\\Users\\rhyde23\\Desktop\\SoccerManager\\Saves', '\\ThrowawayFile.dat'])
					if pi :
						file_path = convert_path(file_path)
					output_file = open(file_path, 'wb')
					pickle.dump({}, output_file)
					
					game.game(save_number+1)
		pygame.display.update()
	while saves_menu :
		display.fill(white)
		display.blit(current_save_image, (0, 0))
		display.set_at(current_clicked, red)
		x, y = pygame.mouse.get_pos()
		for event in pygame.event.get() :
			if event.type == pygame.MOUSEBUTTONDOWN :
				coords = pygame.mouse.get_pos()
				if clicker_mode :
					current_clicked = coords
				save_selected = save_number
				if save_number in not_empty_saves :
					game.game(save_number+1)
				else :
					saves_menu = False
					name_save = True
				
		
		for i, save_name_text in enumerate(save_names_texts) :
			text_y = buttons[i][0]+offset[i]
			display.blit(save_name_text, (100, text_y))
			
		if x >= x_start and x <= x_end :
			for i, button in enumerate(buttons) :
				if y >= button[0] and y <= button[1] :
					save_number = i
					current_save_image = save_background_images[save_number]
		pygame.display.update()
		
		
	while name_save :
		display.fill(white)
		display.blit(current_typed_screen, (0, 0))
		x, y = pygame.mouse.get_pos()
		for event in pygame.event.get() :
			if event.type == pygame.MOUSEBUTTONDOWN :
				coords = pygame.mouse.get_pos()
				if over_submit :
					if entering_save :
						new_save_name = current_typed
						current_typed = ""
						current_typed_text = myfont2.render(current_typed, True, light_blue)
						current_typed_x = get_x_value(current_typed_text.get_width())
						current_typed_screen = default_typed_screen

						space_bar_down = False

						enter_extension_string = "your Manager"
						string2 = "manager"

						name_save_header = myfont2.render("Enter a Name for "+enter_extension_string, True, light_blue)
						name_save_header_x = get_x_value(name_save_header.get_width())

						too_many_chars = False

						enter_or_submit = True
						over_submit = False

						entering_save = False
					else :
						new_manager_name = current_typed
						name_save = False
						select_team = True
			if event.type == pygame.KEYDOWN :
				try :
					key = event.key
					if key == pygame.K_SPACE :
						if len(current_typed) < 20 :
							space_bar_down = True
							current_typed += ' '
						else :
							too_many_chars = True
					elif key == pygame.K_BACKSPACE :
						current_typed = current_typed[:-1]
						current_typed_screen = keyboard_order[key]
						too_many_chars = False
					else :
						if len(current_typed) < 20 :
							current_typed_screen = keyboard_order[key]
							current_typed += keyboard_letters[key]
						else :
							too_many_chars = True
					current_typed_text = myfont2.render(current_typed, True, light_blue)
					current_typed_x = get_x_value(current_typed_text.get_width())
				except :
					pass
				if current_typed != '' and enter_or_submit :
					name_save_header = myfont2.render("Click here to submit "+string2+" name", True, light_blue)
					name_save_header_x = get_x_value(name_save_header.get_width())
					enter_or_submit = False
				if current_typed == '' and not enter_or_submit :
					name_save_header = myfont2.render("Enter a Name for "+enter_extension_string, True, light_blue)
					name_save_header_x = get_x_value(name_save_header.get_width())
					enter_or_submit = True
					over_submit = False
			if event.type == pygame.KEYUP :
				if key == pygame.K_SPACE :
					space_bar_down = False
				current_typed_screen = default_typed_screen
		
		if x >= 42 and x <= 745 and y >= 51 and y <= 109 and (not enter_or_submit) and (not over_submit) :
			over_submit = True
			name_save_header = myfont2.render("Click here to submit "+string2+" name", True, gray)
		if over_submit and not (x >= 42 and x <= 745 and y >= 51 and y <= 109) :
			over_submit = False
			name_save_header = myfont2.render("Click here to submit "+string2+" name", True, light_blue)
		if space_bar_down :
			pygame.draw.rect(display, key_color, pygame.Rect(240, 505, 315, 50))
		else :
			pygame.draw.rect(display, white, pygame.Rect(240, 505, 315, 50))
		if over_submit :
			pygame.draw.rect(display, light_blue, pygame.Rect(42, 51, 703, 58))
		else :
			pygame.draw.rect(display, gray, pygame.Rect(42, 51, 703, 58))
		display.blit(name_save_header, (name_save_header_x, 60))
		display.blit(current_typed_text, (current_typed_x, 160))
		if too_many_chars :
			display.blit(too_many_chars_text, (too_many_chars_x, 575))
		pygame.display.update()
