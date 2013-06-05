290D-Yelp
============
This repo contains code in python for a class project in UC Santa Barbara's
CS 290D: Searching Big Data course. In our project, we will try to develop
a predictive model that assists users in deciding on when to visit a business
based on how congested or crowded it might be.

Details can be found at the project website:
	https://sites.google.com/site/yelpbusy/home

_Current_
* yelpdata Python module, functions to import JSON data for:
  - Businesses
  - Users
  - Reviews
  - Checkins
* extract JSON objects for businesses by category
* extract JSON objects for reviews by business ID
* YelpDataContainer class that stores Yelp data and methods to operate on it
* BusinessSentiment class in YelpDataContainer module to store/adjust sentiment
* sentiment and business data stored in binary tree (need to change this)

_In Process_
* YelpDataContainer additional functionality
