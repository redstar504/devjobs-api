#!/bin/bash

docker build --no-cache -t redstar504/devjobs-backend:latest .
docker push redstar504/devjobs-backend:latest
kubectl rollout restart deployment devjobs-api