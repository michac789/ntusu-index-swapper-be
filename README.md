# NTUSU Backend - Index Swapper MVP

Simple backend for the NTUSU Index Swapper MVP. For frontend devs, please refer to the steps below to run the server successfully.

## How to Run (for frontend devs)

Prerequisities:

- Python >3.9
- Pip
- Git
- VS Code (recommended)

1. Clone the repository

    ```powershell
    git clone https://github.com/michac789/ntusu-index-swapper-be.git
    ```

2. Change your directory inside of the project

    ```powershell
    cd path/to/ntusu-index-swapper-be
    ```

3. Install dependencies

   ```powershell
   git install -r requirements.txt
   ```

   You may want to use conda or venv to create a virtual environment for this project.

4. Migrate database

   ```powershell
   python manage.py migrate
   ```

5. Load sample data

   Sample data will provides you will all of this:
   - A superuser account (username: superuser), and 5 regular accounts (username: user1, user2, user3, user4, user5), password are all '123'
   - Sample course indexes (33 indexes across 3 different courses)

   Please refer to the `fixtures` folder for the detail of the sample data.

   ```powershell
   python manage.py loaddata sample_user.json
   python manage.py loaddata sample_course_index_small.json
   ```

   Note: Please run the above command in order!
   Also, run this command only once when you first setup the project.
   If you have added additional data, running this may cause an error.
   In that case, you might consider resetting the database before loading the sample data.

6. Run server

   ```powershell
   python manage.py runserver
   ```

   The server should be running on `localhost:8000` by default.

   You can visit Django admin page at `localhost:8000/admin` and login with the superuser account.

   You can see the API documentation at `localhost:8000/swagger` and test the API needed there.
