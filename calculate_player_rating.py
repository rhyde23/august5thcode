import re
from file_path_converter import convert_path

pi = True

"""
text_file_path = 'C:\\Users\\rhyde23\\Desktop\\Project\\positionratingstuff.txt'
if pi :
	text_file_path = convert_path(text_file_path)

text_string = open(text_file_path, 'r').read()

divider_string = '__________________________________\n'
final_dict = {}

positions_that_apply = {
	'Goalkeeper': ['GK'], 
	'Centre Back': ['CB'], 
	'Full Back': ['RB', 'LB'], 
	'Wing Back': ['RWB', 'LWB'], 
	'Defensive Midfielder': ['CDM'],
	'Central Midfielder': ['CM'],
	'Attacking Midfielder': ['CAM'],
	'Wide Midfielder': ['RM', 'LM'],
	'Winger': ['RW', 'LW'], 
	'Centre Forward': ['RF', 'LF', 'CF'], 
	'Striker': ['ST']
	
}



for f in re.findall(divider_string+'[^_]+'+divider_string+'[^_]+', text_string) :
	f_splitted = f.split('\n')
	header = f_splitted[1]
	final_dict[header] = {}
	f_splitted = f_splitted[3:][:-1]
	for line in f_splitted :
		stat, value = line.split(':')
		value = int(value)
		for apply_stat in positions_that_apply[stat] :
			final_dict[header][apply_stat] = value
"""





text_file_path = 'C:\\Users\\rhyde23\\Desktop\\Project\\samplepositionratingstuff.txt'
if pi :
	text_file_path = convert_path(text_file_path)

text_string = open(text_file_path, 'r').read()
player_stats = {}

for line in [line for line in text_string.split('\n') if line != ''] :
	try :
		line_splitted = line.split(' ')
		stat, value = ' '.join(line_splitted[:-1]), line_splitted[-1]
		player_stats[stat] = int(value)
	except :
		pass




final_dict = {
	'Crossing': {'GK': 1, 'CB': 1, 'RB': 10, 'LB': 10, 'RWB': 13, 'LWB': 13, 'CDM': 1, 'CM': 1, 'CAM': 1, 'RM': 11, 'LM': 11, 'RW': 10, 'LW': 10, 'RF': 1, 'LF': 1, 'CF': 1, 'ST': 1},
	'Finishing': {'GK': 1, 'CB': 1, 'RB': 1, 'LB': 1, 'RWB': 1, 'LWB': 1, 'CDM': 1, 'CM': 3, 'CAM': 8, 'RM': 7, 'LM': 7, 'RW': 11, 'LW': 11, 'RF': 12, 'LF': 12, 'CF': 12, 'ST': 19}, 
	'Heading': {'GK': 1, 'CB': 11, 'RB': 5, 'LB': 5, 'RWB': 1, 'LWB': 1, 'CDM': 1, 'CM': 1, 'CAM': 1, 'RM': 1, 'LM': 1, 'RW': 1, 'LW': 1, 'RF': 3, 'LF': 3, 'CF': 3, 'ST': 11}, 
	'Short Pass': {'GK': 1, 'CB': 6, 'RB': 8, 'LB': 8, 'RWB': 11, 'LWB': 11, 'CDM': 15, 'CM': 18, 'CAM': 17, 'RM': 12, 'LM': 12, 'RW': 10, 'LW': 10, 'RF': 10, 'LF': 10, 'CF': 10, 'ST': 6}, 
	'Volleys': {'GK': 1, 'CB': 1, 'RB': 1, 'LB': 1, 'RWB': 1, 'LWB': 1, 'CDM': 1, 'CM': 1, 'CAM': 1, 'RM': 1, 'LM': 1, 'RW': 1, 'LW': 1, 'RF': 1, 'LF': 1, 'CF': 1, 'ST': 3}, 
	'Dribbling': {'GK': 1, 'CB': 1, 'RB': 1, 'LB': 1, 'RWB': 5, 'LWB': 5, 'CDM': 1, 'CM': 8, 'CAM': 14, 'RM': 16, 'LM': 16, 'RW': 17, 'LW': 17, 'RF': 15, 'LF': 15, 'CF': 15, 'ST': 8}, 
	'Curve': {'GK': 1, 'CB': 1, 'RB': 1, 'LB': 1, 'RWB': 1, 'LWB': 1, 'CDM': 1, 'CM': 1, 'CAM': 1, 'RM': 1, 'LM': 1, 'RW': 1, 'LW': 1, 'RF': 1, 'LF': 1, 'CF': 1, 'ST': 1}, 
	'FK Acc.': {'GK': 1, 'CB': 1, 'RB': 1, 'LB': 1, 'RWB': 1, 'LWB': 1, 'CDM': 1, 'CM': 1, 'CAM': 1, 'RM': 1, 'LM': 1, 'RW': 1, 'LW': 1, 'RF': 1, 'LF': 1, 'CF': 1, 'ST': 1}, 
	'Long Pass': {'GK': 1, 'CB': 1, 'RB': 1, 'LB': 1, 'RWB': 1, 'LWB': 1, 'CDM': 11, 'CM': 14, 'CAM': 5, 'RM': 6, 'LM': 6, 'RW': 1, 'LW': 1, 'RF': 1, 'LF': 1, 'CF': 1, 'ST': 1}, 
	'Ball Control': {'GK': 1, 'CB': 5, 'RB': 8, 'LB': 8, 'RWB': 9, 'LWB': 9, 'CDM': 11, 'CM': 15, 'CAM': 16, 'RM': 14, 'LM': 14, 'RW': 15, 'LW': 15, 'RF': 16, 'LF': 16, 'CF': 16, 'ST': 11}, 
	'Acceleration': {'GK': 1, 'CB': 1, 'RB': 6, 'LB': 6, 'RWB': 5, 'LWB': 5, 'CDM': 1, 'CM': 1, 'CAM': 5, 'RM': 8, 'LM': 8, 'RW': 8, 'LW': 8, 'RF': 6, 'LF': 6, 'CF': 6, 'ST': 5}, 
	'Sprint Speed': {'GK': 1, 'CB': 3, 'RB': 8, 'LB': 8, 'RWB': 7, 'LWB': 7, 'CDM': 1, 'CM': 1, 'CAM': 4, 'RM': 7, 'LM': 7, 'RW': 7, 'LW': 7, 'RF': 6, 'LF': 6, 'CF': 6, 'ST': 6}, 
	'Agility': {'GK': 1, 'CB': 1, 'RB': 1, 'LB': 1, 'RWB': 1, 'LWB': 1, 'CDM': 1, 'CM': 1, 'CAM': 4, 'RM': 8, 'LM': 8, 'RW': 4, 'LW': 4, 'RF': 1, 'LF': 1, 'CF': 1, 'ST': 1}, 
	'Reactions': {'GK': 12, 'CB': 6, 'RB': 9, 'LB': 9, 'RWB': 9, 'LWB': 9, 'CDM': 8, 'CM': 9, 'CAM': 8, 'RM': 1, 'LM': 1, 'RW': 8, 'LW': 8, 'RF': 10, 'LF': 10, 'CF': 10, 'ST': 9}, 
	'Balance': {'GK': 1, 'CB': 1, 'RB': 1, 'LB': 1, 'RWB': 1, 'LWB': 1, 'CDM': 1, 'CM': 1, 'CAM': 1, 'RM': 1, 'LM': 1, 'RW': 1, 'LW': 1, 'RF': 1, 'LF': 1, 'CF': 1, 'ST': 1}, 
	'Shot Power': {'GK': 1, 'CB': 1, 'RB': 1, 'LB': 1, 'RWB': 1, 'LWB': 1, 'CDM': 1, 'CM': 1, 'CAM': 1, 'RM': 1, 'LM': 1, 'RW': 1, 'LW': 1, 'RF': 6, 'LF': 6, 'CF': 6, 'ST': 11}, 
	'Jumping': {'GK': 1, 'CB': 4, 'RB': 1, 'LB': 1, 'RWB': 1, 'LWB': 1, 'CDM': 1, 'CM': 1, 'CAM': 1, 'RM': 1, 'LM': 1, 'RW': 1, 'LW': 1, 'RF': 1, 'LF': 1, 'CF': 1, 'ST': 1}, 
	'Stamina': {'GK': 1, 'CB': 1, 'RB': 9, 'LB': 9, 'RWB': 11, 'LWB': 11, 'CDM': 7, 'CM': 7, 'CAM': 1, 'RM': 6, 'LM': 6, 'RW': 1, 'LW': 1, 'RF': 1, 'LF': 1, 'CF': 1, 'ST': 1}, 
	'Strength': {'GK': 1, 'CB': 11, 'RB': 1, 'LB': 1, 'RWB': 1, 'LWB': 1, 'CDM': 5, 'CM': 1, 'CAM': 1, 'RM': 1, 'LM': 1, 'RW': 1, 'LW': 1, 'RF': 1, 'LF': 1, 'CF': 1, 'ST': 6}, 
	'Long Shots': {'GK': 1, 'CB': 1, 'RB': 1, 'LB': 1, 'RWB': 1, 'LWB': 1, 'CDM': 1, 'CM': 5, 'CAM': 6, 'RM': 1, 'LM': 1, 'RW': 5, 'LW': 5, 'RF': 5, 'LF': 5, 'CF': 5, 'ST': 4}, 
	'Aggression': {'GK': 1, 'CB': 8, 'RB': 1, 'LB': 1, 'RWB': 1, 'LWB': 1, 'CDM': 6, 'CM': 1, 'CAM': 1, 'RM': 1, 'LM': 1, 'RW': 1, 'LW': 1, 'RF': 1, 'LF': 1, 'CF': 1, 'ST': 1}, 
	'Interceptions': {'GK': 1, 'CB': 14, 'RB': 13, 'LB': 13, 'RWB': 13, 'LWB': 13, 'CDM': 15, 'CM': 6, 'CAM': 1, 'RM': 1, 'LM': 1, 'RW': 1, 'LW': 1, 'RF': 1, 'LF': 1, 'CF': 1, 'ST': 1}, 
	'Vision': {'GK': 1, 'CB': 1, 'RB': 1, 'LB': 1, 'RWB': 1, 'LWB': 1, 'CDM': 5, 'CM': 14, 'CAM': 15, 'RM': 8, 'LM': 8, 'RW': 7, 'LW': 7, 'RF': 9, 'LF': 9, 'CF': 9, 'ST': 1}, 
	'Penalties': {'GK': 1, 'CB': 1, 'RB': 1, 'LB': 1, 'RWB': 1, 'LWB': 1, 'CDM': 1, 'CM': 1, 'CAM': 1, 'RM': 1, 'LM': 1, 'RW': 1, 'LW': 1, 'RF': 1, 'LF': 1, 'CF': 1, 'ST': 1}, 
	'Composure': {'GK': 1, 'CB': 1, 'RB': 1, 'LB': 1, 'RWB': 1, 'LWB': 1, 'CDM': 1, 'CM': 1, 'CAM': 1, 'RM': 1, 'LM': 1, 'RW': 1, 'LW': 1, 'RF': 1, 'LF': 1, 'CF': 1, 'ST': 1}, 
	'Marking': {'GK': 1, 'CB': 15, 'RB': 9, 'LB': 9, 'RWB': 8, 'LWB': 8, 'CDM': 10, 'CM': 1, 'CAM': 1, 'RM': 1, 'LM': 1, 'RW': 1, 'LW': 1, 'RF': 1, 'LF': 1, 'CF': 1, 'ST': 1}, 
	'Stand Tackle': {'GK': 1, 'CB': 18, 'RB': 12, 'LB': 12, 'RWB': 9, 'LWB': 9, 'CDM': 13, 'CM': 6, 'CAM': 1, 'RM': 1, 'LM': 1, 'RW': 1, 'LW': 1, 'RF': 1, 'LF': 1, 'CF': 1, 'ST': 1}, 
	'Slide Tackle': {'GK': 1, 'CB': 11, 'RB': 15, 'LB': 15, 'RWB': 12, 'LWB': 12, 'CDM': 6, 'CM': 1, 'CAM': 1, 'RM': 1, 'LM': 1, 'RW': 1, 'LW': 1, 'RF': 1, 'LF': 1, 'CF': 1, 'ST': 1}, 
	'GK Diving': {'GK': 24, 'CB': 0, 'RB': 0, 'LB': 0, 'RWB': 0, 'LWB': 0, 'CDM': 0, 'CM': 0, 'CAM': 0, 'RM': 0, 'LM': 0, 'RW': 0, 'LW': 0, 'RF': 0, 'LF': 0, 'CF': 0, 'ST': 0}, 
	'GK Handling': {'GK': 24, 'CB': 0, 'RB': 0, 'LB': 0, 'RWB': 0, 'LWB': 0, 'CDM': 0, 'CM': 0, 'CAM': 0, 'RM': 0, 'LM': 0, 'RW': 0, 'LW': 0, 'RF': 0, 'LF': 0, 'CF': 0, 'ST': 0}, 
	'GK Kicking': {'GK': 7, 'CB': 0, 'RB': 0, 'LB': 0, 'RWB': 0, 'LWB': 0, 'CDM': 0, 'CM': 0, 'CAM': 0, 'RM': 0, 'LM': 0, 'RW': 0, 'LW': 0, 'RF': 0, 'LF': 0, 'CF': 0, 'ST': 0}, 
	'GK Positioning': {'GK': 24, 'CB': 0, 'RB': 0, 'LB': 0, 'RWB': 0, 'LWB': 0, 'CDM': 0, 'CM': 0, 'CAM': 0, 'RM': 0, 'LM': 0, 'RW': 0, 'LW': 0, 'RF': 0, 'LF': 0, 'CF': 0, 'ST': 0}, 
	'GK Reflexes': {'GK': 24, 'CB': 0, 'RB': 0, 'LB': 0, 'RWB': 0, 'LWB': 0, 'CDM': 0, 'CM': 0, 'CAM': 0, 'RM': 0, 'LM': 0, 'RW': 0, 'LW': 0, 'RF': 0, 'LF': 0, 'CF': 0, 'ST': 0},
	'Att. Position':{'GK': 1, 'CB': 1, 'RB': 1, 'LB': 1, 'RWB': 1, 'LWB': 1, 'CDM': 1, 'CM': 7, 'CAM': 10, 'RM': 9, 'LM': 9, 'RW': 9, 'LW': 9, 'RF': 14, 'LF': 14, 'CF': 14, 'ST': 14}
}

same_positions = [
	['GK'], 
	['CB'], 
	['RB', 'LB'], 
	['RWB', 'LWB'], 
	['CDM'],
	['CM'],
	['CAM'],
	['RM', 'LM'],
	['RW', 'LW'], 
	['RF', 'LF', 'CF'], 
	['ST']
]

def calculate_player_rating(player_stats, position, real_position, real_position_rating=None) :
	rating = 0
	for stat_name in player_stats :
		add_to_rating = final_dict[stat_name][position]*(player_stats[stat_name]/100)
		rating += add_to_rating
	rating = int(rating*0.8)
	found = False
	for s_p in same_positions :
		if position in s_p :
			if real_position in s_p :
				rating += 2
				found = True 
				break
	if not found :
		difference = real_position_rating-rating
		if difference <= 5 :
			pass
		elif difference > 5 and difference < 10 :
			rating -= 1
		elif difference >= 10 and difference < 15 :
			rating -= 2
		else :
			rating -= 3
	return rating

#print(calculate_player_rating(player_stats, 'GK', 'GK', real_position_rating=None))
