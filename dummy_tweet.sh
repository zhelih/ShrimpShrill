#!/bin/bash

curl -i -H "Content-Type: application/json" -X POST -d '{"user":"Satan", "date":1455, "source":0}' http://localhost:5000/ers/post_new
curl -i -H "Content-Type: application/json" -X POST http://localhost:5000/ers/next_pending
curl -i -H "Content-Type: application/json" -X POST -d '{"location":{"state":"TX", "city":"CollegeStation", "street":"Holland","building":"666","latitude":30.589,"longitude":-96.316},"level": 2, "approved":1980 }' http://localhost:5000/ers/approve/1

curl -i -H "Content-Type: application/json" -X POST -d '{"user":"Jade", "date":1984, "source":0, "text":"Oh my heavenly hash browns!", "location":{"city":"CollegeStation", "latitude": 30.609, "longitude": -96.3403}}' http://localhost:5000/ers/post_new
curl -i -H "Content-Type: application/json" -X POST http://localhost:5000/ers/next_pending
curl -i -H "Content-Type: application/json" -X POST -d '{"level": 3, "approved":1999 }' http://localhost:5000/ers/approve/2

curl -i -H "Content-Type: application/json" -X POST -d '{"user":"Ladybug", "date":277270, "source":0, "text":"Fake news! Sad", "location":{"city":"College Station", "latitude": 30.622, "longitude": -96.3394}}' http://localhost:5000/ers/post_new
curl -i -H "Content-Type: application/json" -X POST http://localhost:5000/ers/next_pending
curl -i -H "Content-Type: application/json" -X POST -d '{"level": 1, "approved":321321 }' http://localhost:5000/ers/approve/3
