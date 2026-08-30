# PlantPal

## Introduction

PlantPal is a full-stack web application that helps people look after indoor plants. Users create an account, add each plant they own, record care actions such as watering, and see a dashboard of which plants are due or overdue.

The project is built with Django, a relational Postgres database, custom HTML/CSS with Bootstrap 5, and is deployed on Heroku. Secrets are kept out of version control. Optional plant photographs can be stored on Cloudinary.

**Hero Image**

![Hero Image](docs/screenshots/hero-image.png) **TBC**

**Live Site:** [**TBC** Heroku URL here]

## Contents

* [Project Description](#project-description)
* [UX Design - The 5 Planes](#ux-design---the-5-planes)
  * [1. Strategy (Project Goals)](#1-strategy-project-goals)
  * [2. Scope (Features)](#2-scope-features)
  * [3. Structure (Information Architecture)](#3-structure-information-architecture)
  * [4. Skeleton (Wireframes)](#4-skeleton-wireframes)
  * [5. Surface (Look & Feel)](#5-surface-look--feel)
* [User Stories](#user-stories)
* [Entity Relationship Diagram](#entity-relationship-diagram)
* [Data Schema](#data-schema)
* [Security](#security)
* [Technologies Used](#technologies-used)
* [Code and Media Attribution](#code-and-media-attribution)
* [Deployment](#deployment)
* [Testing](#testing)
* [Future Features](#future-features)


## Project Description

PlantPal is designed for people who keep houseplants and need to keep track of watering and care. The app stores each plant with its own watering frequency and builds a dated care history. The dashboard uses that history to list plants that need attention today.

Key Features:

* User registration, log in and log out
* Create, read, update and delete plants owned by the logged-in user
* Search plants by nickname, species or room
* Log care actions (water, fertilize, prune, repot, check, other) against a plant
* Dashboard that splits plants into “Needs attention” and “Doing fine”
* Owner isolation so one user cannot view or change another user’s plants
* Responsive layout for mobile, tablet and desktop
* Optional plant photographs stored on Cloudinary

The project was developed using Python, Django, HTML5, CSS3 (with Bootstrap 5), and a small amount of third-party JavaScript from Bootstrap. Data is stored in Postgres (Code Institute database) in production, with SQLite available for locally if needed for testing. The application is deployed on Heroku with WhiteNoise serving static files.

This project showcases core back-end and full-stack skills including:

* Relational data modelling and migrations
* CRUD against related models
* Authentication and object-level authorisation
* Template inheritance and server-rendered UX
* Environment variables and production configuration
* Cloud deployment
* Accessibility and documentation

**Live Site:**

[**TBC** Heroku URL here]

**GitHub Repo:**

https://github.com/Blitzgeist-69/plantpal

## UX Design - The 5 Planes

### 1. Strategy (Project Goals)



### 2. Scope (Features)



### 3. Structure (Information Architecture)



### 4. Skeleton (Wireframes)



#### Home (logged out)



#### Log in



#### Dashboard




#### My plants




#### Plant detail




#### Add / Edit plant




#### Delete confirm




#### Mobile




### 5. Surface (Look & Feel)

### Design Choices


## User Stories


## Entity Relationship Diagram


## Data Schema


### USER


### PLANT


### CARELOG


## Security


## Technologies Used


## Code and Media Attribution


## Deployment


## Testing

A full record of all testing (user story validation, manual testing, HTML/CSS/Python validators, responsiveness, owner-isolation checks, deployment smoke tests, and bugs encountered and fixed) can be found in the separate **[TESTING.md](./TESTING.md)** file.

## Future Features



