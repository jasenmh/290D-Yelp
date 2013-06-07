#!/usr/bin/python

import yelpdata

revs = yelpdata.importJSONreview('data/yelp_academic_dataset_review-Restaurants-Over100.json')

found = {}
matches = {}
for r in revs:
  rb = r["business_id"]
  rd = r["date"]
  if rb not in found.keys():
    td = []
    td.append(rd)
    found[rb] = td
  elif rd not in found[rb]:
    found[rb].append(rd)
  else:
    if rb not in matches.keys():
      td = {}
      td[rd] = 2 
      matches[rb] = td
    elif rd not in matches[rb].keys():
      matches[rb][rd] = 2
    else:
      matches[rb][rd] += 1

if len(matches) == 0:
  print "No reviews happen on the same day."
else:
  for rb in matches.keys():
    for rd in matches[rb].keys():
      print "{0} on {1} got {2} reviews.".format(rb, rd, matches[rb][rd])

