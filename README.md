# Analyzing Twitter Data SLS

This project is designed to analyze Twitter data using FastAPI and PostgreSQL. The data includes tweets and popular hashtags, which are loaded from text files and stored in a PostgreSQL database. The project demonstrates how to build a simple RESTful API with FastAPI to manage and query the Twitter data.

## Project Structure

```
analyzing_twitter_data_sls/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── database.py
│   ├── utils.py
│
├── routers/
│   ├── q2.py
│
├── .env
├── requirements.txt
├── popular_hashtags.txt
├── query2_ref.txt
└── README.md
```

## Installation

### Prerequisites

- Python 3.8 or higher
- PostgreSQL
- `virtualenv` for creating a virtual environment

### Steps

1. Clone the Repository

    ```
    git clone https://github.com/yschristian/analyzing_twitter_data_sls.git
    cd analyzing_twitter_data_sls
    
    ```

2. Create and Activate Virtual Environment

    ```
    python -m venv venv
    venv\Scripts\activate 

    ```

3. Install Dependencies

    ```
    pip install -r requirements.txt

    ```

4. Configure PostgreSQL

    Ensure you have PostgreSQL installed and running. Create a database named `twitter`.

    ```sql
    CREATE DATABASE twitter;
    ```

5. Set Up Environment Variables

    Create a `.env` file in the root directory with the following content:

    ```
    DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost/twitter
    ```

    Replace `YOUR_PASSWORD` with your PostgreSQL password.

## Usage

1. Run the Application

    ```
    uvicorn app.main:app --reload
    ```

2. Load Data

   to load the data from `query2_ref.txt` and `popular_hashtags.txt` into the PostgreSQL database.

    ```
      python etl.py 
    ```

3. API Endpoints

   - `GET /q2?user_id={user_id}&type={type}&phrase={phrase}&hashtag={hashtag}` 

## Project Components

- FastAPI: A modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.
- SQLAlchemy: The Python SQL toolkit and Object-Relational Mapping (ORM) library.
- PostgreSQL: An open-source relational database management system emphasizing extensibility and SQL compliance.


