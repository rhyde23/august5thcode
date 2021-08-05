import requests, re, html
from bs4 import BeautifulSoup
from file_path_converter import convert_path
from calculate_player_rating import calculate_player_rating

pi = True

def scrape(link) :
    page = requests.get(link)
    
    soup = html.unescape(str(BeautifulSoup(page.content, 'html.parser')))
    return soup


category_change_names = {'Preferred Positions':'Position', 'Birth Date':'Date of Birth'}

def main(link) :
	soup = scrape(link)
	stats = {}
	player_stats = {}
	stats_collected = 0
	nationality = re.findall('nationality=[0-9]+\" title=\"[^"]+\"', soup)
	nationality = nationality[0][:-1].split('\"')[-1]
	stats['Nation'] = nationality
	collected_team = False
	collecting_ps = False
	subtract_off_of_end = 0
	if 'Traits' in soup :
		subtract_off_of_end += 1
	if 'Specialties' in soup :
		subtract_off_of_end += 1
	
	#print(soup.split('card-header'))
	for section in soup.split('card-header')[2:] :
		for line in section.split('\n') :
			visible_in_line = re.findall('>[^<>]+<', line)
			if len(visible_in_line) > 1 :
				for i, visible_text in enumerate(visible_in_line) :
					while True :
						try :
							c = 0
							if visible_text[0] in ['>', '<', ' '] :
								visible_text = visible_text[1:]
							else :
								c += 1
							if visible_text[-1] in ['>', '<', ' '] :
								visible_text = visible_text[:-1]
							else :
								c += 1
							if c == 2 :
								break
						except :
							break
					visible_in_line[i] = visible_text
				visible_in_line = [element for element in visible_in_line if element != '']
				if len(visible_in_line) == 1 :
					if not collected_team :
						stats['Team'] = visible_in_line[0]
						collected_team = True
					continue
				category = visible_in_line[0]
				if not category in ['Position', 'Kit Number', 'Joined Club', 'Contract Length', 'Player Work Rate', 'Value', 'Wage'] :
					if category in category_change_names :
						category = category_change_names[category]
					if stats_collected == 0 :
						stats['Name'] = category
						stats_collected += 1
					else :
						collecting_index = 1
						if category in ['Height', 'Weight'] :
							collecting_index = 2
						elif category == 'Ball Control' :
							collecting_ps = True 
						if collecting_ps :
							player_stats[category] = int(visible_in_line[collecting_index])
						else :
							stats[category] = visible_in_line[collecting_index]
						stats_collected += 1
	stats['Goals'] = 0
	stats['Assists'] = 0
	stats['Freshness'] = 0.5
	positions_to_compute = ['CAM', 'CB', 'CDM', 'CF', 'CM', 'GK', 'LB', 'LM', 'LW', 'LWB', 'RB', 'RM', 'RW', 'RWB', 'ST']
	positions_to_compute.remove(stats['Position'])
	real_position_rating = calculate_player_rating(player_stats, stats['Position'], stats['Position'])
	stats['Rating'] = str(real_position_rating)
	ratings_positions = {stats['Position']:real_position_rating}
	for position_to_compute in positions_to_compute :
		ratings_positions[position_to_compute] = calculate_player_rating(player_stats, position_to_compute, stats['Position'], real_position_rating=real_position_rating)
	stats['Player Stats'] = player_stats
	stats['Positions'] = ratings_positions
	return stats

"""
link = 'https://www.fifaindex.com/player/192985/kevin-de-bruyne/'
result = main(link) 
for key in result :
	print(key, result[key])
"""
