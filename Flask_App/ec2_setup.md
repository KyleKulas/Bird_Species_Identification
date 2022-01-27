# Instruction for setting up ec2 instance

## Move files to EC2 instance
Copy 'Flask_App' folder to EC2 instance

## Download Anaconda
Get link to latest anaconda version from https://www.anaconda.com/products/individual

$ curl -O https://repo.anaconda.com/archive/Anaconda3-2021.11-Linux-x86_64.sh
$ sh Anaconda3-2021.11-Linux-x86_64.sh


## Create new environment from requirements.txt file
conda create --name tf --file requirements.txt

## Restart terminal

## Start TMUX
$ tmux

## Activate conda environment
$ conda activate tf

## Start Flask App
$ python Flask_App/flask_app.py
