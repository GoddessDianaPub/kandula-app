import boto3
import psycopg2


def get_db_connection():
    # Replace the placeholders with your actual database credentials
    conn = psycopg2.connect(
        host='rds-db-instance-0.cihzevxi90ql.us-east-1.rds.amazonaws.com:5432',
        user='diana',
        password='Aa123456!',
        database='applicationdb0'
    )
    return conn


def get_scheduling():
    # TODO: Implement a DB select query that gets all instance ids and their scheduled hours
    #       The returned data would be in JSON format as shown in the sample output below
    session = boto3.Session(region_name="us-east-1")
    ec2_cli = session.client(service_name="ec2")

    instance_ids = []
    for each in ec2_cli.describe_instances()['Reservations']:
        for each_in in each['Instances']:
            instance_ids.append(each_in['InstanceId'])

    # Add all instance IDs to the "Instances" list with a default DailyShutdownHour of 23:00
    instance_schedule = {"Instances": []}
    for instance_id in instance_ids:
        instance_schedule["Instances"].append({"Id": instance_id, "DailyShutdownHour": 23})
    return instance_schedule



# Retrieve the scheduling information and print the output

instance_schedule = get_scheduling()
print(instance_schedule)


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

