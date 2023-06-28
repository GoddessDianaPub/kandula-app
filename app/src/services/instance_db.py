import psycopg2
import logging

#instance_schedule = {
#    "instances": []
#}

log = logging.getLogger()
logging.basicConfig(level=logging.INFO)

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

#get_query = 'SELECT * FROM instances_scheduler'
conn.autocommit = True
cursor = conn.cursor()


def get_scheduling():
    instance_schedule = []
    get_query = "SELECT instance_id, shutdown_time FROM instances_scheduler"
    try:
        cursor.execute(get_query)
        rows = cursor.fetchall()
        for r in rows:
            try:
                instance_id, shutdown_time = r
                instance_schedule.append({"instance_id": instance_id, "shutdown_time": shutdown_time})
            except Exception:
                log.error("Error parsing data: %s", r)
        return instance_schedule
    except psycopg2.Error as error:
        log.error("Error retrieving data from the database: %s", error)


def create_scheduling(instance_id, shutdown_hour):
    cursor.execute("INSERT INTO instances_scheduler (instance_id, shutdown_time) VALUES (%s, %s)", (instance_id, shutdown_hour))
    try:
        index = next((i for i, inst in enumerate(instance_schedule["instances_scheduler"]) if inst["instance_id"] == instance_id))
        instance_schedule["instances_scheduler"][index] = {"instance_id": instance_id, "shutdown_time": shutdown_hour}
        log.info("Instance %s will be shutdown, updated to the hour %s", instance_id, shutdown_hour)
    except StopIteration:
        instance_schedule["instances_scheduler"].append({"instance_id": instance_id, "shutdown_time": shutdown_hour})
        log.info("Instance %s will be shutdown every day at %s", instance_id, shutdown_hour)


def delete_scheduling(instance_id):
    cursor.execute("DELETE FROM instances_scheduler WHERE instance_id = %s", (instance_id,))
    try:
        index = next((i for i, inst in enumerate(instance_schedule["instances_scheduler"]) if inst["instance_id"] == instance_id))
        instance_schedule["instances_scheduler"].pop(index)
        log.info("Instance %s was removed from scheduling", instance_id)
    except StopIteration:
        instance_schedule["instances_scheduler"].pop(index)
        log.info("Instance %s was not there to begin with", instance_id)

#def close_connection():
#    conn.close()
