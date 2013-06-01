import yelpdata
import datetime

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
    self.seniment = []

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

  def findSentimentByBusinessID(self, busID):
    """
    Finds the sentiment class for a specific business and returns it. If
    the sentiment does not exist, one is created.
    """
    for sents in self.sentiment:
      if(sents.businessID == busID):
        return sents

    s = BusinessSentiment(busID)
    self.sentiment.append(s)
    return s

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

  def __init__(self, bID = 0, sents = [.5 for x in range(14)]):
    self.sentiment = sents
    self.businessID = bID
    self.reviewCountByDay = [0 for x in range(7)]
    if len(positiveDict):
      BusinessSentiment.loadDictionaries()

  def getSentiment(self, day, meal):
    """
    Gets sentiment rating for specified day of the week (0-6) and time
    (0=lunch, 1=dinner) of day.
    """
    if(day > 6):
      return -1

    if(meal != 0):
      day += 7   # array elements 0-6 are mon-sun lunch, 7-13 mon-sun dinner

    return self.sentiment[day]

  def setSentiment(self, day, meal, sent):
    """
    Sets sentiment for a day of the week (0=Monday-6=Sunday) and time
    (0=lunch, 1=dinner) to a value 0-1 (0=busiest sentiment).
    """
    if(meal != 0):
      day += 7
    if(day > 13):
      return

    self.sentiment[day] = sent

  def getReviewCountByDay(self, dayOfWeek):
    return self.reviewCountByDay[dayOfWeek]

  def getBusinessID(self):
    return self.businessID

  def setBusinessID(self, bID):
    self.businessID = bID

  def analyzeReviewSentiment(self, reviewJSON):
    """
    This function takes the text of a review and 1) determine the day of the
    week it applies to, 2) determines the meal it applies to (or both as a
    default) and 3) determines the sentiment (+.1 or -.1) to add to the
    existing sentiment for that day/time.
    """

    timeSlot = 0
    sentiment = 0

    if len(self.dinnerDict) == 0:
      self.loadDictionaries()

    try:
      revData = json.loads(reviewJSON)
    except ValueError:
      print "Unable to parse review data."
      return

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

    # evaluate each sentence for meal time and sentiment
    for sentence in revSent:
      words = sentence.split(' ')
      for element in lunchDict:
        if element in words:
          timeSlot -= 1
      for element in dinnerDict:
        if element in words:
          timeSlot += 1
      for element in negativeDict:
        if element in words:
          sentiment -= 1
      for element in positiveDict:
        if element in words:
          sentiment += 1

    # determine meal time
    if timeSlot > 0:
      timeSlot = 1
    else:
      timeSlot = 0

    # determine sentiment
    if sentiment > 0:
      sentiment = .1
    elif sentiment < 0:
      sentiment = -.1
    else:
      sentiment = 0

    # set new sentiment for day of week
    currentSentiment = this.getSentiment(dayOfWeek, timeSlot)
    currentSentiment += sentiment
    if currentSentiment > 1:
      currentSentiment = 1
    elif currentSentiment < 0:
      currentSentiment = 0
    this.setSentiment(dayOfWeek, timeSlot, currentSentiment)

  @staticmethod
  def loadDictionaries():
    """
    Populates sentiment dictionaries
    """

    dataFile = open('dinner.txt')
    for line in dataFile:
      dinnerDict.append(line)

    dataFile = open('lunch.txt')
    for line in dataFile:
      lunchDict.append(line)

    dataFile = open('negative.txt')
    for line in dataFile:
      negativeDict.append(line)

    dataFile = open('positive.txt')
    for line in dataFile:
      positiveDict.append(line)
