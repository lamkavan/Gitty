# Gitty
**IBM Summer Project 2019**  
**Developers**: Kavan Lam and Nimrah Gill  
**Mentor/Guidance**: Don Bourne

## What is Gitty

Gitty aims to automate git issue routing using artificial intelligence to determine the best team and/or person to assign to. 

This project is not intended for commerical use, but displays what artificial intelligence is capable of and is a great learning experience for developers. A wide range of technologies including Python, Javascript, Express, Flask, Github REST API, Keras/Tensorflow and Gensim were used in this project.


Gitty has three main sections each responsible for one task:

1. Data Collection

   - Collects data from the issues found within the repositories of the [OpenLiberty project](https://github.com/OpenLiberty/)

2. Model Creation and Training
   
   - Creates the models and trains the neural network on the data that was collected
   
3. Predictions

   - Predicts the best teams and assignees for a given git issue for the [open-liberty repository](https://github.com/OpenLiberty/open-liberty)



## Instructions to setup Gitty

The following contains important information about the application and usage details. These instructions will be as general as possible, but they were written with Windows in mind.

### Setup details for the frontend
  1. Ensure [node.js](https://nodejs.org/en/) and `npm` are installed and working (`npm` should automatically come with node.js)
  2. `cd` to Gitty/IBM_Summer_Project_2019/Frontend/dependencies
  3. Run the following command to install all the dependencies for the frontend
     ```
     npm install
     ```
  4. `cd` to Gitty/IBM_Summer_Project_2019/Frontend/javascript
  5. Run the following command
     ```
     node server.js
     ```
  6. Go to the `localhost:<port_number>` endpoint. The port number is given to you after running the above command
  7. You will now be able to view the applicaiton on the webpage (Google Chrome recommended)

### Setup details for the backend
  1. Download a version of Python that works with Tensorflow ([Python3.6.6](https://www.python.org/downloads/release/python-366/) recommended)
  2. Download/install all dependencies for the backend. There are many ways to do this, but most people will resort to using `pip`. However, using PyCharm is higly recommened for the ease of use. Below is a complete list of all the dependencies needed.
     - Flask
     - Flask-Cors
     - Keras
     - gensim
     - pandas
     - numpy
     
     If you decide to use PyCharm then just open the backend code and all the missing dependencies will be underlined in red in the imports. Then just go over to Files --> Settings --> Project:Gitty --> Project Interpreter and ensure you select Python3.6.6 as the interpreter. Then click the plus icon on the right, and a new window should appear. Type in the name of the missing dependencies and install them.
  3. Once you have the dependencies installed. All you need to do is start the backend server to do this run the following command
     ```
     <location of Python3.x>/python.exe   <location of Gitty>/Gitty/IBM_Summer_Project_2019/backend/app.py
     ```
     
     You will see a lot of text printed to the console (that is fine). If it worked you will see 
     > Running on http://127.0.0.1:5000/ Press `CTRL+C` to quit
     
     at the very end. Now go back to the webpage and it should be ready to use.
   
### Important information

If you select to retrieve all the issues for all the repositories under OpenLiberty
then expect to wait up to 1 hour for the application to finish. The reason is because
the Github REST api has a limit on how many search requests can be made in a minute.
Also, when using the application be sure to let things finish loading before hitting other
endpoints.

### Login information for dummy Github account
Outlook account

    Email: IBM-Gitty@outlook.com
    Password: [Please ask repo owners]
    
Github account (Required to increase the Github REST api search limit)

    Username: IBM-Gitty
    Password: [Please ask repo owners]
