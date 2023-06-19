import psycopg2
import boto3

# Database connection details
host = "rds-db-instance-0.cihzevxi90ql.us-east-1.rds.amazonaws.com"
port = 5432
schema = "kandula"
database = "kandula"
scheduler_table = "instances_scheduler"
user = "kandula"
password = "Aa123456!"

con = psycopg2.connect(
    host=host,
    port=port,
    database=database,
    user=user,
    password=password
)

# Function to retrieve instance IDs and update the scheduler table
def update_scheduler_table(con):
    try:
        session = boto3.Session()
        ec2_client = session.client("ec2")

        filters = [{"Name": "tag-key", "Values": ["Stop"]}]
        instances = ec2_client.describe_instances(Filters=filters)

        instance_data = []
        for reservation in instances["Reservations"]:
            for instance in reservation["Instances"]:
                instance_id = instance["InstanceId"]
                shutdown_time = None
                for tag in instance["Tags"]:
                    if tag["Key"] == "Stop":
                        shutdown_time = tag["Value"]
                        break
                instance_data.append((instance_id, shutdown_time))

        cur = con.cursor()
        cur.executemany("INSERT INTO {}.{} (instance_id, shutdown_time) VALUES (%s, %s) "
                        "ON CONFLICT (instance_id) DO UPDATE SET shutdown_time = excluded.shutdown_time".format(schema, scheduler_table),
                        instance_data)
        cur.close()
        con.commit()
        print("Scheduler")
        
    except (Exception, psycopg2.Error) as error:
        print("ERROR:", error)
        

# Function to query the scheduler table
def query_table(con):
    try:
        cur = con.cursor()
        cur.execute("SELECT instance_id, shutdown_time FROM {}.{}".format(schema, scheduler_table))
        rows = cur.fetchall()
        print("\n{:<12} {:<15}".format("Instance ID", "Shutdown Time"))
        print("-----------------------------")
        for r in rows:
            print("{:<12} {:<15}".format(r[0], r[1]))
        cur.close()
    except (Exception, psycopg2.Error) as error:
        print("ERROR:", error)

# Function to delete data from the scheduler table
def delete_from_table(con):
    try:
        cur = con.cursor()
        id_val = input("Enter the instance ID to delete: ")
        cur.execute("DELETE FROM {}.{} WHERE instance_id = %s".format(schema, scheduler_table), (id_val,))
        cur.close()
        con.commit()
        print("Data deleted successfully.")
    except (Exception, psycopg2.Error) as error:
        print("ERROR:", error)
        con.rollback()
