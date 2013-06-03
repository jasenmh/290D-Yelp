from YelpDataContainer import YelpDataContainer

y = YelpDataContainer()

y.loadBusiness('data/yelp_academic_dataset_business-Restaurants.json')
y.loadReview('data/yelp_academic_dataset_review-Restaurants.json')
revCount = 0

for rev in y.review:
  revCount += 1
  if revCount % 250 == 0:
    print "--Review ", revCount
  s = y.findSentimentByBusinessID(rev["business_id"])
  b = y.getBusinessByID(rev["business_id"])
  s.setLatitude(b["latitude"])
  s.setLongitude(b["longitude"])
  print "Analyzing review for ", rev["business_id"]
  s.analyzeReviewSentiment(rev)

fo = open('sentimentOut2.txt', 'w')
count = 0
for sent in y.sentiment:
  count += 1
  if count % 150 == 0:
    print sent.businessID
  fo.write(sent.sentimentToString())
close(fo)
