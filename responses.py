# Just displays a nice little graph of HTTP response codes from an nginx log file

import re
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

def parse_log_file(log_file_path):
    log_pattern = re.compile(
        r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - '
        r'\[(?P<datetime>\d+\/\b\w+\b\/\d{4}:\d{2}:\d{2}:\d{2} \+\d{4})\] '
        r'"(?P<method>\S+) (?P<path>\S+) HTTP\/\d.\d" (?P<status>\d+) (?P<size>\d+) '
        r'"(?P<referrer>-|[^"]+)" "(?P<user_agent>[^"]+)"'
    )

    records = []

    with open(log_file_path, 'r') as file:
        for line in file:
            match = log_pattern.match(line)
            if match:
                datetime_str = match.group('datetime')
                datetime_obj = datetime.strptime(datetime_str, '%d/%b/%Y:%H:%M:%S %z')
                records.append({
                    'datetime': datetime_obj,
                    'status': int(match.group('status')),
                    'size': int(match.group('size'))
                })

    return records

def analyze_logs(records):
    df = pd.DataFrame(records)
    response_code_distribution = df['status'].value_counts()
    return response_code_distribution

def plot_response_code_distribution(response_code_distribution):
    plt.figure(figsize=(12, 6))
    response_code_distribution.plot(kind='bar')
    plt.title('Response Code Distribution')
    plt.xlabel('HTTP Status Code')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()

log_file_path = 'nginx-log.txt'  # Replace with your actual log file path
log_records = parse_log_file(log_file_path)
response_code_distribution = analyze_logs(log_records)

plot_response_code_distribution(response_code_distribution)
