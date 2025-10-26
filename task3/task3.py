import re
from collections import Counter
import sys
import datetime

def load_logs(file_path: str) -> list:
    with open(file_path) as file:
        return file.readlines()


def parse_log_line(line: str) -> dict:
    # (2024-01-22) (08:30:01) (INFO) (User logged in successfully.) 4 groups in log line
    try:
        log_pattern = r'(\d{4}-\d{2}-\d{2})\s(\d{2}:\d{2}:\d{2})\s(INFO|DEBUG|WARNING|ERROR)\s(.+)'
        parsed_log = re.search(log_pattern, line)
        return {
            'date': parsed_log.group(1),
            'time': parsed_log.group(2),
            'level': parsed_log.group(3),
            'msg': parsed_log.group(4)
        }
    except: # when regexp pattern can't handle line in log file
        return { # returns log about corrupted log
            'date': datetime.datetime.now().strftime('%Y-%m-%d'),
            'time': datetime.datetime.now().time().strftime('%H:%M:%S'),
            'level': 'ERROR',
            'msg': "Log file corrupted"
        } 

def filter_logs_by_level(logs: list, level: str=None) -> list:
    filtered_logs = list(filter(lambda log: log['level'] == level, logs))
    return filtered_logs

def count_logs_by_level(logs: list) -> dict:
    return dict(Counter(log['level'] for log in logs))


def display_log_counts(counts: dict):
    table = f"""
Рівень логування | Кількість
-----------------|--------------------
"""
    print(table, end='')
    for key, value in counts.items():
        print(f"{key}\t\t | {value}")


def main():
    try:
        PATH = 1
        LEVEL = 2

        logs = list(map(parse_log_line, load_logs(sys.argv[PATH]))) #runs log parser on every line from log file via map()
        display_log_counts(count_logs_by_level(logs)) 
        try:  
            if len(sys.argv) < 3:
                # tries to read second argument if fails, gracefully drop optional logic
                return
            level = sys.argv[LEVEL]
            level = level.upper() 
            LEVELS = {'INFO', 'DEBUG', 'WARNING', 'ERROR'} 
            if level not in LEVELS: # checks log level for searching
                print("Log level not found")
                return
            filtered_logs = filter_logs_by_level(logs, level)
            print(f"Деталі логів для рівня '{level}':")

            for log in filtered_logs:
                print(f"{log['date']} {log['time']} - {log['msg']}")

        except Exception as err_msg:
            print(err_msg) 

    except IndexError:
        print("pass log file")

    except Exception as err_msg:
        print(err_msg)

if __name__ == '__main__':
    main()