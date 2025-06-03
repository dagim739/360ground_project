# 🗓️ 360Ground Event Management System

A modern, lightweight event management system built with **Django** (backend), **HTMX** (frontend interactivity), and **SQLite** (database). The app supports **one-time and recurring events**, user **login/registration**, and the ability to **add, edit, and delete events** via a clean, dynamic UI.

---

## ⚙️ Setup

###  Requirements

- Docker and Docker Compose
- GNU Make (for command shortcuts)

### 📦 Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/360groundproject.git
   cd 360groundproject


2. Build the docker image
    ```bash
    make build

3. Make migrations
    ```bash
    make migrate



## Run

1. Start the development server:
    ```bash
    make start

2. To stop the server:
    ```bash
    make stop





## Architectural Decisions

### Backend Django
    Built with Django 5.2.1

    Models represent events and user accounts

    Authentication via Django’s built-in auth system

### Event System
    Supports both one-time and recurring events

    Recurrence logic handled in models and forms


###Frontend:HTMX
    HTMX is used for interactive front-end behaviors:

    Inline event editing

    Modal-based forms

    Partial page updates (e.g., adding/deleting without full page reloads)

###Database:SQLite

    Uses SQLite for simplicity in development

    Can be replaced with PostgreSQL for production



##Shortcuts

| Command                | Description                       |
| ---------------------- | --------------------------------- |
| `make build`           | Build the Docker container        |
| `make start`           | Start the app at `localhost:8000` |
| `make stop`            | Stop the app                      |
| `make migrate`         | Run database migrations           |
| `make createsuperuser` | Create an admin user              |
| `make shell`           | Open bash shell in container      |


## Features
📝 Add, edit, and delete events

🔁 Supports recurring events (daily, weekly, monthly)

🔐 User login and registration

⚡ Dynamic UI via HTMX for better UX