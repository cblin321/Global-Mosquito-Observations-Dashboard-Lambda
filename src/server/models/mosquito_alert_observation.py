################################################################################
#                                                                              #
#                        mosquito_alert_observation.py                         #
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

class MosquitoAlertObservation(Observation):

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
		'dataStreamObsType',
		'dataStreamUniCategory',
		'observationProObsUID',
		'observationResCatObsPheTime',
		'observationResCatObsResTime',
		'observationResCatObsResult',
		'obsResCatObsResult_type',
		'Indentified_by_Human',
		'Identified_by_Machine',
		'observationResCatObsSubTime',
		'observationImaImaStatus',
		'observationImaImaResult',
		'observationConParameters',
		'Aegypti_Certainty',
		'Tiger_Certainty',
		'omProcessLicLicName',
		'omProcessLicLicURI',
		'omProcessLicLicAttSource',
		'omProcessLicAttAggregator',
		'omPrcoessProType',
		'omProcessProReference',
		'omPrcoessResQuaValStatus',
		'omPrcoessResQuaValMethod',
		'omPrcoessResQuaValResult',
		'omPrcoessResQuaQuaGrade',
		'observedProName',
		'observedProDescription',
		'observedProDefinition',
		'sensorName',
		'sensorDescription',
		'sensorEncType',
		'locationName',
		'locationDescription',
		'locationEncType',
		'latitude',
		'longitude',
		'thingName',
		'thingDescription',
		'featureIntName',
		'featureIntDescription',
		'featureIntEncType',
		'featureIntLocation',
		'type',
		'coordinates',
		'nuts_3',
		'nuts_2',
		'Speed',
		'Direction_of_travel',
		'Compass_reading',
		'Position_source_type',
		'Receiver_Name',
		'Horizontal_Accuracy',
		'Altitude',
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
		'objects': [
			'dataStreamUniCategory',
			'observationResCatObsResult',
			'observationConParameters',
			'coordinates'
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
		self.table = 'mosquito_alert'
		self.attributes = attributes;

	#
	# conversion methods
	#

	@staticmethod
	def to_value(key: str, data: object):
		if key in MosquitoAlertObservation.casts['objects']:
			return Observation.to_object(data)
		else:
			return data

	@staticmethod
	def to_values(data: object):
		fields = {}
		count = 0
		for key in MosquitoAlertObservation.fields:
			fields[key] = MosquitoAlertObservation.to_value(key, data[count])
			count += 1
		return fields