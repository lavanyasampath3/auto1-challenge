# auto1-code challenge-UI

### Introduction 
This repository contains the UI automation code for the challenge . It has a self contained automation framework that was build atop of selenium python binding.
### Supported Browsers
__The Automation is tested in chome browser__ . It should be possible to add support to other browsers through a small code change
### Running the test cases 
Follow the steps given in the section `Running the Test Locally` to execute the test case

#### __Running the Test locally__
__Prerequisites:__
1. The project requires pip3 and Python 3 to be installed and configured . 
2. The automation needs selenium server running in standalone mode or grid mode, Either locally or at an IP that is visible  

__Configuation Steps:__

1. Download Selenium server : Download the selenium standalone server jar from https://www.seleniumhq.org/download/
2. Download Chrome driver : Download the latest version of the chrome driver from http://chromedriver.chromium.org/downloads ,extract the contents and __copy the chromedriver binary to the same folder containing the selenium standalone server jar file__
3. Launch the selenium server in standalone mode with the command __`java -jar <path to the selenium standalone.jar>`__

__Running the Tests:__

The tests can be launched from the command line, First Navigate to the automation-code-challenge base folder 
1. To run the automation in chrome type __download the code from test.py file from github and run the code

#### __Other Details__
1. Filters used for validation : The framework uses (Erstzulassung-2015 and Höchster Preis)
2. Screenshots on failure : Not Implemented.
3. Ability to run tests for different browsers/OS/Environments by configuring - the driver and a small piece of code in the main class Currently chrome is supported
4. The framework uses Punit concept.

#### A note on Assertion messages 
The code uses generators to check if the vehicles are greater than 201. This peice of code is taken from stackoverflow.com

