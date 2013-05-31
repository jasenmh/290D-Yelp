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

def selectBusinessByCatagory(dataFile, category):
  """
    parameters:
  dataFile - file containing business objects
  category - Yelp business category
  
    side effects:
  writes a new data file called 'datafile+category' containing only the
  businesses that are in the specified category
  """

  try:
    bus = open(dataFile)
  except IOError:
    print "Unable to open data file: ", dataFile
    return

  fileParts = dataFile.split('.')
  outFile = fileParts[0] + '-' + category + '.' + fileParts[1]
  try:
    busout = open(outFile, 'w')
  except IOError:
    print "Unable to open output file: ", outFile
    return

  for line in bus:
    try:
      data = json.loads(line)
    except ValueError:
      print "Failed to convert JSON object to dictionary"
      return

    if category in data["categories"]:
      busout.write(line)

def selectReviewByBusinessIDs(dataFile, busIDs):

  try:
    revs = open(dataFile)
  except IOError:
    print "Unable to open data file: ", dataFile
    return

  fileParts = dataFile.split('.')
  outFile = fileParts[0] + '-ByIDs.' + fileParts[1]
  try:
    revsout = open(outFile, 'w')
  except IOError:
    print "Unable to open output file: ", outFile
    return

  for line in revs:
    try:
      data = json.loads(line)
    except ValueError:
      print "Failed to convert JSON object to dictionary"
      return

    if data["business_id"] in busIDs:
      revsout.write(line)

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

