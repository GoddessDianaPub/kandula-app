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


def insert_data(con):
    try:
        cur = con.cursor()
        if table_name == scheduler_table:
            print ("table not created yet")
        else:
            id_val = input("Enter your value for id: ")
            name_val = input("Enter your value for id: ")
            cur.execute("insert into "+schema+"."+scheduler_table+" (id, name) values (%s, %s)", (id_val, name_val) )
            cur.close()
            con.commit()
    except (Exception) as error:
        print("ERROR: ", end = " ")
        print(error)
        cur.close()
        con.commit()

def create_table(con):
    try:
        cur = con.cursor()
        global table_name
        table_name = input("choose a table name: ")
        cur.execute("create table "+schema+"."+scheduler_table+"(id int primary key, name varchar(50))")
        cur.close()
        con.rollback()
    except psycopg2.errors.DuplicateTable as error:
        cur.close()
        con.commit()
        print("ERROR: ", end =" ")
        print(error)
        use_table_name = input("would you like to use "+scheduler_table+" table?: (y/n)")
        if use_table_name != "y":
            table_name = "not set"

def query_table(con):
    if table_name == "not set":
        print ("table not created yet")
    else:
        cur = con.cursor()
        cur.execute("select id, name  from "+schema+"."+table_name)
        rows = cur.fetchall()
        print("")
        print ("{:<8} {:<15}".format("id","name"))
        print("----     -----")
        for r in rows:
            print ("{:<8} {:<15}".format(r[0],r[1]))
        cur.close()


def delete_from_table(con):
    print("not implemented yet")

def leave(con):
    con.close()


while True:
    try:
        print(chr(27)+'[2j')
        print('\033c')
        print('\x1bc')
        print('which of the following would you like to do')
        print("1 - create table")
        print("2 - insert data to table")
        print("3 - delete data from table")
        print("4 - query table")
        print("5 - leave")
        val = input("Enter your value: ")
        if val == "1":
            create_table(con)
        elif val == "2":
            insert_data(con)
        elif val == "3":
            delete_from_table(con)
        elif val == "4":
            query_table(con)
        elif val == "5":
            print ("goodby")
            leave(con)
            break
        else:
            print ("Error: '"+val+"' is not a valid option")
        ignored_val = input("press enter to continue:")
    except (Exception) as error:
        print("ERROR: "+"in except")
        print(error)
        ignored_val = input("press enter to continue:")
        
 

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
