# This shows the distribution of response sizes by time of day, a metric no one asked for and no one needs. But it has density colouring and that's fun. And it's technically a log of logs, so that's fun too.

import re
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from scipy.stats import gaussian_kde

def parse_log_file(log_file_path):
    log_pattern = re.compile(
        r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - '
        r'\[(?P<date>\d+\/\w+\/\d+):(?P<time>\d+:\d+:\d+) \+\d+\] '
        r'"(?P<method>\S+) (?P<path>\S+) (?P<protocol>\S+)" '
        r'(?P<status>\d+) (?P<size>\d+) '
        r'"(?P<referrer>.*)" "(?P<user_agent>.*)"'
    )

    records = []

    with open(log_file_path, 'r') as file:
        for line in file:
            match = log_pattern.match(line)
            if match:
                timestamp_str = match.group('date') + ' ' + match.group('time')
                timestamp = datetime.strptime(timestamp_str, '%d/%b/%Y %H:%M:%S')
                time_of_day = timestamp.hour * 60 + timestamp.minute
                response_size = int(match.group('size'))
                # Apply a logarithmic transformation to response size with an offset to avoid log(0)
                log_response_size = np.log(response_size + 1)
                records.append((time_of_day, log_response_size))

    return records

log_file_path = 'nginx-log.txt'
log_records = parse_log_file(log_file_path)

df_log = pd.DataFrame(log_records, columns=['TimeOfDay', 'LogResponseSize'])

xy = np.vstack([df_log['TimeOfDay'], df_log['LogResponseSize']])
z = gaussian_kde(xy)(xy)

plt.figure(figsize=(12, 6))
sc = plt.scatter(df_log['TimeOfDay'], df_log['LogResponseSize'], s=0.1, c=z, cmap='hot', alpha=0.5)
plt.xticks(range(0, 1440, 120), [f"{(i//60):02d}:00" for i in range(0, 1440, 120)])
plt.xlabel('Time of Day')
plt.ylabel('Log of Response Size (log(bytes))')
plt.title('Scatter Plot of Log Response Sizes by Time of Day')
cbar = plt.colorbar(sc, label='Density')
cbar.set_label('Density', rotation=270)
plt.grid(True)
plt.show()
