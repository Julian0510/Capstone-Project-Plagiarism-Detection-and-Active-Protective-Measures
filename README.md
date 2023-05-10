# Capstone-Project-Plagiarism-Detection-and-Active-Protective-Measures
Similarity Checker that reads in a zybooks zipfile and returns which files are similar to each other along their a corresponding score to the console
Developed for CSUMB Spring 2023 Capstone project Plagiarism Detection and Active Protective Measures.

# System pre-specifications
All your computer needs to be able to do is run the latest version of Python. The imports used by the program should already be built in.

 # How it works
 When you start the program it will run in the console and ask for the name of the zipfile that contains the solution files you would like to compare
 with each other. The program assumes that the zipfile you entered contsins other, nested zipfiles that contain the code you would like to compare. After entering the name of the zipfile you will see the results printed to the console. It will print out the name of the nested file as well as what other files are similar to it (hard coded as any files that have a similarity score >70.0). If none meet the threshhold the line will be blank. Note that currently this program can only compare C++ and Java programs.  
 
 # Known Issues
The program expects that the nested zip file is only one file so it will not run properly if there are 2 or more.

Mac systems add extra artifacts when compressing zip files so please only use the zip file as it originally is when downloaded from zybooks 
