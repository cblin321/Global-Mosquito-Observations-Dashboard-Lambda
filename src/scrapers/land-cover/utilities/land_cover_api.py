################################################################################
#                                                                              #
#                              land_cover_api.py                               #
#                                                                              #
################################################################################
#                                                                              #
#        This is a script for interfacing with the Land Cover API.             #
#                                                                              #
#        Author(s): Abe Megahed                                                #
#                                                                              #
#        This file is subject to the terms and conditions defined in           #
#        'LICENSE.txt', which is part of this source code distribution.        #
#                                                                              #
################################################################################
#        Copyright (C) 2025 - Global Mosquito Observations Dashboard           #
################################################################################

import requests
import json
import sys
import math

sys.path.insert(0, '../../translators/land-cover') 
from utilities.json_translator import LandCoverTranslator

class LandCoverAPI:

	#
	# static attributes
	#

	api = 'https://api.globe.gov/search/v1/measurement/protocol/measureddate/'
	params = {
		'protocols': 'land_covers',
		'geojson': 'FALSE',
		'sample': 'FALSE'
	}

	#
	# getting methods
	#

	@staticmethod
	def get_url(url, params):

		"""
		Get a url from a base url and a set of query string parameters.

		Args:
			url (string): The base url.
			params (dict): The collection of query string parameters.

		Returns:
			string: The url.
		"""

		query_string = ''
		for param in params:
			value = params[param]
			if value != None:
				query_string += ('?' if query_string == '' else '&') + param + '=' + str(value)
		return url + query_string

	#
	# counting methods
	#

	@staticmethod
	def num_observations(start_date, end_date):

		"""
		Fetch number of observations within a date range.

		Args:
			api: The api to fetch data from
			start_date: The start of the date range.
			end_date: The end of the date range.

		Returns:
			integer: The number of observations.
		"""

		# make request
		#
		response = requests.get(LandCoverAPI.get_url(LandCoverAPI.api, LandCoverAPI.params | {
			'startdate': start_date,
			'enddate': end_date
		}))

		# check for a response
		#
		if response is None:
			print("No results returned from API.")
			return 0

		# parse response
		#
		results = json.loads(response.text)

		# parse observations
		#
		observations = results['results'] if 'results' in results else []

		# count observations
		#
		return len(observations) if observations else 0

	#
	# fetching methods
	#

	@staticmethod
	def fetch_data(start_date, end_date):

		"""
		Fetch data within a date range.

		Args:
			api: The api to fetch data from
			start_date: The start of the date range.
			end_date: The end of the date range.

		Returns:
			array: The data fetched from the api.
		"""

		# make request
		#
		response = requests.get(LandCoverAPI.get_url(LandCoverAPI.api, LandCoverAPI.params | {
			'startdate': start_date,
			'enddate': end_date
		}))

		# check for a response
		#
		if response is None:
			print("No results returned from API.")
			return []

		# parse response
		#
		results = json.loads(response.text)

		# parse observations
		#
		observations = results['results'] if 'results' in results else []

		# transform data
		#
		return LandCoverTranslator().translate_observations(observations)