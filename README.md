# Uzbek licence plate generator

A tool for generating Uzbek licence plate dataset for plate detecting.

## First Stage: Create training data
* Open create_train_data.py
* Edit "lets" array according to which letters you need
* Edit "nums" array according to how many letters you need
* A variable called "Batchsize" on 180th line is number of training data. Pay attantion to combination of "nums" list and this variable

## Second Stage: Augmentation
* Run augmentation.py

After completing these two stages, you can get full training data in result folder

<!-- This is some text
* This is a list item
* This is another one
* Another one -->
