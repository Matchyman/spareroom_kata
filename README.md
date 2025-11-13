# Checkout Implementation

## Backend:

Make sure you have uv installed

uv venv --no-cache --python 3.11

.venv/Scripts/activate

uv sync (will install all required packages for backend)

python ./main.py will start api backend

## Frontend:

cd into frontend

npm install

Vite requires Node.js version 20.19+ or 22.12+

npm run will start frontend


## Database:

Database is SQLite db, if you wish to change the data, change csv's located in src/backend/database

Delete db and run db_setup.py
