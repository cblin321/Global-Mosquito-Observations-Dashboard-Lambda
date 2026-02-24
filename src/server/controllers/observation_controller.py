################################################################################
#                                                                              #
#                         habitat_mapper_controller.py                         #
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

import flask
from array import array
from flask import request, jsonify
from controllers.controller import Controller

class ObservationController(Controller):

	#
	# query construction methods
	#

	@staticmethod
	def add_filter(query: str, column: str, operator: str, value):
		if column:
			if 'WHERE' in query:
				query += " AND " + column + " " + operator + " '" + value + "'"
			else:
				query += " WHERE " + column + " " + operator + " '" + value + "'"
		return query

	def add_countries_filter(query: str, column: str, countries: array):
		if countries is None:
			return query

		# compose condition
		#
		condition = '('
		count = 0
		for country in countries:
			if count == 0:
				condition += (column + " LIKE '%" + country + "%'")
			else:
				condition += (" OR " + column + " LIKE '%" + country + "%'")
			count += 1
		condition += ')'

		# add condition to query
		#
		if 'WHERE' in query:
			query += " AND " + condition
		else:
			query += " WHERE " + condition

		return query

	@staticmethod
	def add_date_filter(query: str, column: str, after: str, before: str):
		if after:
			query = ObservationController.add_filter(query, column, '>=', after)
		if before:
			query = ObservationController.add_filter(query, column, '<', before)
		return query

	def add_genera_filter(query: str, column: str, genera: array):
		if genera is None:
			return query

		# compose condition
		#
		condition = '('
		count = 0
		for genus in genera:
			if count == 0:
				condition += (column + " LIKE '%" + genus + "%'")
			else:
				condition += (" OR " + column + " LIKE '%" + genus + "%'")
			count += 1
		condition += ')'

		# add condition to query
		#
		if 'WHERE' in query:
			query += " AND " + condition
		else:
			query += " WHERE " + condition

		return query

	def add_species_filter(query: str, column: str, species: array):
		if species is None:
			return query

		# compose condition
		#
		condition = '('
		count = 0
		for specie in species:
			if count == 0:
				condition += (column + " = '" + specie + "'")
			else:
				condition += (" OR " + column + " = '" + specie + "'")
			count += 1
		condition += ')'

		# add condition to query
		#
		if 'WHERE' in query:
			query += " AND " + condition
		else:
			query += " WHERE " + condition

		return query

	#
	# genus getting methods
	#

	@staticmethod
	def get_genera(db: object, table: str):

		# connect to database
		#
		connection = ObservationController.connect(db)
		if connection is None:
			return 'Could not connect to database', 500

		# create query
		#
		query = 'SELECT DISTINCT Indentified_by_Human FROM ' + table;

		# execute query
		#
		cursor = connection.cursor()
		cursor.execute(query)
		data = cursor.fetchall()
		cursor.close()

		# get list of genera
		#
		genera = []
		if data:
			species = [array[0] for array in data]
			for item in species:
				if item and ' ' in item:
					terms = item.split(' ')
					genus = terms[0]
					if not genus in genera:
						genera.append(terms[0])
			genera.sort()

		# return results
		#
		return genera

	@staticmethod
	def get_genera_by_indices(db: object, table: str, indices: array):
		if indices is None:
			return []
		array = []
		genera = ObservationController.get_genera(db, table)
		if genera:
			indes = 0
			for index in indices:
				array.append(genera[int(index) - 1])
		return array

	#
	# getting methods
	#

	@staticmethod
	def get_all(db: object, query: str):

		# connect to database
		#
		connection = Controller.connect(db)
		if connection is None:
			return 'Could not connect to database', 500

		# execute query
		#
		cursor = connection.cursor()
		cursor.execute(query)
		data = cursor.fetchall()
		cursor.close()

		# return results
		#
		return data

	@staticmethod
	def get_one(db: object, query: str):

		# connect to database
		#
		connection = Controller.connect(db)
		if connection is None:
			return 'Could not connect to database', 500

		# execute query
		#
		cursor = connection.cursor()
		cursor.execute(query)
		data = cursor.fetchone()
		cursor.close()
		
		return data

	@staticmethod
	def get_value(db: object, query: str):

		# connect to database
		#
		connection = Controller.connect(db)
		if connection is None:
			return 'Could not connect to database', 500

		# execute query
		#
		cursor = connection.cursor()
		cursor.execute(query)
		result = cursor.fetchone()
		value = result[0]
		cursor.close()

		# return num
		#
		return str(value)
