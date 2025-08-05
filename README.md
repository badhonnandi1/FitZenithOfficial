FitZenith: Fitness School Management System
FitZenith is a comprehensive, web-based platform designed to streamline and centralize the operations of a fitness coaching institution. This system supports structured coordination between admins, instructors, and trainees, enabling personalized workout planning, progress tracking, event management, and community engagement—all within a single, cohesive environment.

Whether used by a personal trainer, a fitness academy, or a health-focused community, the system provides an efficient way to manage multiple training programs, monitor trainee performance, and maintain accountability throughout the fitness journey. 

[Note: This project is still in development phase]

Table of Contents
Purpose and Target Users

Key Features

Software Architecture

Technologies Used

Setup and Installation

Application Workflow

Purpose and Target Users
The primary goal of the platform is to enhance the effectiveness of fitness training by offering a centralized, user-friendly solution that overcomes the fragmented communication and inconsistent tracking of traditional tools like WhatsApp and spreadsheets. 

The system is designed for:


Admins: Who oversee program operations, manage system users, and handle event creation and deletion. 

Instructors: Who can guide trainees, assign personalized workout routines, and upload fitness resources. 

Normal Users (Trainees): Who follow customized fitness programs, track their body transformation (BMI, BMR, etc.), and register for fitness events like marathons. 



Key Features

Profile Management: Users can view and update their personal details, including name, phone number, and fitness metrics. The system automatically calculates BMI, BMR, and maintenance calories based on the user's height, weight, and date of birth. 



Event Management: Admins have exclusive rights to create and delete marathon events. Users can browse a list of upcoming marathons and register for any event that has available slots. 


Secure Authentication: Users can register for a new account and log in securely. The system uses a session-based approach to manage user authentication across the application.

Role-Based Access Control: The application enforces a clear separation of abilities between regular users and administrators, ensuring that sensitive actions like event creation are protected.

Software Architecture
The application is built using the 

Model-View-Controller (MVC) architectural pattern to ensure a clean separation of concerns and promote maintainability. 


Model: Manages the application's data structure and business logic. It directly interacts with the MySQL database via SQLAlchemy to handle all data operations.  The core models are 

User, Marathon, and MarathonRegistration.


View: This is the user interface, rendered using HTML templates and the Jinja2 templating engine.  It displays data to the user and captures their interactions.


Controller: Handles the application's logical operations. Implemented using Flask Blueprints, it processes user requests from the View, interacts with the Model, and selects the appropriate View to render in response. 

Technologies Used
The project leverages a modern and robust stack for web development:


Backend: Flask (Python Web Framework) 


Database: MySQL with SQLAlchemy as the ORM 



Frontend: HTML, CSS, and JavaScript 



Template Engine: Jinja2 

Setup and Installation
To get a local copy up and running, follow these simple steps.

Prerequisites

Python 3.10 or onward is completly fine :3

MySQL Server

Installation

Clone the repository:

Bash

git clone https://github.com/your_username/FitZenithOfficial.git
Navigate to the project directory:

Bash

cd FitZenithOfficial
Create and activate a virtual environment:

Bash

python -m venv env
source env/bin/activate  # On Windows, use `env\Scripts\activate`
Install the required packages:

Bash

pip install -r requirements.txt
Set up your database connection in app/__init__.py.

Run the application:

Bash

python run.py
Application Workflow
The application is started by executing the run.py file. This initializes the Flask app using the create_app factory in app/__init__.py, which sets up the database, registers all route blueprints, and creates the necessary database tables. The default landing page (index.html) is served, from which users can navigate to log in, register, or browse public content.