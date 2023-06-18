import json
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

con = psycopg2.connect(
    host=host,
    port=port,
    database=database,
    user=user,
    password=password
)


def insert_data(con, scheduler_table):
    try:
        cur = con.cursor()
        if table_name == "instances_scheduler":
            print("Table not created yet")
        else:
            id_val = input("Enter the value for id: ")
            name_val = input("Enter the value for name: ")
            cur.execute(
                f"INSERT INTO {schema}.{scheduler_table} (id, name) VALUES (%s, %s)",
                (id_val, name_val),
            )
            con.commit()
            print("Data inserted successfully")
        cur.close()
    except Exception as error:
        print("ERROR:", error)


def query_table(con, scheduler_table):
    try:
        cur = con.cursor()
        if table_name == "instances_scheduler":
            print("Table not created yet")
        else:
            cur.execute(f"SELECT id, name FROM {schema}.{scheduler_table}")
            rows = cur.fetchall()
            print("")
            print("{:<8} {:<15}".format("id", "name"))
            print("----     -----")
            for r in rows:
                print("{:<8} {:<15}".format(r[0], r[1]))
        cur.close()
    except Exception as error:
        print("ERROR:", error)


def delete_from_table(con, scheduler_table):
    try:
        cur = con.cursor()
        if table_name == "instances_scheduler":
            print("Table not created yet")
        else:
            id_val = input("Enter the id to delete: ")
            cur.execute(f"DELETE FROM {schema}.{scheduler_table} WHERE id = %s", (id_val,))
            con.commit()
            print("Data deleted successfully")
        cur.close()
    except Exception as error:
        print("ERROR:", error)


def leave(con):
    con.close()


def get_scheduling(con, schema, scheduler_table):
    try:
        cur = con.cursor()
        cur.execute(f"SELECT instance_id, shutdown_time FROM {schema}.{scheduler_table}")
        rows = cur.fetchall()
        cur.close()

        instance_schedule = {
            "Instances": []
        }

        for row in rows:
            instance_id = row[0]
            shutdown_time = row[1]
            
            instance_schedule["Instances"].append({
                "InstanceId": instance_id,
                "Stop": shutdown_time,
                "DailyShutdownHour": int(shutdown_time.split(":")[0])
            })

        return instance_schedule

    except Exception as error:
        print("ERROR:", error)


def create_scheduling(shutdown_hour, scheduler_table):
    instance_schedule = get_scheduling(con, schema, scheduler_table)
    try:  # Update 22:00
        index_22 = next(
            index
            for index, instance in enumerate(instance_schedule["Instances"])
            if instance["Stop"] == "22:00"
        )
        instance_schedule["Instances"][index_22]["DailyShutdownHour"] = int(shutdown_hour)
        print(
            "Instances with Stop time '22:00' will be shutdown at {}".format(
                shutdown_hour
            )
        )
    except StopIteration:  # Insert 22:00
        instance_schedule["Instances"].append(
            {"Stop": "22:00", "DailyShutdownHour": int(shutdown_hour)}
        )
        print(
            "Instances with Stop time '22:00' will be shutdown every day at {}".format(
                shutdown_hour
            )
        )

    try:  # Update 23:00
        index_23 = next(
            index
            for index, instance in enumerate(instance_schedule["Instances"])
            if instance["Stop"] == "23:00"
        )
        instance_schedule["Instances"][index_23]["DailyShutdownHour"] = int(shutdown_hour)
        print(
            "Instances with Stop time '23:00' will be shutdown at {}".format(
                shutdown_hour
            )
        )
    except StopIteration:  # Insert 23:00
        instance_schedule["Instances"].append(
            {"Stop": "23:00", "DailyShutdownHour": int(shutdown_hour)}
        )
        print(
            "Instances with Stop time '23:00' will be shutdown every day at {}".format(
                shutdown_hour
            )
        )
    # TODO: Implement a DB insert that creates the instance schedule in the table
    # Remember to store the updated instance_schedule back in the database



def delete_scheduling(con, scheduler_table):
    try:
        cur = con.cursor()
        cur.execute(f"DELETE FROM {schema}.{scheduler_table}")
        con.commit()
        print("Scheduling deleted successfully")
        cur.close()
    except Exception as error:
        print("ERROR:", error)
        


def insert_log(con, schema, log_table, instance_id, shutdown_time):
    try:
        cur = con.cursor()
        cur.execute(
            f"INSERT INTO {schema}.{log_table} (instance_id, shutdown_time) VALUES (%s, %s)",
            (instance_id, shutdown_time),
        )
        con.commit()
        cur.close()
        print("Log inserted successfully")
    except Exception as error:
        print("ERROR:", error)


def delete_log(con, schema, log_table):
    try:
        cur = con.cursor()
        cur.execute(f"DELETE FROM {schema}.{log_table}")
        con.commit()
        print("Logs deleted successfully")
        cur.close()
    except Exception as error:
        print("ERROR:", error)
