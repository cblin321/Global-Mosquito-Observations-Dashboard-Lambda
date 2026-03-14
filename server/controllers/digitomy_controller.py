################################################################################
#                                                                              #
#                            digitomy_controller.py                            #
#                                                                              #
################################################################################
#                                                                              #
#        This controller is used to handle requests for observation info.      #
#                                                                              #
#        Author(s): Abe Megahed                                                #
#                                                                              #
################################################################################
#     Copyright (C) 2025, Data Science Institute, University of Wisconsin      #
################################################################################

from models.observation import Observation
from models.digitomy_observation import DigitomyObservation
from controllers.observation_controller import ObservationController
from controllers.country_controller import CountryController

class DigitomyController(ObservationController):

	#
	# getting methods
	#

	@staticmethod
	def get_all(db: object, options: object):
		
		# create query
		#
		table = DigitomyObservation().table
		query = 'SELECT ' + ','.join(Observation.fields) + ' FROM ' + table

		# add filters
		#
		if 'after' in options or 'before' in options:
			query = ObservationController.add_date_filter(query, 'captured_at', options['after'], options['before'])
		if 'genera' in options and options['genera'] is not None:
			return []
		if 'species' in options and options['species'] is not None:
			return []

		# get data
		#
		observations = []
		data = ObservationController.get_all(db, query)
		if data != 'Could not connect to database':
			for item in data:
				observations.append(DigitomyObservation.to_values(item))
		return observations

	@staticmethod
	def get_index(db: object, id: str):

		# create query
		#
		table = DigitomyObservation().table
		query = 'SELECT ' + ','.join(DigitomyObservation.fields) + ' FROM ' + table + " WHERE id = '" + str(id) + "'";

		# get data
		#
		data = ObservationController.get_one(db, query)
		return DigitomyObservation.to_all_values(data)

	@staticmethod
	def get_num(db: object, options: object):

		# create query
		#
		table = DigitomyObservation().table
		query = 'SELECT COUNT(*) FROM ' + table;

		# add filters
		#
		if 'after' in options or 'before' in options:
			query = ObservationController.add_date_filter(query, 'captured_at', options['after'], options['before'])
		if 'genera' in options and options['genera'] is not None:
			return []
		if 'species' in options and options['species'] is not None:
			return []

		# get value
		#
		return ObservationController.get_value(db, query)
