import psycopg2

# Variables
host = "rds-db-instance-0.cihzevxi90ql.us-east-1.rds.amazonaws.com"
port = 5432
schema = "kandula"
database = "kandula"
scheduler_table = "instances_scheduler"
log_table = "instances_shutdown_log"
user = "kandula"
password = "Aa123456!"

conn = psycopg2.connect(
    host=host,
    port=port,
    database=database,
    user=user,
    password=password
)


def get_scheduling():
    cursor = conn.cursor()

    query = "SELECT instance_id, scheduled_hours FROM {}".format(scheduler_table)
    cursor.execute(query)

    rows = cursor.fetchall()

    cursor.close()

    # Prepare the result in JSON format
    instance_schedule = []
    for row in rows:
        instance_id, scheduled_hours = row
        instance_schedule.append({
            "instance_id": instance_id,
            "scheduled_hours": scheduled_hours
        })

    return instance_schedule


def create_scheduling(instance_id, shutdown_hour):
    try:
        cursor = conn.cursor()

        query = "SELECT instance_id FROM {} WHERE instance_id = %s".format(scheduler_table)
        cursor.execute(query, (instance_id,))
        existing_instance = cursor.fetchone()

        if existing_instance:
            update_query = "UPDATE {} SET scheduled_hours = %s WHERE instance_id = %s".format(scheduler_table)
            cursor.execute(update_query, (shutdown_hour, instance_id))

            print("Instance {} will be shutdown was updated to the hour {}".format(instance_id, shutdown_hour))
        else:
            insert_query = "INSERT INTO {} (instance_id, scheduled_hours) VALUES (%s, %s)".format(scheduler_table)
            cursor.execute(insert_query, (instance_id, shutdown_hour))

            print("Instance {} will be shutdown every day when the hour is {}".format(instance_id, shutdown_hour))

        conn.commit()

    except Exception:
        print("An error occurred while creating the scheduling.")

    finally:
        cursor.close()


def delete_scheduling(instance_id):
    try:
        cursor = conn.cursor()

        query = "SELECT instance_id FROM {} WHERE instance_id = %s".format(scheduler_table)
        cursor.execute(query, (instance_id,))
        existing_instance = cursor.fetchone()

        if existing_instance:
            delete_query = "DELETE FROM {} WHERE instance_id = %s".format(scheduler_table)
            cursor.execute(delete_query, (instance_id,))

            print("Instance {} was removed from scheduling".format(instance_id))
        else:
            print("Instance {} was not found in the scheduling".format(instance_id))

        conn.commit()

    except Exception:
        print("An error occurred while deleting the scheduling.")

    finally:
        cursor.close()


# Close the connection when it's no longer needed
def close_connection():
    conn.close()
