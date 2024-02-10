# A little moving average for visits based on an nginx log, no particular reason, just for fun and trying out pandas and matplotlib.

import re
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def parse_log_file(log_file_path):
    log_pattern = re.compile(
        r'\[(\d+\/\w+\/\d+):(\d+:\d+):\d+ \+\d+\] '
        r'"(?:GET|POST|PUT|DELETE|HEAD) (.*?) HTTP/\d.\d" (\d+) (\d+)'
    )

    timestamps = []
    with open(log_file_path, 'r') as file:
        for line in file:
            match = log_pattern.search(line)
            if match:
                timestamp_str = match.group(1) + ' ' + match.group(2)
                timestamp = datetime.strptime(timestamp_str, '%d/%b/%Y %H:%M')
                timestamps.append(timestamp)

    return timestamps

def main(log_file_path):
    timestamps = parse_log_file(log_file_path)
    time_series = pd.Series(1, index=pd.to_datetime(timestamps))
    minutely_visits = time_series.resample('min').sum().fillna(0)
    
    # Calculates a simple moving average for the last N minutes
    moving_average = minutely_visits.rolling(window=15).mean()

    plt.figure(figsize=(15, 8))
    plt.plot(minutely_visits.index, minutely_visits, label='Visits')
    plt.plot(moving_average.index, moving_average, label='Moving Average', linestyle='--')
    plt.xlabel('Month-Day Hour')
    plt.ylabel('Visits')
    plt.title('Just a Moving Average of Visits')
    plt.legend()
    plt.show()

log_file_path = 'nginx-log.txt'
main(log_file_path)
