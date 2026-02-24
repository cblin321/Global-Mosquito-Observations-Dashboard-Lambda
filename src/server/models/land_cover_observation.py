################################################################################
#                                                                              #
#                          land_cover_observation.py                           #
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

import json
from models.observation import Observation

class LandCoverObservation(Observation):

	#
	# attributes
	#

	fields = [
		'id',
		'OBJECTID',
		'title',
		'description',
		'dataStreamName',
		'dataStreamDescription',
		'observationType',
		'unitOfCategory',
		'projectObservationUID',
		'phenomenonTime',
		'resultTime',
		'result',
		'submitTime',
		'imageStatus',
		'imageResult',
		'lc_UpwardPhotoUrl',
		'lc_DownwardPhotoUrl',
		'lc_EastPhotoUrl',
		'lc_WestPhotoUrl',
		'lc_NorthPhotoUrl',
		'lc_SouthPhotoUrl',
		'parameters',
		'licenseName',
		'licenseURI',
		'attributionDataAggregator',
		'validationStatus',
		'validationMethod',
		'validationResult',
		'qualityDescription',
		'qualityGrade',
		'observedPropertyName',
		'observedPropertyDescription',
		'observedPropertyDefinition',
		'sensorName',
		'sensorDescription',
		'locationName',
		'locationDescription',
		'locationEncodingType',
		'latitude',
		'longitude',
		'elevation',
		'thingName',
		'thingDescription',
		'featureName',
		'featureDescription',
		'featureEncodingType',
		'featureLocation',
		'Speed',
		'Altitude',
		'Direction_of_travel',
		'Compass_reading',
		'Position_source_type',
		'Receiver_Name',
		'Horizontal_Accuracy',
		'Vertical_Accuracy',
		'PDOP',
		'HDOP',
		'VDOP',
		'Fix_Type',
		'Correction_Age',
		'Station_ID',
		'Number_of_Satellites',
		'Fix_Time',
		'Average_Horizontal_Accuracy',
		'Average_Vertical_Accuracy',
		'Averaged_Positions',
		'Standard_Deviation',
		'x',
		'y',
		'country'
	]

	#
	# casting
	#

	casts = {
		'ints': [
			'imageStatus',
			'validationStatus'
		],

		'objects2': [
			'dataStreamDescription',
			'unitOfCategory',
			'result',
			'imageResult',
			'parameters',
			'thingDescription',
			'featureLocation'
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
		self.table = 'land_cover'
		self.attributes = attributes;

	#
	# conversion methods
	#

	@staticmethod
	def to_value(key: str, data: object):
		if key in LandCoverObservation.casts['ints']:
			return Observation.to_int(data)
		elif key in LandCoverObservation.casts['objects2']:
			return Observation.to_object2(data)
		else:
			return data

	@staticmethod
	def to_values(data: object):
		fields = {}
		count = 0
		for key in LandCoverObservation.fields:
			fields[key] = LandCoverObservation.to_value(key, data[count])
			count += 1
		return fields