"""
SQL Injection Examples
----------------------
Contains unsafe patterns (to be detected) and safe alternatives.
Use this file to test the security agent's ability to flag raw SQL
and recommend parameterized queries / ORM usage.
"""

# ----- Unsafe examples (should be flagged) -----
def unsafe_concat(cursor, user_input: str):
    # Unsafe: string concatenation / interpolation into SQL
    # If user_input contains: "'; DROP TABLE users; --" this is dangerous.
    query = "SELECT * FROM users WHERE name = '" + user_input + "';"
    return cursor.execute(query)


def unsafe_fstring(cursor, user_input: str):
    # Unsafe: f-string directly embedding user input
    query = f"SELECT id, email FROM users WHERE email = '{user_input}'"
    return cursor.execute(query)


def unsafe_format(cursor, user_input: str):
    # Unsafe: format into query string
    query = "UPDATE accounts SET balance = balance - 100 WHERE owner = '{}'".format(user_input)
    return cursor.execute(query)


# ----- Slightly safer (still risky if used incorrectly) -----
def semi_safe(cursor, user_input: str):
    # Using Python string replacement is still risky unless you validate/escape input properly.
    q = "SELECT * FROM sessions WHERE token = '%s'" % user_input
    return cursor.execute(q)


# ----- Safe examples (should NOT be flagged) -----
def safe_parameterized(cursor, user_input: str):
    # Parameterized query with DB-API placeholders (example for psycopg2: %s)
    query = "SELECT * FROM users WHERE name = %s"
    return cursor.execute(query, (user_input,))


def safe_named_parameters(cursor, user_input: str):
    # Example for named parameters (e.g., sqlite3 uses ? placeholders; some drivers support :name)
    query = "SELECT * FROM orders WHERE order_id = :order_id"
    return cursor.execute(query, {"order_id": user_input})


# ----- ORM example (preferred for many cases) -----
def orm_example(session, user_input: str):
    # Example using SQLAlchemy ORM (safer when used correctly)
    # from model import User
    # return session.query(User).filter(User.name == user_input).all()
    # (This is pseudocode for demonstration.)
    return session.query("User").filter_by(name=user_input).all()


# ----- Demonstration runner (not executed during analysis) -----
if __name__ == "__main__":
    # NOTE: These calls are placeholders to show usage; they won't run without a DB/cursor.
    fake_cursor = None
    fake_session = None
    user = "alice"

    # Unsafe (should be flagged)
    # unsafe_concat(fake_cursor, user)
    # unsafe_fstring(fake_cursor, user)

    # Safe (recommended)
    # safe_parameterized(fake_cursor, user)
    # orm_example(fake_session, user)
