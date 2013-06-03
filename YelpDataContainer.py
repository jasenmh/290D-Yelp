import yelpdata
from TreeNode import TreeNode
import datetime
import json

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
    self.busRoot = 0
    self.checkin = []
    self.review = []
    self.user = []
    self.sentiment = []
    self.sentRoot = 0

  def loadBusiness(self, fileName):
    """
    Takes the name of the file containing Business data and stores the
    data in the self.business[] list.
    """
    t = yelpdata.importJSONbusiness(fileName)
    self.business = t[0]
    self.busRoot = t[1]
    # print self.busRoot, "should be", t[1]

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
    return -1   # does not work with business binary tree, need to redo

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

  def getBusinessByID(self, busID):
    """
    This method takes a Yelp business ID and returns the data tuple for
    that business.
    """
    return self.busRoot.findValueByKey(busID)

    #for bus in self.business:
    #  if busID == bus['business_id']:
    #    return bus

    #return 0

  def findSentimentByBusinessID(self, busID):
    """
    Finds the sentiment class for a specific business and returns it. If
    the sentiment does not exist, one is created.
    """
    if self.sentRoot == 0:  # no sentiments yet
      bs = BusinessSentiment(busID)
      self.sentiment.append(bs)
      s = TreeNode()
      s.key = busID
      s.value = bs
      self.sentRoot = s
    else:   # there are some sentiments, lets try to find ours  
      s = self.sentRoot.findValueByKey(busID)
      if s == 0:    # didn't find one, make it up
        bs = BusinessSentiment(busID)
        self.sentiment.append(bs)
        s = TreeNode()
        s.key = busID
        s.value = bs

    try:
      v = s.value
    except AttributeError:
      print "Found broken sentiment for ID", busID
      v = 0

    return v

    #for sents in self.sentiment:
    #  if(sents.businessID == busID):
    #    return sents

    #s = BusinessSentiment(busID)
    #self.sentiment.append(s)
    #return s

class BusinessSentiment:
  """
  Stores sentiment values for a business (identifiable by its businessID
  property) for each day of the week (0-6) and 2 meal times (0=lunch, 
  1=dinner).
  """
  dinnerDict = []
  lunchDict = []
  positiveDict = []
  negativeDict = []

  def __init__(self, bID = 0):
    self.businessID = bID
    self.latitude = 0.0
    self.longitude = 0.0
    self.posReviewByDay = [0 for x in range(7)]
    self.negReviewByDay = [0 for x in range(7)]
    self.reviewCountByDay = [0 for x in range(7)]
    if len(BusinessSentiment.positiveDict):
      BusinessSentiment.loadDictionaries()

  def sentimentToString(self):
    returnString = "{0}, {1}, {2}, ".format(self.businessID, self.latitude, self.longitude)
    for x in range(7):
      returnString += str(self.getSentiment(x))
      returnString += ", "
      returnString += str(self.reviewCountByDay[x])
      if x != 6:
        returnString += ", "
    return returnString


  def setLatitude(self, lat):
    self.latitude = lat

  def setLongitude(self, lng):
    self.longitude = lng

  def getSentiment(self, day):
    """
    Gets sentiment rating for specified day of the week (0-6) and time
    (0=lunch, 1=dinner) of day.
    """
    if(day > 6):
      return -1

    if self.reviewCountByDay[day] == 0:
      return 0.5    # no reviews, no sentiment
    else:
      return self.negReviewByDay[day] / self.reviewCountByDay[day]

  def getBusinessID(self):
    return self.businessID

  def setBusinessID(self, bID):
    self.businessID = bID

  def analyzeReviewSentiment(self, reviewList):
    """
    This function takes the text of a review and 1) determine the day of the
    week it applies to, 2) determines the meal it applies to (or both as a
    default) and 3) determines the sentiment (+.1 or -.1) to add to the
    existing sentiment for that day/time.
    """

    sentiment = 0

    if len(BusinessSentiment.dinnerDict) == 0:
      BusinessSentiment.loadDictionaries()

    revData = reviewList

    # day of week
    dateList = revData["date"].split('-')
    rDt = datetime.datetime(int(dateList[0]), int(dateList[1]), int(dateList[2]))
    dayOfWeek = rDt.weekday()

    self.reviewCountByDay[dayOfWeek] += 1

    # isolate sentences in review text
    revText = revData["text"]
    revSent2 = revText.split('.') # first split review into sentences by periods
    revSent1 = []
    for sent in revSent2:
      revSent1 += sent.split('?') # then by question marks
    revSent = []
    for sent in revSent1:
      revSent += sent.split('!') # then bangs, leaving all sentences split?

    # evaluate each sentence for sentiment
    for sentence in revSent:
      words = sentence.split(' ')
      for element in BusinessSentiment.negativeDict:
        if element in words:
          sentiment -= 1
      for element in BusinessSentiment.positiveDict:
        if element in words:
          sentiment += 1

    # set new sentiment for day of week
    if sentiment > 0:
      self.posReviewByDay[dayOfWeek] += 1
    else:
      self.negReviewByDay[dayOfWeek] += 1

  @staticmethod
  def loadDictionaries():
    """
    Populates sentiment dictionaries
    """

    dataFile = open('dinner.txt')
    for line in dataFile:
      BusinessSentiment.dinnerDict.append(line)

    dataFile = open('lunch.txt')
    for line in dataFile:
      BusinessSentiment.lunchDict.append(line)

    dataFile = open('negative.txt')
    for line in dataFile:
      BusinessSentiment.negativeDict.append(line)

    dataFile = open('positive.txt')
    for line in dataFile:
      BusinessSentiment.positiveDict.append(line)
