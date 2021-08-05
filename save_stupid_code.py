
"""
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
def rearrange_lineup_formation_change(new_formation, new_positions) :
    best_options_each_pos = {}
    final_new, used = {}, []
    while True :
        f = False
        for new_position in new_positions :
            converted_pos = convert_outside_position_to_center(new_position)
            if converted_pos in ['RB', 'RWB'] :
                converted_pos_array = ['RB', 'RWB']
            elif converted_pos in ['LB', 'LWB'] :
                converted_pos_array = ['LB', 'LWB']
            else :
                converted_pos_array = [converted_pos]
            best_options = [option for option in get_best_players_in_given_position(team, converted_pos) if option in current_data['CurrentLineup'] and not option in used]
            if current_data[team+'_Players'][best_options[0]]['Position'] in converted_pos_array :
                best_options_each_pos = {}
                final_new[new_position] = best_options[0]
                used.append(best_options[0])
                new_positions.remove(new_position)
                f = True
                break
            else :
                best_options_each_pos[new_position] = best_options
        if not f :
            break
    
    print(len(final_new))
    if len(final_new) != 11 :
        left_positions_order = list(best_options_each_pos.keys())
        left_players = best_options_each_pos[left_positions_order[0]]
        if len(final_new) == 10 :
            final_new[left_positions_order[0]] = left_players[0]
        else :
            for permu_standards in [[1.0, 1.1], [1.0, 1.1, 1.2], [1.0, 1.1, 1.2, 1.3], [1.0, 1.1, 1.2, 1.3, 1.4], [1.0, 1.1, 1.2, 1.3, 1.4, 1.5]] :
                current_lineup_position_ratings = {n:{pos:current_data[team+'_Players'][n]['Positions'][convert_outside_position_to_center(pos)] for pos in left_positions_order} for n in left_players}
                current_lineup_position_percentages = {n:{pos:round((int(current_data[team+'_Players'][n]['Rating'])/current_data[team+'_Players'][n]['Positions'][convert_outside_position_to_center(pos)]), 1) for pos in left_positions_order} for n in left_players}
                number_in_combo = len(left_players)
                permu_arrays = [[] for xyz in range(number_in_combo)]
                for cipp in current_lineup_position_percentages :
                    for cipp_position in current_lineup_position_percentages[cipp] :
                        if current_lineup_position_percentages[cipp][cipp_position] in permu_standards :
                            permu_arrays[left_positions_order.index(cipp_position)].append(cipp)
                    
                if not [] in permu_arrays :
                    failed = False
                    for le in left_players :
                        alright = False
                        for p_a in permu_arrays :
                            if le in p_a :
                                alright = True
                                break
                        if not alright :
                            failed = True
                    if failed :
                        continue
                else :
                    continue
                    
                highest_rating = 0
                all_same_attempts = []
                amount_of_permutations = 0
                combos = [[element] for element in permu_arrays[0]]
                current_permu_index = 1
                while combos != [] :
                    new_combos = []
                    for combo in combos :
                        for element in [element for element in permu_arrays[current_permu_index] if not element in combo] :
                            new_addition = combo+[element]
                            if len(new_addition) == number_in_combo :
                                attempt = determine_rating_of_combo(new_addition, left_positions_order, current_lineup_position_ratings, number_in_combo)
                                if attempt > highest_rating :
                                    highest_rating = attempt
                                    all_same_attempts = [new_addition]
                                if attempt == highest_rating :
                                    all_same_attempts.append(new_addition)
                                amount_of_permutations += 1
                            else :
                                new_combos.append(new_addition)
                    combos = new_combos
                    current_permu_index += 1
                print()
                print('Performance:', amount_of_permutations)
                best, best_r = (), 0
                for a in all_same_attempts :
                    points = get_correct_general_placements(left_positions_order, a)
                    if points >= best_r :
                        best, best_r = a, points
                try :
                    for i in range(number_in_combo)  :
                        final_new[left_positions_order[i]] = best[i]
                    break
                except :
                    pass
    return [final_new[n_pos] for n_pos in get_positions_from_formation(new_formation)]
"""

"""
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
"""


"""
def return_first_text(string) :
    return re.findall('>[^<>]+<', string)[0][1:][:-1]


card_types = ['nifgold', 'nifsilver', 'nifbronze']

replacements = ['\'']


weird_all_ones = {
    'Aaron Mooy':{'CB': 71, 'CDM': 76, 'CM': 76, 'CAM': 76, 'CF': 74, 'ST': 70, 'LW': 74, 'LF': 74, 'RF': 74, 'RW': 74, 'LM': 75, 'RM': 75, 'RB': 72, 'RWB': 74, 'LB': 72, 'LWB': 74},
    'Jordan Archer':{'CB': 32, 'CDM': 34, 'CM': 31, 'CAM': 32, 'CF': 33, 'ST': 34, 'LW': 29, 'LF': 32, 'RF': 32, 'RW': 29, 'LM': 35, 'RM': 35, 'RB': 31, 'RWB': 31, 'LB': 31, 'LWB': 31},
}


def main() :
    final_dict = {
        'Manchester City':{},
        'Manchester United':{},
        'Liverpool':{},
        'Chelsea':{},
        'Leicester City':{},
        'West Ham United':{},
        'Tottenham Hotspur':{},
        'Arsenal':{},
        'Leeds United':{},
        'Everton':{},
        'Aston Villa':{},
        'Newcastle United':{},
        'Wolverhampton Wanderers':{},
        'Crystal Palace':{},
        'Southampton':{},
        'Brighton & Hove Albion':{},
        'Burnley':{},
        'Fulham':{},
        'West Bromwich Albion':{},
        'Sheffield United':{}
    }
    for card_type in card_types :
        x = 0
        while True :
            page_dict = {}
            main_link = "https://www.futwiz.com/en/fifa21/players?page="+str(x)+"&release="+card_type+"&leagues[]=13"
            soup = scrape(main_link)
            player_names_in_order = []
            findings = re.findall('\"[^0-9]+[0-9]{2}\sRated\"', soup)
            if findings == [] :
                break
            for player_string in findings :
                rating = re.findall('[0-9]+', player_string)[0]
                name = player_string.split(rating)[0][12:][:-1]
                for char in name :
                    if char in replacements :
                        name = name.replace(char, '')
                link_version_of_name = '-'.join([s.lower() for s in name.split(' ')])
                link = 'https://www.futwiz.com/'+re.search('a href=\"/en/fifa21/player/'+link_version_of_name+'/[0-9]+\"', soup).group()[8:][:-1]
                player_soup = scrape(link)
                main_info_section = player_soup.split('h1')[1]
                main_info_matches = re.findall('>[^<>]+<', main_info_section)
                nation, team = main_info_matches[3][1:][:-1], main_info_matches[5][1:][:-1]
                if team == 'Brighton &amp; Hove Albion' :
                    team = 'Brighton & Hove Albion'
                chem_section = player_soup.split('mt-10 altpos-pitch mb-20')[1].split('p style')[0]
                chem_section_matches = re.findall('>[^<>]+<', chem_section)
                chem_section_matches = [s[1:][:-1] for s in chem_section_matches if s != '>\n<']
                ratings = chem_section_matches[::2]
                positions = chem_section_matches[1::2]
                chem_dictionary = {}
                for i, pos in enumerate(positions) :
                    chem_dictionary[pos] = int(ratings[i])
                
                if name in weird_all_ones :
                    chem_dictionary = weird_all_ones[name]
                    
                for c in chem_dictionary :
                    if chem_dictionary[c] == 1 :
                        print(name)
                        print(chem_dictionary)
                
                db_splits = player_soup.split('<div class=\"playerprofile-db\">')[3:][:-9]
                age, height, weight = return_first_text(db_splits[0]), return_first_text(db_splits[1]), return_first_text(db_splits[2])
                page_dict[name] = {'Name':name, 'Rating':rating, 'Team':team, 'Nation':nation, 'Positions':chem_dictionary, 'Age':age, 'Height':height, 'Weight':weight, 'Freshness':0.5, 'Goals':0, 'Assists':0}
                player_names_in_order.append(name)
            for i, match in enumerate(re.findall('<div class=\"card-21-pack-position\">[A-Z]+</div>', soup)) :
                try :
                    match = re.findall('>[^<>]+<', match)[0][1:][:-1]
                    page_dict[player_names_in_order[i]]['Position'] = match
                    if match == 'GK' :
                        page_dict[player_names_in_order[i]]['Positions']['GK'] = page_dict[player_names_in_order[i]]['Rating']
                    else :
                        page_dict[player_names_in_order[i]]['Positions']['GK'] = 35
                    if page_dict[player_names_in_order[i]]['Positions'][match] != int(rating) :
                        page_dict[player_names_in_order[i]]['Positions'][match] = int(rating)
                    for km in page_dict[player_names_in_order[i]]['Positions'] :
                        if page_dict[player_names_in_order[i]]['Positions'][km] > int(rating) :
                            page_dict[player_names_in_order[i]]['Positions'][km] = int(rating)
                except :
                    print(player_names_in_order[i], 'broke')
                    break
            for player_key in page_dict :
                player_info = page_dict[player_key]
                team = player_info['Team']
                if not team in final_dict :
                    print(team)
                    quit()
                    
                final_dict[team][player_key] = player_info
            x += 1
            print(x)
            
    return final_dict
"""
