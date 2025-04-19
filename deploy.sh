#!/bin/bash

docker build --platform="linux/amd64" -t redstar504/devjobs-backend:latest .
docker push redstar504/devjobs-backend:latest
kubectl rollout restart deployment devjobs-api