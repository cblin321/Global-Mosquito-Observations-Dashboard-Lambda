################################################################################
#                                                                              #
#                        mosquito_alert_controller.py                          #
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
from models.mosquito_alert_observation import MosquitoAlertObservation
from controllers.observation_controller import ObservationController
from controllers.inaturalist_controller import iNaturalistController
from controllers.country_controller import CountryController

class MosquitoAlertController(ObservationController):

	#
	# getting methods
	#

	@staticmethod
	def get_all(db: object, options: object):

		# create query
		#
		table = MosquitoAlertObservation().table
		query = 'SELECT ' + ','.join(Observation.fields) + ' FROM ' + table

		# add filters
		#
		if 'countries' in options and options['countries'] is not None:
			query = ObservationController.add_countries_filter(query, 'locationName', CountryController.get_by_indices(db, options['countries']))
		if 'after' in options or 'before' in options:
			query = ObservationController.add_date_filter(query, 'observationResCatObsPheTime', options['after'], options['before'])
		if 'genera' in options and options['genera'] is not None:
			query = ObservationController.add_genera_filter(query, 'Indentified_by_Human', iNaturalistController.get_genera_by_indices(db, options['genera']))
		if 'species' in options and options['species'] is not None:
			query = ObservationController.add_species_filter(query, 'Indentified_by_Human', iNaturalistController.get_species_by_indices(db, options['species']))

		# get data
		#
		observations = []
		data = ObservationController.get_all(db, query)
		for item in data:
			observations.append(Observation.to_values(item))
		return observations

	@staticmethod
	def get_index(db: object, id: object):

		# create query
		#
		table = MosquitoAlertObservation().table
		query = 'SELECT ' + ','.join(MosquitoAlertObservation.fields) + ' FROM ' + table + " WHERE id = " + str(id);

		# get data
		#
		data = ObservationController.get_one(db, query)
		return MosquitoAlertObservation.to_values(data)

	@staticmethod
	def get_num(db: object, options: object):

		# create query
		#
		table = MosquitoAlertObservation().table
		query = 'SELECT COUNT(*) FROM ' + table;

		# add filters
		#
		if 'after' in options or 'before' in options:
			query = ObservationController.add_date_filter(query, 'observationResCatObsPheTime', options['after'], options['before'])
		if 'genera' in options and options['genera'] is not None:
			return []
		if 'species' in options and options['species'] is not None:
			return []

		# get value
		#
		return ObservationController.get_value(db, query)