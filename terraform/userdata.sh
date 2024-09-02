#!/bin/bash
sudo yum update -y
sudo amazon-linux-extras install docker -y
sudo yum install docker -y
sudo service docker start
sudo usermod -a -G docker ec2-user
sudo chkconfig docker on
sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo yum install git -y
cd /home/ec2-user
git clone https://github.com/SimonJan2/Employee_Management_Flask.git
cd Employee_Management_Flask
docker-compose up -d