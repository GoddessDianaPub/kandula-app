import psycopg2
import json

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

# Rest of your code...

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
                    "shutdown_time": str(shutdown_time)  # Convert time to string
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
        query = "SELECT instance_id FROM {} WHERE instance_id = %s".format(scheduler_table)
        cursor.execute(query, (instance_id,))
        existing_instance = cursor.fetchone()

        if existing_instance:
            update_query = "UPDATE {} SET scheduled_hours = %s WHERE instance_id = %s".format(scheduler_table)
            cursor.execute(update_query, (shutdown_time, instance_id))

            print("Instance {} will be shutdown was updated to the hour {}".format(instance_id, shutdown_time))
        else:
            insert_query = "INSERT INTO {} (instance_id, scheduled_hours) VALUES (%s, %s)".format(scheduler_table)
            cursor.execute(insert_query, (instance_id, shutdown_time))

            print("Instance {} will be shutdown every day when the hour is {}".format(instance_id, shutdown_time))

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
