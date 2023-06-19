from flask import Flask, render_template
import json
import psycopg2
import datetime

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
    instance_schedule = []
    try:
        cursor = conn.cursor()
        query = "SELECT instance_id, shutdown_time FROM {}".format(scheduler_table)
        cursor.execute(query)
        rows = cursor.fetchall()

        if rows:
            for row in rows:
                instance_id, shutdown_time = row
                instance_schedule.append({
                    "instance_id": instance_id,
                    "shutdown_time": str(shutdown_time)
                })

    except Exception as e:
        print("An error occurred while retrieving the scheduling:", str(e))

    finally:
        if cursor:
            cursor.close()

    return instance_schedule

scheduling_data = get_scheduling()

json_data = json.dumps(scheduling_data)

print(json_data)



def create_scheduling(instance_id, shutdown_time):
    try:
        cursor = conn.cursor()

        # Check if shutdown_time is already in the expected format
        if not isinstance(shutdown_time, str):
            print("Invalid shutdown time format for instance {}. Please check the time format.".format(instance_id))
            return

        query = "SELECT instance_id, shutdown_time FROM {} WHERE instance_id = %s".format(scheduler_table)
        cursor.execute(query, (instance_id,))
        existing_instance = cursor.fetchone()

        if existing_instance:
            existing_shutdown_time = existing_instance[1]
            if existing_shutdown_time is None:
                print("Instance {} already has a shutdown time set as null.".format(instance_id))
            else:
                update_query = "UPDATE {} SET shutdown_time = %s WHERE instance_id = %s".format(scheduler_table)
                cursor.execute(update_query, (shutdown_time, instance_id))
                print("Instance {} shutdown time was updated to {}".format(instance_id, shutdown_time))
        else:
            insert_query = "INSERT INTO {} (instance_id, shutdown_time) VALUES (%s, %s)".format(scheduler_table)
            cursor.execute(insert_query, (instance_id, shutdown_time))
            print("Instance {} will be scheduled for shutdown every day at {}".format(instance_id, shutdown_time))

        # Insert log entry
        log_timestamp = datetime.datetime.now()
        log_query = "INSERT INTO {} (instance_id, log_timestamp) VALUES (%s, %s)".format(log_table)
        cursor.execute(log_query, (instance_id, log_timestamp))

        conn.commit()

    except Exception as e:
        print("An error occurred while creating the scheduling:", str(e))
        conn.rollback()

    finally:
        if cursor:
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

        # Log the scheduling deletion
        log_timestamp = datetime.now()
        instancename = get_instance_name(instance_id)  # Replace with your logic to get the instance name
        log_query = "INSERT INTO {} (instance_id, log_timestamp, instancename) VALUES (%s, %s, %s)".format(log_table)
        cursor.execute(log_query, (instance_id, log_timestamp, instancename))

        conn.commit()

    except Exception as e:
        print("An error occurred while deleting the scheduling:", str(e))
        conn.rollback()

    finally:
        if cursor:
            cursor.close()


# Rollback the current transaction explicitly
def rollback_transaction():
    conn.rollback()


# Close the connection when it's no longer needed
def close_connection():
    conn.close()
