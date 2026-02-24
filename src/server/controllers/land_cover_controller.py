################################################################################
#                                                                              #
#                          land_cover_controller.py                            #
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
from models.land_cover_observation import LandCoverObservation
from controllers.observation_controller import ObservationController

class LandCoverController(ObservationController):

	#
	# getting methods
	#

	@staticmethod
	def get_all(db: object, options: object):

		# create query
		#
		table = LandCoverObservation().table
		query = 'SELECT ' + ','.join(Observation.fields) + ' FROM ' + table

		# add filters
		#
		if 'countries' in options and options['countries'] is not None:
			return [];
		if 'after' in options or 'before' in options:
			query = ObservationController.add_date_filter(query, 'phenomenonTime', options['after'], options['before'])
		if 'genera' in options and options['genera'] is not None:
			return []
		if 'species' in options and options['species'] is not None:
			return []

		# get data
		#
		observations = []
		data = ObservationController.get_all(db, query)
		for item in data:
			observations.append(Observation.to_values(item))
		return observations

	@staticmethod
	def get_index(db: object, id: str):

		# create query
		#
		table = LandCoverObservation().table
		query = 'SELECT ' + ','.join(LandCoverObservation.fields) + ' FROM ' + table + " WHERE id = " + str(id);

		# get data
		#
		data = ObservationController.get_one(db, query)
		return LandCoverObservation.to_values(data)

	@staticmethod
	def get_num(db: object, options: object):

		# create query
		#
		table = LandCoverObservation().table
		query = 'SELECT COUNT(*) FROM ' + table;

		# add filters
		#
		if 'after' in options or 'before' in options:
			query = ObservationController.add_date_filter(query, 'phenomenonTime', options['after'], options['before'])
		if 'genera' in options and options['genera'] is not None:
			return []
		if 'species' in options and options['species'] is not None:
			return []

		# get value
		#
		return ObservationController.get_value(db, query)
