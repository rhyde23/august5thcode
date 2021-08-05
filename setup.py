import cx_Freeze
from os import listdir

executables = [cx_Freeze.Executable('game_launcher.py')]

imports = """
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
"""

all_imports = list(set([imp.split(' ')[1]+'.py' for imp in imports.split('\n')[1:][:-1]]))+['game.py']

for extension in ['Team Database', 'Saves', 'Images'] :
	
	all_imports = all_imports+[extension+'/'+element for element in listdir('/home/pi/Desktop/Project/'+extension)]

cx_Freeze.setup(
	name='ESG Beta 1.0',
	options={'build_exe':{'packages':['pygame', 'pickle', 'random', 'itertools', 'time', 'os'], 'include_files':all_imports}},
	executables=executables
	)
