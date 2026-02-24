################################################################################
#                                                                              #
#                            mosquito_alert_api.py                             #
#                                                                              #
################################################################################
#                                                                              #
#        This is a script for interfacing with the Mosquito Alert API.         #
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

sys.path.insert(0, '../../translators/mosquito-alert') 
from utilities.json_translator import MosquitoAlertTranslator

class MosquitoAlertAPI:

	#
	# static attributes
	#

	api = 'https://api.mosquitoalert.com/v1'
	page_size = 100

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
		response = requests.get(MosquitoAlertAPI.get_url(MosquitoAlertAPI.api + '/observations', {
			'updated_at_after': start_date,
			'updated_at_before': end_date,
			'page': 1,
			'page_size': 1
		}))

		# check for a response
		#
		if response is None:
			print("No results returned from API.")
			return 0

		# parse response
		#
		json_data = json.loads(response.text)
		return json_data['count'] if json_data and 'count' in json_data else 0

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
			page: The starting page to fetch.

		Returns:
			array: The data fetched from the api.
		"""

		data = []
		num_observations = MosquitoAlertAPI.num_observations(start_date, end_date)
		num_pages = math.ceil(num_observations / MosquitoAlertAPI.page_size)
		print("# of observations =", num_observations)

		for page in range(1, num_pages + 1):

			url = MosquitoAlertAPI.get_url(MosquitoAlertAPI.api + '/observations', {
				'updated_at_after': start_date,
				'updated_at_before': end_date,
				'page': page,
				'page_size': MosquitoAlertAPI.page_size
			})

			# make request
			#
			print("Fetching page", page, '/', num_pages)
			response = requests.get(url)

			# check for a response
			#
			if response is None:
				print("No results returned from API.")

			# parse response
			#
			if response is not None:
				json_data = json.loads(response.text)
				if 'results' in json_data:
					results = json_data['results']

					# transform data
					#
					values = MosquitoAlertTranslator().translate_observations(results)
					for value in values:
						data.append(value)

		return data