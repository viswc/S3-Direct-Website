#!/bin/bash
cd /home/ec2-user/S3DirectWebsite
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
