import json

"""
yelpdata.py
This module contains basic functionality to work with the Yelp Phoenix
Academic Dataset.
"""

def importJSONbusiness(dataFile):
	"""
        parameters:
	dataFile - name of file containing business JSON objects

	returns:
	busData - list containing dictionaries representing Yelp businesses
	"""

	busData = []
	try:
		bus = open(dataFile)
	except IOError:
		print "Unable to open data file: ", dataFile
		return -1

	for line in bus:
		try:
			data = json.loads(line)
		except ValueError:
			print "Failed to convert JSON object to dictionary"
			return -1

		busData.append(data)

	return busData

def importJSONcheckin(dataFile):
	"""
	parameters:
	dataFile - name of file containing checkin JSON objects

	returns:
	checkinData - list containing dicts representing Yelp checkins
	"""

	checkinData = []
	try:
		checkin = open(dataFile)
	except IOError:
		print "Unable to open data file: ", dataFile
		return -1

	for line in checkin:
		try:
			data = json.loads(line)
		except ValueError:
			print "Failed to convert JSON object to dictionary"
			return -1

		checkinData.append(data)

	return checkinData

def importJSONreview(dataFile):
	"""
	parameters:
	dataFile - name of file containing review JSON objects

	returns:
	reviewData - list containing dicts representing Yelp reviews
	"""

	reviewData = []
	try:
		review = open(dataFile)
	except IOError:
		print "Unable to open data file: ", dataFile
		return -1

	for line in review:
		try:
			data = json.loads(line)
		except ValueError:
			print "Failed to convert JSON object to dictionary"
			return -1

		reviewData.append(data)

	return reviewData

def importJSONuser(dataFile):
	"""
	parameters:
	dataFile - name of file containing user JSON objects

	returns:
	userData - list containing dicts representing Yelp users
	"""

	userData = []
	try:
		user = open(dataFile)
	except IOError:
		print "Unable to open data file: ", dataFile
		return -1

	for line in user:
		try:
			data = json.loads(line)
		except ValueError:
			print "Failed to convert JSON object to dictionary"
			return -1

		userData.append(data)

	return userData

