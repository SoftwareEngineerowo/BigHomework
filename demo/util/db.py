from django.db import connection


def updateSQL(update_sql, select_sql):
    with connection.cursor() as cursor:
        print(">>> update sql::update_sql: ", update_sql)
        cursor.execute(update_sql)
        cursor.execute(select_sql)
        row = cursor.fetchone()

    return row
