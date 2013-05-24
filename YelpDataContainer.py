import yelpdata

"""
This module contains the YelpDataContainer class.
"""

class YelpDataContainer:

"""
This class holds yelp data retrieved from the Phoenix Academic Dataset, read
from files, and includes methods to help use that data.
"""

	def __init__(self):
		self.business = []
		self.checkin = []
		self.review = []
		self.user = []

	def loadBusiness(self, fileName):
	"""
	Takes the name of the file containing Business data and stores the
	data in the self.business[] list.
	"""
		self.business = yelpdata.importJSONbusiness(fileName)

	def loadCheckin(self, fileName):
	"""
	Takes the name of the file containing Checkin data and stores the
	data in the self.checkin[] list.
	"""
		self.checkin = yelpdata.importJSONcheckin(fileName)

	def loadReview(self, fileName):
	"""
	Takes the name of the file containing Review data and stores the
	data in the self.review[] list.
	"""
		self.review = yelpdata.importJSONreview(fileName)

	def loadUser(self, fileName):
	"""
	Takes the name of the file containing User data and stores the
	data in the self.user[] list.
	"""
		self.user = yelpdata.importJSONuser(fileName)
