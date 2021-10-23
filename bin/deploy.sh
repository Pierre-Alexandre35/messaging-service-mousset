#!/bin/bash

declare BASE_PATH="$(pwd)"
declare GCP_PROJECT_ID="vetements-mousset-313116"
declare IMAGE_NAME="twilio-messaging"
declare CLOUD_RUN_REGION="europe-west1"

docker-compose build
docker push gcr.io/$GCP_PROJECT_ID/$IMAGE_NAME
gcloud config set project $GCP_PROJECT_ID
gcloud run deploy $IMAGE_NAME --image gcr.io/$GCP_PROJECT_ID/$IMAGE_NAME --platform managed --region=$CLOUD_RUN_REGION

