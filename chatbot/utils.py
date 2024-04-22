import sqlvalidator
import sqlparse
import json


# Helper functions
def is_valid_sql(string):
    valid = False
    sv_parsed = sqlvalidator.parse(string)
    sp_parsed = sqlparse.parse(string)
    sv_valid = sv_parsed.is_valid()
    sql_type = sp_parsed[0].get_type()
    if sql_type in ["CREATE", "DELETE", "INSERT"]:
        valid = True
    if sql_type == "SELECT":
        valid = sv_valid
    return valid


def validate_query(query):
    query = query.strip().upper()

    valid_query_types = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'CREATE', 'SHOW', 'DESCRIBE', 'DESC']
    query_type = None

    for valid_type in valid_query_types:
        if query.startswith(valid_type):
            query_type = valid_type
            break

    if query_type is None:
        return False, None

    # If the query starts with 'DESCRIBE' or 'DESC', normalize it to 'DESCRIBE'
    if query_type == 'DESC':
        query_type = 'DESCRIBE'

    return True, query_type


def load_questions():
    with open("questions.json", "rb") as f:
        question_data = json.load(f)

    questions = {}
    for item in question_data:
        question = item['question']
        query = item['query']
        questions[question] = query

    return questions
