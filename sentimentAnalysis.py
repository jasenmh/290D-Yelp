#!/usr/bin/python

from YelpDataContainer import YelpDataContainer
import yelpdata
import time
import sys

def writeOutput(y, outCount, quietMode):
  outFile = "SentimentOut{0}.txt".format(outCount)
  fo = open(outFile, 'w')
  count = 0
  for sent in y.sentiment:
    if quietMode == 0 and count % 5000 == 0:
      print "Printing..."
    count += 1
    fo.write(sent.sentimentToString() + '\n')
  fo.close()

def main():
  quietMode = 0
  pruneCount = 0
  saveInterval = 1000
  reportInterval = 100

  for i in range(1, len(sys.argv)):
    clArg = sys.argv[i]
    if clArg == '-q':   #quiet mode
      quietMode = 1
      continue

  y = YelpDataContainer()
  revCount = 0
  outCount = 0

  print "Loading data..."
  y.loadBusiness('data/yelp_academic_dataset_business-Restaurants-Over100.json')
  #y.loadReview('data/yelp_academic_dataset_review-Restaurants-Over100.json')
  rFile = open('data/yelp_academic_dataset_review-Restaurants-Over100.json')

  if quietMode == 0:
    timeStart = time.time()
    timeLast = time.time()

  print "Starting analysis..."
  #for rev in y.review:
  for line in rFile:
    rev = yelpdata.importSTRINGreview(line)
    revCount += 1
    if revCount % saveInterval == 0:
      writeOutput(y, revCount, quietMode)
    if quietMode == 0 and revCount % reportInterval == 0:
      timeNew = time.time()
      print "--Review",revCount," Time",timeNew-timeLast,"/",timeNew-timeStart
      timeLast = timeNew
    s = y.findSentimentByBusinessID(rev["business_id"])
    if s == 0:  # This shouldn't happen anymore
      print "No sentiment for {0}, skipping it.".format(rev["business_id"])
      continue
    if s.latitude == 0.0:
      b = y.getBusinessByID(rev["business_id"])
      s.setLatitude(b["latitude"])
      s.setLongitude(b["longitude"])

    s.analyzeReviewSentiment(rev)

  rFile.close()

  print "Printing results..."
  writeOutput(y, "Final", quietMode)

if __name__ == "__main__":
  main()
