import psycopg2
from datetime import datetime

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


def get_instance_name(instance_id):
    # Replace with your logic to get the instance name based on the instance_id
    pass


def get_scheduling():
    try:
        cursor = conn.cursor()
        query = "SELECT instance_id, scheduled_hours FROM {}".format(scheduler_table)
        cursor.execute(query)
        rows = cursor.fetchall()

        # Prepare the result in JSON format
        instance_schedule = []
        if rows:
            for row in rows:
                instance_id, scheduled_hours = row
                instance_schedule.append({
                    "instance_id": instance_id,
                    "scheduled_hours": scheduled_hours
                })

        return instance_schedule

    except Exception as e:
        print("An error occurred while retrieving the scheduling:", str(e))

    finally:
        if cursor:
            cursor.close()



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

        # Log the scheduling creation
        log_timestamp = datetime.now()
        instancename = get_instance_name(instance_id)  # Replace with your logic to get the instance name
        log_query = "INSERT INTO {} (instance_id, log_timestamp, instancename) VALUES (%s, %s, %s)".format(log_table)
        cursor.execute(log_query, (instance_id, log_timestamp, instancename))

        conn.commit()

    except Exception as e:
        print("An error occurred while creating the scheduling:", str(e))
        conn.rollback()

    finally:
        if cursor:
            cursor.close()


def create_scheduling(instance_id, shutdown_hour):
    # TODO: Implement a DB insert that creates the instance ID and the chosen hour in DB
    try:  # update
        index = [i['Id'] for i in instance_schedule["Instances"]].index(instance_id)
        instance_schedule["Instances"][index] = {"Id": instance_id, "DailyShutdownHour": int(shutdown_hour[0:2])}
        print("Instance {} will be shutdown was updated to the hour {}".format(instance_id, shutdown_hour))
    except Exception:  # insert
        instance_schedule["Instances"].append({"Id": instance_id, "DailyShutdownHour": int(shutdown_hour[0:2])})
        print("Instance {} will be shutdown every day when the hour is {}".format(instance_id, shutdown_hour))


def delete_scheduling(instance_id):
    # TODO: Implement a delete query to remove the instance ID from scheduling
    try:
        index = [k['Id'] for k in instance_schedule["Instances"]].index(instance_id)
        instance_schedule["Instances"].pop(index)
        print("Instance {} was removed from scheduling".format(instance_id))
    except Exception:
        print("Instance {} was not there to begin with".format(instance_id))
