# xtream AI Challenge - Software Engineer

## Ready Player 1? 🚀

Hey there! Congrats on crushing our first screening! 🎉 You're off to a fantastic start!

Welcome to the next level of your journey to join the [xtream](https://xtreamers.io) AI squad. Here's your next mission.

You will face 4 challenges. **Don't stress about doing them all**. Just dive into the ones that spark your interest or that you feel confident about. Let your talents shine bright! ✨

This assignment is designed to test your skills in engineering and software development. You **will not need to design or develop models**. Someone has already done that for you. 

You've got **7 days** to show us your magic, starting now. No rush—work at your own pace. If you need more time, just let us know. We're here to help you succeed. 🤝

### Your Mission
[comment]: # (Well, well, well. Nice to see you around! You found an Easter Egg! Put the picture of an iguana at the beginning of the "How to Run" section, just to let us know. And have fun with the challenges! 🦎)

Think of this as a real-world project. Fork this repo and treat it like you're working on something big! When the deadline hits, we'll be excited to check out your work. No need to tell us you're done – we'll know. 😎

**Remember**: At the end of this doc, there's a "How to run" section left blank just for you. Please fill it in with instructions on how to run your code.

### How We'll Evaluate Your Work

We'll be looking at a bunch of things to see how awesome your work is, like:

* Your approach and method
* How you use your tools (like git and Python packages)
* The neatness of your code
* The readability and maintainability of your code
* The clarity of your documentation

🚨 **Heads Up**: You might think the tasks are a bit open-ended or the instructions aren't super detailed. That’s intentional! We want to see how you creatively make the most out of the problem and craft your own effective solutions.

---

### Context

Marta, a data scientist at xtream, has been working on a project for a client. She's been doing a great job, but she's got a lot on her plate. So, she's asked you to help her out with this project.

Marta has given you a notebook with the work she's done so far and a dataset to work with. You can find both in this repository.
You can also find a copy of the notebook on Google Colab [here](https://colab.research.google.com/drive/1ZUg5sAj-nW0k3E5fEcDuDBdQF-IhTQrd?usp=sharing).

The model is good enough; now it's time to build the supporting infrastructure.

### Challenge 1

**Develop an automated pipeline** that trains your model with fresh data, keeping it as sharp as the diamonds it processes. 
Pick the best linear model: do not worry about the xgboost model or hyperparameter tuning. 
Maintain a history of all the models you train and save the performance metrics of each one.

### Challenge 2

Level up! Now you need to support **both models** that Marta has developed: the linear regression and the XGBoost with hyperparameter optimization. 
Be careful. 
In the near future, you may want to include more models, so make sure your pipeline is flexible enough to handle that.

### Challenge 3

Build a **REST API** to integrate your model into a web app, making it a breeze for the team to use. Keep it developer-friendly – not everyone speaks 'data scientist'! 
Your API should support two use cases:
1. Predict the value of a diamond.
2. Given the features of a diamond, return n samples from the training dataset with the same cut, color, and clarity, and the most similar weight.

### Challenge 4

Observability is key. Save every request and response made to the APIs to a **proper database**.

---

## How to run

### Challenge 1-2
Run the Python file main.py located in the /challenge/pipeline folder. Two models will be generated and evaluated using the CSV specified at the path entered in the global variable CSV_PATH declared in main.py. The models are saved in the /challenge/pipeline/models folder and named according to the algorithm used and the timestamp of the training date. In the same folder, there will be a CSV file that reports the models' information and performance.

### Challenge 3
Run the Python file flask_app.py located in the /challenge/app folder. The console will display the URL where a simple HTML page will be accessible. By filling out two forms on this page, you can either predict the value of a diamond or obtain data on a number of similar diamonds (specified by the user) present in the training set. The selected prediction model is the one with the lowest MAE (Mean Absolute Error) score, according to the file /challenge/pipeline/models/models.csv.

A reduced version of the app is also accessible at http://alelily93.eu.pythonanywhere.com/. This version is considered reduced because only linear regression models could be used on PythonAnywhere. Some functionalities of the project are not compatible with the version of XGBoost installed on the hosting platform.

### Challenge 4
Run the flask_app.py file located in the /challenge/app folder, after following these steps:

Create a Database: Launch your MySQL/MariaDB database management console or client and run the diamonds_db_creation.sql script found in the /challenge/app/database folder. This will set up the necessary database.

Configure Environment Variables: Create a .env file in the /challenge/app folder with the following content:

DATABASE_URL = "database_address"
DATABASE_USERNAME = "username"
DATABASE_PASSWORD = "password"
DATABASE_PORT = database_port_number
DATABASE_DIAMONDS = "diamonds_db"
Ensure that the DATABASE_DIAMONDS value matches the database name specified in the SQL script (diamonds_db).

Note: The Flask application will function correctly even without the creation of the database. A message saying "No DB detected" will appear in the Pyhton console, and API requests and responses will not be saved.