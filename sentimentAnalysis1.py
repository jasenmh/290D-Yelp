#!/usr/bin/python

from YelpDataContainer import YelpDataContainer
import time
import sys

def writeOutput(y, outCount):
  outFile = "SentimentOut{0}.txt".format(outCount)
  fo = open(outFile, 'w')
  count = 0
  for sent in y.sentiment:
    if count % 500 == 0:
      print "Printing..."
    count += 1
    fo.write(sent.sentimentToString() + '\n')
  fo.close()

def main():
  quietMode = 0
  pruneCount = 0

  for i in range(1, len(sys.argv)):
    arg = sys.argv[i]
    if arg == '-q':   #quiet mode
      quietMode = 1
      continue
    try:
      pruneCount = int(arg)
    except ValueError:
      print "Unable to parse argument:", arg
      return

  y = YelpDataContainer()
  revCount = 0
  outCount = 0

  print "Loading data..."
  y.loadBusiness('data/yelp_academic_dataset_business-Restaurants.json')
  y.loadReview('data/yelp_academic_dataset_review-Restaurants.json')

  timeStart = time.time()
  timeLast = time.time()
  print "Starting analysis..."
  for rev in y.review:
    revCount += 1
    if revCount % 1000 == 0:
      writeOutput(y, revCount)
    if revCount % 100 == 0:
      timeNew = time.time()
      print "--Review",revCount," Time",timeNew-timeLast,"/",timeNew-timeStart
      timeLast = timeNew
    s = y.findSentimentByBusinessID(rev["business_id"])
    if s == 0:
      continue
    b = y.getBusinessByID(rev["business_id"])
    s.setLatitude(b["latitude"])
    s.setLongitude(b["longitude"])
    #print "Analyzing review for ", rev["business_id"]
    s.analyzeReviewSentiment(rev)

  writeOutput(y, "Final")

if __name__ == "__main__":
  main()
