#!/bin/bash

curl -i -H "Content-Type: application/json" -X POST -d '{"user":"Satan", "date":1455, "source":0}' http://localhost:5000/ers/post_new
curl -i -H "Content-Type: application/json" -X POST http://localhost:5000/ers/next_pending
curl -i -H "Content-Type: application/json" -X POST -d '{"location":{"state":"TX", "city":"CollegeStation", "street":"Holland","building":"666","latitude":30.589,"longitude":-96.316},"level": 2, "approved":1980 }' http://localhost:5000/ers/approve/1
