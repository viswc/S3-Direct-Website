#!/bin/bash
cd /home/ec2-user/S3-Direct-Website
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
