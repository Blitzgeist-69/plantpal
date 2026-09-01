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

The strategy behind PlantPal was to build a useful back-end application. The product problem is concrete: indoor plants die when watering is guessed. The application should answer “what should I do today?” in one screen after log in.

The project follows a mobile-first approach so a user can log watering while standing at the sink. Emphasis was placed on clear feedback after every save, private data per account, and a schema that can grow (many care events per plant) without repeating plant details.

Key strategic decisions included:

* Using Django’s built-in `User` model instead of a custom accounts app.
* Storing care events in a related `CareLog` table rather than a single “last watered” field on the plant.
* Calculating “due / overdue” in the view so the database stays normalised.
* Logging care on the plant detail page to avoid extra navigation.
* Deferring photographs until core CRUD and deployment work.

### 2. Scope (Features)

**In Scope**

* Public home page that explains the product before asking for an account
* User registration, login and logout
* Plant CRUD restricted to the owning user
* Search across nickname, species and location
* Care log create form on the plant detail page
* Dashboard of plants due or overdue for watering
* Confirm page before deleting a plant (care history is removed with it)
* Success and error messages after form actions
* Responsive Bootstrap navigation and layouts
* Custom 404 page
* README, TESTING.md, Git history and Heroku deployment
* Secrets stored in `env.py` locally and Heroku Config Vars in production

**Out of Scope**

The following features were considered but deliberately excluded from the current version of the project:

* Email reminders or scheduled notifications
* Sharing a plant collection with another user
* A separate Room entity
* Plant identification from a photograph
* Social features or comments
* Editing or deleting individual care log rows (create-only history in v1)
* Full test suite with pytest / Django TestCase automation (manual testing is documented instead)

These features were deemed out of scope due to time constraints and the need to keep the submission focused on relational CRUD, security and deployment.

**Known Limitations**

* “Needs attention” is based on the most recent care log date plus `water_frequency_days`. It does not distinguish watering from other actions unless that logic is tightened later.
* Photographs depend on Cloudinary being configured. Plants can be saved without an image.
* Heroku’s filesystem is ephemeral. User uploads must not be stored on the dyno.
* The first version does not send email, so a forgotten password flow is not included.

### 3. Structure (Information Architecture)

PlantPal is a multi-page Django application. Each URL renders a server-side template. After a successful POST the user is redirected so the new data is visible immediately.

| Section | Description | Triggered By |
| --- | --- | --- |
| **Navbar** | Logo, Dashboard, My plants, Add plant, account links / log out | Always visible |
| **Home** | Product explanation and register / log in calls to action | Logged-out users at `/` |
| **Register / Login** | Account forms | Nav links or protected-page redirect |
| **Dashboard** | Plants split into Needs attention / Doing fine | `/dashboard/` after login; logged-in users hitting `/` |
| **My plants** | Searchable card grid of the current user’s plants | `/plants/` |
| **Plant detail** | Facts, optional photo, log-care form, care history | `/plants/<id>/` |
| **Add / Edit plant** | Shared plant form | `/plants/add/` and `/plants/<id>/edit/` |
| **Delete confirm** | Warns that care history will be deleted | `/plants/<id>/delete/` |

**Navigation**

* Logged-out nav: PlantPal, Log in, Register.
* Logged-in nav: PlantPal, Dashboard, My plants, Add plant, greeting, Log out.
* On mobile the nav collapses to Bootstrap’s hamburger control.
* Log out is submitted as POST.
* Plant cards and dashboard rows link to the matching detail page.
* Detail pages include a back link to My plants.

**Information Hierarchy**

* Primary focus after login: plants that need care today.
* Secondary focus: the full collection and a dated history per plant.
* Supporting elements: messages under the nav, empty states when a list has no rows, and a delete confirm page so CASCADE deletes are not a surprise.

### 4. Skeleton (Wireframes)

The wireframes were drawn as low-fidelity layouts for the core screens. **Click for full image.**

The wireframes show:

#### Home (logged out)

[![Home wireframe](readme_images/wireframes/previews/home_logged_out_wireframe_preview.png)](readme_images/wireframes/home_logged_out_wireframe.png)

Purpose: A new visitor understands the product in one screen.

* Top bar: PlantPal left; Log in and Register right. No dashboard links.
* Hero: one sentence headline (“Stop guessing when to water”) and one sentence of value.
* One primary button (Create a free account) and one Log in.
* Optional three short feature points under the hero: track plants, log care, see what is due.
* Footer: one line.

#### Log in

[![Log in wireframe](readme_images/wireframes/previews/log_in_wireframe_preview.png)](readme_images/wireframes/log_in_wireframe.png)

Purpose: Account access.

* Same nav as Home.
* Narrow centred column, not full width.
* Register: username, optional email, password, password confirm, Register.
* Login: username, password, Log in, plus “New here? Register”.
* Errors sit above or beside the fields.

#### Dashboard

[![Dashboard wireframe](readme_images/wireframes/previews/dashboard_wireframe_preview.png)](readme_images/wireframes/dashboard_wireframe.png)

Purpose: Answer “what should I do today?”

* Nav: Dashboard, My plants, Add plant plus “Hi, username” and Log out. Current page marked.
* Title Today’s care and a count (“You are tracking 4 plants”).
* Block 1, first: Needs attention (due, overdue, or never logged). Each row is the plant name (link) + short reason.
* Block 2: Doing fine with next due date.
* Empty states: “Nothing is due.” and “Add your first plant.”

#### My plants

[![My plants wireframe](readme_images/wireframes/previews/my_plants_wireframe_preview.png)](readme_images/wireframes/my_plants_wireframe.png)

Purpose: Scan and find.

* Page title left, Add plant button right (always visible).
* Search field + Search button. Placeholder: “Search by name, species or room”.
* Responsive grid: 3 cards on desktop, 2 on tablet, 1 on phone.
* Card content only: nickname (link), species, location, one status line such as “Last watered 3 days ago” or “No care logged”.
* Empty state replaces the grid if the user has zero plants.

#### Plant detail

[![Plant detail wireframe](readme_images/wireframes/previews/plant_detail_wireframe_preview.png)](readme_images/wireframes/plant_detail_wireframe.png)

Purpose: Identity, history and the action of logging care, on one page.

* Back link - All plants.
* Name as h1, species and light as supporting text.
* Facts: location, frequency, last care date, notes.
* Optional image box top-right if time permits, in Cloudinary.
* Edit and Delete as secondary buttons, not hidden in a menu.
* Log care form immediately under the facts: date, action, notes, Save care log.
* Care history table: Date, Action, Notes, newest first.
* Empty history: “No care has been logged yet.”

#### Add / Edit plant

[![Plant form wireframe](readme_images/wireframes/previews/add_edit_plant_wireframe_preview.png)](readme_images/wireframes/add_edit_plant_wireframe.png)

Purpose: One form, two modes.

* Title Add a plant or Edit existing plant.
* Single column. Labels above inputs.
* Fields: nickname, species, location, acquired date, water frequency, light needs, notes, optional photo (time permitting).
* Save primary, Cancel returns to the list (add) or detail (edit).
* Date uses the browser date picker (type="date").

#### Delete confirm

[![Delete confirm wireframe](readme_images/wireframes/previews/delete_confirm_wireframe_preview.png)](readme_images/wireframes/delete_confirm_wireframe.png)

Purpose: Prevent accidental CASCADE deletes.

* Question title: Delete {plant name?}
* One sentence consequence: history will go too and this cannot be undone.
* Yes, delete and Cancel.

#### Mobile

[![Mobile wireframe](readme_images/wireframes/previews/mobile_wireframe_preview.png)](readme_images/wireframes/mobile_wireframe.png)

* Nav becomes a hamburger; logo stays left.
* Dashboard lists stay full width, stacked.
* Plant grid becomes one column.
* Detail: image (if any) stacks above the facts; form fields stay full width.
* Primary buttons full width on phones so they are tappable.

### 5. Surface (Look & Feel)

### Design Choices

* The logged-out home page states the problem before asking for an account.
* The dashboard lists due plants above healthy plants so the urgent work is seen first.
* Plant collections use cards so a growing list can be scanned quickly.
* Care is logged on the detail page so watering does not require a separate URL.
* Status is written in words (“Overdue by 2 days”) as well as any later colour, for accessibility.
* Delete always uses a confirm page because related care logs are removed with the plant.
* A single plant form is reused for create and update to keep the interface consistent.

**Colour and type**

**TBC final colours, fonts etc here.**

| Token | Value | Use |
| --- | --- | --- |
| Primary | *leaf green* | Nav, primary buttons |
| Surface | *off-white* | Page background |
| Text | *near-black* | Body copy |
| Danger | *warm red* | Delete confirm |
| Font | *Google Font* | Headings and body |

## User Stories

Stories are tracked on the following GitHub project:

[PlantPal GitHub Project](https://github.com/users/Blitzgeist-69/projects/8)

Acceptance criteria and tasks are recorded on the issues.

**Must Have (MVP)**

* As a new plant owner, I want to create an account with a username and password so that my plants are saved privately and I can come back later.
* As a registered plant owner, I want to log in and log out so that only I can change my plants on a shared computer.
* As a first-time visitor, I want a clear home page and navigation so that I know PlantPal is a plant-care tracker before I register.
* As a logged-in plant owner, I want to add a plant with a nickname, species and watering frequency so that PlantPal can track that plant.
* As a logged-in plant owner, I want to see all of my plants and search them so that I can find a plant quickly as the collection grows.
* As a logged-in plant owner, I want to open one plant and see its details and care history so that I know how I have been looking after it.
* As a logged-in plant owner, I want to change a plant’s details so that the record stays correct when I move it or learn its real species.
* As a logged-in plant owner, I want to delete a plant I no longer have so that my list stays accurate.
* As a logged-in plant owner, I want to record that I watered, fed or checked a plant so that I have a history and the dashboard can tell me what is due.
* As a logged-in plant owner, I want a dashboard that lists plants that are due or overdue for watering so that I do not have to remember every schedule.
* As a plant owner, I want nobody else to read or change my plants so that my collection stays private.

**Should Have**

* As a plant owner standing at the sink, I want the site to work on a small screen so that I can log watering with one hand.
* As a plant owner, I want a visible success or error message after every save so that I know whether the action worked.

**Could Have**

* As a logged-in plant owner, I want to attach a photo of a plant so that I can recognise it in the list.

## Entity Relationship Diagram

PlantPal uses Django’s built-in `User` plus two project models. Care history is a separate table so a plant can have many dated events without repeating nickname or species.

**Cardinality**

* One user owns many plants. A plant belongs to exactly one user.
* One plant has many care logs. A care log belongs to exactly one plant.
* There is no direct foreign key from `User` to `CareLog`. Logs are reached through the plant.

**Why this shape**

* Owner data lives once on `User`.
* Repeating “last watered” only on `Plant` would lose history and make the dashboard guess.
* `image` is a field (Cloudinary reference).
* Both foreign keys use `on_delete=CASCADE`: deleting a user removes their plants; deleting a plant removes its logs. The delete confirm page tells the user this.

![PlantPal ERD Logical Model](readme_images/tables/plantpal_erd_logical_model.png)


## Data Schema

### USER

![User Data Schema](readme_images/tables/user_entity_table.png)

### PLANT

![Plant Data Schema](readme_images/tables/plant_entity_table.png)

### CARELOG

![Carelog Data Schema](readme_images/tables/carelog_entity_table.png)

**Derived values (not stored)**

* Last care date = latest `CareLog.date` for that plant.
* Due date = last care date + `water_frequency_days` (or “due now” if there is no log).
* Needs attention = due date is today or earlier, or no log exists.

## Security

* `SECRET_KEY`, `DATABASE_URL` and `CLOUDINARY_URL` live in `env.py` locally and in Heroku Config Vars in production. `env.py` is listed in `.gitignore`.
* Production `DEBUG` is `False`.
* Plant and care views require login.
* Queries are scoped to `request.user` (or a helper that 404s if the plant is not owned). Guessing another user’s plant URL returns 404, not the record.
* Passwords are hashed by Django. They are never written to templates or logs on purpose.
* CSRF protection is left on. Logout uses POST.
* Uploaded images go to Cloudinary, not the Heroku dyno disk.

## Technologies Used
* Balsamiq - Wireframes and Tables
* Heroku CLI
* Python 3.12.10
* Django 4.2.3
* Django authentication (`User`, login / logout views)
* Postgres (Code Institute `dbs.ci-dbs.net`)
* dj-database-url
* gunicorn
* WhiteNoise - Static Files
* HTML5
* CSS3 - Styles
* Bootstrap 5 - Layout
* GitHub - Code Repository
* Heroku - Deployment
* VS Code - Development
* W3C Markup Validation Service - Testing
* W3C CSS Validation Service - Testing
* pep8ci / flake8 - Testing
* Chrome DevTools - Testing
* WAVE / Lighthouse - Testing
* Favicon.io
* Cloudinary **TBC**
* Diffchecker.com
* Notepad++
* axe DevTools
* WebAIM Accessibility Contrast checker
* WAVE Web Accessibility Evaluation tool


## Code and Media Attribution

* Bootstrap 5.3
* Font Awesome - icons
* Google Fonts


## Deployment


## Testing

A full record of all testing (user story validation, manual testing, HTML/CSS/Python validators, responsiveness, owner-isolation checks, deployment smoke tests, and bugs encountered and fixed) can be found in the separate **[TESTING.md](./TESTING.md)** file.

## Future Features

**TBC**

