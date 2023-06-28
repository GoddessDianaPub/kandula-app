import psycopg2
import logging


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
        instance_schedule = get_scheduling()
        index = next((i for i, inst in enumerate(instance_schedule) if inst["instance_id"] == instance_id), None)
        if index is not None:
            instance_schedule[index]["shutdown_time"] = shutdown_hour
            log.info("Instance %s will be shutdown, updated to the hour %s", instance_id, shutdown_hour)
        else:
            instance_schedule.append({"instance_id": instance_id, "shutdown_time": shutdown_hour})
            log.info("Instance %s will be shutdown every day at %s", instance_id, shutdown_hour)
    except StopIteration:
        instance_schedule.append({"instance_id": instance_id, "shutdown_time": shutdown_hour})
        log.info("Instance %s will be shutdown every day at %s", instance_id, shutdown_hour)



def delete_scheduling(instance_id):
    cursor.execute("DELETE FROM instances_scheduler WHERE instance_id = %s", (instance_id,))
    try:
        index = [k['instance_id'] for k in instance_schedule["instances_scheduler"]].index(instance_id)
        instance_schedule["instances_scheduler"].pop(index)
        log.info("Instance {} was removed from scheduling".format(instance_id))
    except Exception:
        log.info("Instance {} was not there to begin with".format(instance_id))