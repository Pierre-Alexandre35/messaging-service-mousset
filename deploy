#!/bin/bash

echo "Hello, world!"

docker-compose build
docker push gcr.io/vetements-mousset-313116/twilio-messaging
gcloud run deploy twilio-messaging --image gcr.io/vetements-mousset-313116/twilio-messaging --platform managed --region=europe-west1

echo "ok"
