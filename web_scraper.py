#Web Scraper

import requests, re, pickle, html
from bs4 import BeautifulSoup
from scrape_player_page import main

from file_path_converter import convert_path

pi = True

def scrape(link) :
    page = requests.get(link)
    
    soup = html.unescape(str(BeautifulSoup(page.content, 'html.parser')))
    return soup

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

team_fifaindex_indexes = {}

"""
league_page = scrape('https://www.fifaindex.com/teams/?league=13')

remove_parts = ['&']

for team_in_league in teams_in_league :
    link_name = [part for part in team_in_league.lower().split(' ') if not part in remove_parts]
    team_fifaindex_indexes[team_in_league] = re.findall('\"/team/[0-9]+/'+'-'.join(link_name)+'/\"', league_page)[0].split('/')[2]


print(team_fifaindex_indexes)
"""



team_fifaindex_indexes = {'Arsenal': '1', 'Aston Villa': '2', 'Brighton & Hove Albion': '1808', 'Burnley': '1796', 'Chelsea': '5', 'Crystal Palace': '1799', 'Everton': '7', 'Fulham': '144', 'Leeds United': '8', 'Leicester City': '95', 'Liverpool': '9', 'Manchester City': '10', 'Manchester United': '11', 'Newcastle United': '13', 'Sheffield United': '1794', 'Southampton': '17', 'Tottenham Hotspur': '18', 'West Bromwich Albion': '109', 'West Ham United': '19', 'Wolverhampton Wanderers': '110'}

for team_in_league in teams_in_league :
    link = 'https://www.fifaindex.com/team/'+team_fifaindex_indexes[team_in_league]+'/'
    soup = scrape(link)
    
    
    player_links = ['https://www.fifaindex.com'+li[6:]+'/' for li in list(set(re.findall('href=\"/player/[0-9]+', soup)))]
    final_dict = {}
    for player_link in player_links :
        player_data = main(player_link)
        if player_data['Team'] == team_in_league :
            final_dict[player_data['Name']] = player_data
    file_path = ''.join(['C:\\Users\\rhyde23\\Desktop\\Project\\Team Database\\', team_in_league, '.dat'])
    if pi :
        file_path = convert_path(file_path)
    output_file = open(file_path, 'wb')
    pickle.dump(final_dict, output_file)
    
    starting_lineup_findings = [finding[7:][:-9] for finding in re.findall('title=\"[^""]+\"', soup) if finding[-8:] == 'FIFA 21\"']
    starting_lineup = []
    for starting_lineup_finding in starting_lineup_findings :
        if starting_lineup_finding in final_dict and not starting_lineup_finding in starting_lineup :
            starting_lineup.append(starting_lineup_finding)
        if len(starting_lineup) == 11 :
            break 
    print("\'"+team_in_league+"_Lineup\':", starting_lineup)

"""
final_dict = main()
for team in final_dict :
    file_path = ''.join(['C:\\Users\\rhyde23\\Desktop\\Project\\Team Database\\', team, '.dat'])
    if pi :
        file_path = convert_path(file_path)
    output_file = open(file_path, 'wb')
    pickle.dump(final_dict[team], output_file)
    print(team)
    for player in final_dict[team] :
        print(final_dict[team][player])
    print()
    print()
    print()



file_path = ''.join(['C:\\Users\\rhyde23\\Desktop\\Project\\Team Database', '\\ThrowawayFile.dat'])
if pi :
    file_path = convert_path(file_path)
output_file = open(file_path, 'wb')
pickle.dump({}, output_file)

print('Done')
"""

    
    
    
