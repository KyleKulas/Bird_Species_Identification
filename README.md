# Bird Species Identification
The goal of this project is to create a set of tools to monitor a bird feeder and automatically track, classify species, and count the number of visits. This is a final project for Lighthouse Labs Data Science Bootcamp.

## Motivation
[Project FeederWatch](https://feederwatch.org/) is a joint research and education project of Birds Canada and the Cornell Lab of Ornithology. Thousand of volunteers across North America count birds that come to their birdfeeders and submit their counts to Project FeederWatch. This data is then made public and has been a critical source of data for the analysis of bird populations across the contenent. This approach to data collection has a few problems:

1 - It is time consuming for volunteers to watch their feeders

2 - It requires that the volunteers be able to accurately indentify different species that visit their feeders

3 - It is inconsistent because volunteers cannot not watch their feeders all day, everyday. 

This project hopes to solve these problems.

## Project Overview
I've broken the project up into three phases. 
### Phase 1 - Species Identification
Machine learning model that can take an image of bird as input and classify what species the bird belongs to. For this task I am using a vgg16 convolutional neural network that has been pretrained on the ImageNet dataset. From this base model, I use transfer learning in Keras to train the model on a dataset of [325 bird species](https://www.kaggle.com/gpiosenka/100-bird-species) from kaggle.

Accuracy for this model on the test dataset is 91.6%. The notebook can be found in [Models](Models/325_class_bird_species/).

A prototype web app using the model can be found in [Flask_App](Flask_App/)

### Phase 2 - Image Capturing
I am using a Raspberry Pi to remotely capture images of birds visiting our feeder. The script uses a background subtraction method to recognize birds that move into the camera's field of view then saves a cropped photo of the bird for analysis but the species identification model. 

The script and installation instructions can be found in [Raspberrypi](Raspberrypi/).

### Phase 3 - Integration and species counting
This phase consists of integrating the 2 previous systems together to achieve an automated way of recording bird species that visit our feeder. 