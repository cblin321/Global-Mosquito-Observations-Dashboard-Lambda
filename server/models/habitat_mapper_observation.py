################################################################################
#                                                                              #
#                        habitat_mapper_observation.py                         #
#                                                                              #
################################################################################
#                                                                              #
#        This is a model for managing habitat mapper observations.             #
#                                                                              #
#        Author(s): Abe Megahed                                                #
#                                                                              #
#        This file is subject to the terms and conditions defined in           #
#        'LICENSE.txt', which is part of this source code distribution.        #
#                                                                              #
################################################################################
#     Copyright (C) 2025, Data Science Institute, University of Wisconsin      #
################################################################################

from models.observation import Observation

class HabitatMapperObservation(Observation):

	#
	# attributes
	#

	fields = [
		'id',
		'mhm_protocol',
		'mhm_measuredDate',
		'mhm_createDate',
		'mhm_updateDate',
		'mhm_publishDate',
		'mhm_organizationId',
		'mhm_organizationName',
		'mhm_siteId',
		'mhm_siteName',
		'mhm_ExtraData',
		'mhm_AbdomenCloseupPhotoUrls',
		'mhm_WaterSourcePhotoUrls',
		'mhm_LarvaFullBodyPhotoUrls',
		'mhm_LarvaeCount',
		'mhm_MosquitoEggs',
		'mhm_LocationAccuracyM',
		'mhm_MosquitoEggCount',
		'mhm_Comments',
		'mhm_Latitude',
		'mhm_Longitude',
		'mhm_MosquitoHabitatMapperId',
		'mhm_BreedingGroundEliminated',
		'mhm_MeasuredAt',
		'mhm_MeasurementElevation',
		'mhm_Userid',
		'mhm_Genus',
		'mhm_LocationMethod',
		'mhm_WaterSource',
		'mhm_MosquitoAdults',
		'mhm_Species',
		'mhm_MosquitoPupae',
		'mhm_DataSource',
		'mhm_LastIdentifyStage',
		'mhm_WaterSourceType',
		'mhm_GlobeTeams',
		'x',
		'y',
		'country'
	]

	#
	# casting
	#

	casts = {
		'urls': [
			'mhm_AbdomenCloseupPhotoUrls',
			'mhm_WaterSourcePhotoUrls',
			'mhm_LarvaFullBodyPhotoUrls'
		]
	}

	#
	# constructor
	#

	def __init__(self, attributes: object = {}):

		"""
		Creates a new model with the specified attributes.

		Parameters:
			attributes (dict): The model's attributes
		"""

		# set attributes
		#
		self.table = 'habitat_mapper'
		self.attributes = attributes;

	#
	# conversion methods
	#

	@staticmethod
	def to_value(key: str, data: object):
		if key in HabitatMapperObservation.casts['urls']:
			return Observation.to_urls(data)
		else:
			return data

	@staticmethod
	def to_values(data: object):
		fields = {}
		count = 0
		for key in HabitatMapperObservation.fields:
			fields[key] = HabitatMapperObservation.to_value(key, data[count])
			count += 1
		return fields
