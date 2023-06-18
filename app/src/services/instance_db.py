import json
import psycopg2

schema = "kandula"
table_name = "not set"
con = psycopg2.connect(
    host="rds-db-instance-0.cihzevxi90ql.us-east-1.rds.amazonaws.com",
    port=5432,
    database="kandula",
    user="kandula",
    password="Aa123456!"
)


def insert_data(con):
    try:
        cur = con.cursor()
        if table_name == "not set":
            print("Table not created yet")
        else:
            id_val = input("Enter the value for id: ")
            name_val = input("Enter the value for name: ")
            cur.execute(
                f"INSERT INTO {schema}.{table_name} (id, name) VALUES (%s, %s)",
                (id_val, name_val),
            )
            cur.close()
            con.commit()
    except Exception as error:
        print("ERROR:", error)
        cur.close()
        con.commit()


def create_table(con):
    try:
        cur = con.cursor()
        global table_name
        table_name = input("Choose a table name: ")
        cur.execute(f"CREATE TABLE {schema}.{table_name}(id INT PRIMARY KEY, name VARCHAR(50))")
        cur.close()
        con.rollback()
    except psycopg2.errors.DuplicateTable as error:
        cur.close()
        con.commit()
        print("ERROR:", error)
        use_table_name = input(f"Would you like to use {table_name} table? (y/n)")
        if use_table_name != "y":
            table_name = "not set"


def query_table(con):
    if table_name == "not set":
        print("Table not created yet")
    else:
        cur = con.cursor()
        cur.execute(f"SELECT id, name FROM {schema}.{table_name}")
        rows = cur.fetchall()
        print("")
        print("{:<8} {:<15}".format("id", "name"))
        print("----     -----")
        for r in rows:
            print("{:<8} {:<15}".format(r[0], r[1]))
        cur.close()


def delete_from_table(con):
    print("Not implemented yet")


def leave(con):
    con.close()


def get_scheduling(con):
    try:
        cur = con.cursor()
        cur.execute(f"SELECT instance_id, shutdown_time FROM your_table_name")
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




def create_scheduling(os_type, shutdown_hour):
    instance_schedule = json.loads(get_scheduling())
    try:  # Update
        index = next(
            index
            for index, instance in enumerate(instance_schedule["Instances"])
            if instance["OSType"] == os_type
        )
        instance_schedule["Instances"][index]["DailyShutdownHour"] = int(shutdown_hour)
        print(
            "Instances with OS type '{}' will be shutdown at {}".format(
                os_type, shutdown_hour
            )
        )
    except StopIteration:  # Insert
        instance_schedule["Instances"].append(
            {"OSType": os_type, "DailyShutdownHour": int(shutdown_hour)}
        )
        print(
            "Instances with OS type '{}' will be shutdown every day at {}".format(
                os_type, shutdown_hour
            )
        )
    # TODO: Implement a DB insert that creates the OS type and the chosen hour in the DB
    # Remember to store the updated instance_schedule back in the database


def delete_scheduling(os_type):
    # Add indentation here
    try:
        # Delete scheduling logic
        pass
    except Exception as error:
        print("ERROR:", error)


