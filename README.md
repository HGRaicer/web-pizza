# Pizza Delivery Web App

## Overview
This project is a collaborative effort by four students from Moscow Aviation Institute. The aim of this project is to develop a pizza delivery web application using Flask, Python, and PostgreSQL. We planned to add to our web-site not only the basic functions of such applications, but also more complex ones, such as the ability to give the user the administrator role so that he can edit information about goods and view the full order history.

## Features
- *User Authentication*: Allow users to create accounts, log in, and log out.
- *Menu Management*: Admins can manage the menu, including adding, updating, and deleting items.
- *Order Placement*: Users can browse the menu and place orders.
- *Order Tracking*: Users can track the status of their orders.
- *Admin Dashboard*: Admins have access to a dashboard to manage orders and view analytics.
- *Маp integration*: the ability to choose a delivery location using a card

## Technologies Used
- *Flask*: Python web framework for building the application.
- *PostgreSQL*: Database management system for storing application data.
- *HTML/CSS/JavaScript*: Frontend development for the user interface.
- *Third-Party Libraries*: SQLAlchemy

## Testing Strategy
To ensure the reliability and functionality of the application, we will implement a comprehensive testing strategy.
  
## Setup Instructions
1. Clone the repository: git clone https://github.com/HGRaicer/web-pizza.git
2. Install dependencies: pip install -r requirements.txt
3. Set up the PostgreSQL database:
    a) Install the PostgreSQL from the official website: https://www.postgresql.org/
    b) During installation, select the host number 5432 and set the password 1234. If you have selected a different password or host, replace the corresponding fields on line 12 of the code __init__.py on their own values.
    с) Log into the PostgreSQL. Press the space bar until you are asked to enter your password. Write a command CREATE DATABASE web-pizza.
5. Install the necessary libraries for python.
6. Go to the repository folder using Visuas Studio Code or other programs and write the following commands in the python console: flask db init ; flack db migrate ; flask db upgrade .
7. Launch run.py and follow the link displayed in the console.

## Contact
For any inquiries or feedback, please contact us in Telegram: @HGRaicer
