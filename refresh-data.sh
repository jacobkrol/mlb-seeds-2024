#!/bin/bash

echo "Fetching team data..."
node fetchteamdata/index.js

echo "Computing seed data..."
py computeseeds/computeseeds.py

echo "Converting to usable JSON..."
py computeseeds/seedcsvtojson.py

echo "Copying data into UI src..."
cp /computeseeds/allongseeddata.json /computeseeds/nllongseeddata.json /src/data/

echo "Complete!"
