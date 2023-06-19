import psycopg2
from datetime import datetime, timedelta

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
    query = f"SELECT instance_id FROM {schema}.{scheduler_table}"
    cursor.execute(query)
    instance_ids = cursor.fetchall()
    cursor.close()
    return [instance_id[0] for instance_id in instance_ids]

def create_scheduling(instance_id, shutdown_hour):
    cursor = conn.cursor()
    current_time = datetime.now()
    shutdown_time = datetime.combine(current_time.date(), shutdown_hour)
    if shutdown_time < current_time:
        shutdown_time += timedelta(days=1)  # Schedule for the next day
    query = f"INSERT INTO {schema}.{scheduler_table} (instance_id, shutdown_time) VALUES (%s, %s)"
    cursor.execute(query, (instance_id, shutdown_time))
    conn.commit()
    cursor.close()

def delete_scheduling(instance_id):
    cursor = conn.cursor()
    query = f"DELETE FROM {schema}.{scheduler_table} WHERE instance_id = %s"
    cursor.execute(query, (instance_id,))
    conn.commit()
    cursor.close()

conn.close()
