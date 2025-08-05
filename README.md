#  FitZenith: Fitness School Management System

**FitZenith** is a comprehensive, web-based platform designed to streamline and centralize the operations of a fitness coaching institution. This system enables structured coordination between **admins**, **instructors**, and **trainees**, supporting features like personalized workout planning, progress tracking, event management, and community engagement all in one cohesive platform.

>  **Note:** This project is currently under active development.

---

## Table of Contents

- [ Purpose and Target Users](#-purpose-and-target-users)
- [ Key Features](#-key-features)
- [ Software Architecture](#-software-architecture)
- [ Technologies Used](#-technologies-used)
- [ Setup and Installation](#-setup-and-installation)
- [ Application Workflow](#-application-workflow)

---

## Purpose and Target Users

The main goal of FitZenith is to **enhance the effectiveness of fitness training** by providing a centralized, user-friendly platform that solves issues related to fragmented communication and inconsistent tracking via traditional tools (like WhatsApp and spreadsheets).

### Target Users:

- **Admins**: Manage users, programs, and create/delete events.
- **Instructors**: Guide trainees, assign workouts, and upload resources.
- **Trainees (Normal Users)**: Follow customized fitness plans, track metrics (BMI, BMR), and register for fitness events.

---

##  Key Features :3

###  Profile Management
- View and update personal details (name, phone number, fitness stats).
- Auto-calculation of **BMI**, **BMR**, and **maintenance calories**.

###  Event Management
- **Admins only** can create/delete marathon events.
- Users can view upcoming events and register for available slots.

###  Secure Authentication
- Session-based login/logout system with account registration.

###  Role-Based Access Control
- Different views and permissions for admins, instructors, and users.

---

##  Software Architecture

FitZenith follows the **Model-View-Controller (MVC)** pattern for better maintainability and separation of concerns:

- **Model**: Manages database structure and business logic using SQLAlchemy.
- **View**: HTML templates powered by **Jinja2** to render the user interface.
- **Controller**: Flask routes and Blueprints process requests, interact with models, and serve views.

---

##  Technologies Used

| Layer        | Technology                    |
|--------------|-------------------------------|
| Backend      | Flask (Python Web Framework)  |
| Database     | MySQL + SQLAlchemy      |
| Frontend     | HTML, CSS, JavaScript         |
| Templates    | Jinja2                        |

---

###  Prerequisites
- Python 3.10+
- MySQL Server installed and running

## Any kind of suggestions is welcome
