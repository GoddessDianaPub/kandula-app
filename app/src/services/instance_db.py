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


def get_scheduling():
    conn = psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password
    )
    
    cursor = conn.cursor()
    
    query = "SELECT instance_id, scheduled_hours FROM scheduler_table"
    cursor.execute(query)
    
    rows = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
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
    # TODO: Implement a DB insert that creates the instance ID and the chosen hour in DB  
    conn = psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password
    )
    
    try:
        cursor = conn.cursor()

        query = "SELECT instance_id FROM scheduler_table WHERE instance_id = %s"
        cursor.execute(query, (instance_id,))
        existing_instance = cursor.fetchone()

        if existing_instance:
            update_query = "UPDATE scheduler_table SET scheduled_hours = %s WHERE instance_id = %s"
            cursor.execute(update_query, (shutdown_hour, instance_id))

            print("Instance {} will be shutdown was updated to the hour {}".format(instance_id, shutdown_hour))
        else:
            insert_query = "INSERT INTO scheduler_table (instance_id, scheduled_hours) VALUES (%s, %s)"
            cursor.execute(insert_query, (instance_id, shutdown_hour))

            print("Instance {} will be shutdown every day when the hour is {}".format(instance_id, shutdown_hour))

        conn.commit()

    except Exception:
        print("An error occurred while creating the scheduling.")

    finally:
        cursor.close()
        conn.close()


def delete_scheduling(instance_id):
    # TODO: Implement a delete query to remove the instance ID from scheduling
    conn = psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password
    )

    try:
        cursor = conn.cursor()

        query = "SELECT instance_id FROM scheduler_table WHERE instance_id = %s"
        cursor.execute(query, (instance_id,))
        existing_instance = cursor.fetchone()

        if existing_instance:

            delete_query = "DELETE FROM scheduler_table WHERE instance_id = %s"
            cursor.execute(delete_query, (instance_id,))

            print("Instance {} was removed from scheduling".format(instance_id))
        else:
            print("Instance {} was not found in the scheduling".format(instance_id))

        conn.commit()

    except Exception:
        print("An error occurred while deleting the scheduling.")

    finally:
        cursor.close()
        conn.close()
