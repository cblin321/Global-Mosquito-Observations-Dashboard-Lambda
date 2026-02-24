################################################################################
#                                                                              #
#                               scrape_github.py                               #
#                                                                              #
################################################################################
#                                                                              #
#        This is a script for scraping from the Habitat Mapper GitHub.         #
#                                                                              #
#        Author(s): Abe Megahed                                                #
#                                                                              #
#        This file is subject to the terms and conditions defined in           #
#        'LICENSE.txt', which is part of this source code distribution.        #
#                                                                              #
################################################################################
#        Copyright (C) 2025 - Global Mosquito Observations Dashboard           #
################################################################################

import sys
import json
import csv
import requests

sys.path.insert(0, '../../translators/habitat-mapper')
from csv_translator import Translator

#
# globals
#

translator = Translator()
api = 'https://raw.githubusercontent.com/Piphi5/GLOBE-Clean-Datasets/refs/heads/main/General/Clean_MHM.csv'

#
# utility functions
#

def read_observations_from_lines(lines):

	"""
	Convert csv row data to an array of objects.

	Args:
		lines: The lines to convert.

	Returns:
		array: The array of objects.
	"""

	observations = []
	reader = csv.reader(lines)
	index = 0
	columns = []
	for row in reader:
		index += 1
		if index == 1:
			columns = row
		else:
			values = {}
			for i in range(0, len(row)):
				values[columns[i]] = row[i]
			observations.append(values)
	return observations

#
# functions
#

def fetch_data(api):

	"""
	Fetch data from an api.

	Args:
		api: The api to use.

	Returns:
		array: The array of observations.
	"""

	response = requests.get(api)
	results = response.text.splitlines()

	# parse observations
	#
	observations = read_observations_from_lines(results)

	# transform data
	#
	return translator.get_observations_values(observations)

################################################################################
#                                     main                                     #
################################################################################

if __name__ == '__main__':
	values = fetch_data(api)
	print(values)
	