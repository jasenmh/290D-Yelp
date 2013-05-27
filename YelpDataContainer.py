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

  def idReviewsByBusinesses(self):
    """
    Builds a dictionary of reviews about the indexed businesses.
    """
    businessReviews = {}
    reviewFound = 0

    if len(self.review) == 0 or len(self.business) == 0:
      return 0

    for review in self.review:
      reviewFound = 0
      for business in self.business:
        if review['business_id'] == business['business_id']:
          bIdx = review['business_id']
          if bIdx in businessReviews:
            businessReviews[bIdx] = businessReviews[bIdx] + 1
            reviewFound = 1
          else:
            businessReviews[bIdx] = 1

        if reviewFound == 1:
          break;

    return businessReviews

  def getBusinessByID(self, busId):
    """
    This method takes a Yelp business ID and returns the data tuple for
    that business.
    """
    for bus in self.business:
      if busId == bus['business_id']:
        return bus

    return 0
