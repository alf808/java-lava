# Java Lava Cafe Full Stack

## Full Stack API auth - IAM Final Project

A new digitally enabled cafe will be opened to order drinks, socialize, and study hard. It need helps setting up their menu experience.

This project demonstrates skills to create a full stack drink menu application. The application must:

1. Display graphics representing the ratios of ingredients in each drink.
2. Allow public users to view drink names and graphics.
3. Allow the shop baristas to see the recipe information.
4. Allow the shop managers to create new drinks and edit existing drinks.

## Tasks

There are `@TODO` comments throughout the project. We recommend tackling the sections in order. Start by reading the READMEs in:

1. [`./backend/`](./backend/README.md)
2. [`./frontend/`](./frontend/README.md)

## About the Stack

The full stack application is designed with some key functional areas:

### Backend

The `./backend` directory contains Flask server with SQLAlchemy module to simplify your data needs. Please see backend README to see the endpoints. This application integrate third-party Auth0.com for authentication.

[View the README.md within ./backend for more details.](./backend/README.md)

### Frontend

The `./frontend` directory contains an Ionic frontend to consume the data from the Flask server. The environment variables found within (./frontend/src/environment/environment.ts) are updated to reflect the Auth0 configuration details set up for the backend app.

[View the README.md within ./frontend for more details.](./frontend/README.md)
