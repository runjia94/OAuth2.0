Find Restaurant Nearby
======================

This project uses google map api and foursquare api
1. geocode.py contains a google map api to find the latitude and longtitude,
when you input a location (like FortCollins, USA)
2. findRestaurants.py uses foursquare api.
According the lat and lng from geocode.py, they locate the place and find nearby Restaurants.
3. findRestaurantApp transit the result into a json format and at the same time store in the database
(Database is SQLITE)
4. The tester.py tests the process: input place, find restaurant, store in database, query databse.
