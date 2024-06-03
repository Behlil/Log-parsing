import pandas as pd
import matplotlib.pyplot as plt

def extract_timestamp_components(df):
    df['date'], df['time'] = df['Timestamp'].str.split('-').str[0], df['Timestamp'].str.split('-').str[1]

    # divide the date: 4 chars for year, 2 for month, 2 for day
    years = df['date'].str[:4]
    months = df['date'].str[4:6]
    day = df['date'].str[6:]

    # combine the date columns
    df['date'] = years + '-' + months + '-' + day

    # convert to datetime
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d', errors='coerce')

    df['time'] = pd.to_datetime(df['time'], format='%H:%M:%S:%f', errors='coerce').dt.time
    # drop NaT values in the date column
    df.dropna(subset=['date'], inplace=True)

    # extract day, month, year from date
    df['day'] = df['date'].dt.day
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year


    # extract hour, minute, second from time, milliseconds 
    df['hour'] = df['time'].apply(lambda x: x.hour)
    df['minute'] = df['time'].apply(lambda x: x.minute)
    df['second'] = df['time'].apply(lambda x: x.second)
    df['millisecond'] = df['time'].apply(lambda x: x.microsecond)

    # use only 3 decimal places for milliseconds
    df['millisecond'] = df['millisecond'] // 1000

    # convert year to int and ignore errors

    df['year'] = df['year'].astype(int)


    # convert month to int
    df['month'] = df['month'].astype(int)


    df.drop(['Timestamp', 'date', 'time'], axis=1, inplace=True)

    return df


def load_data():
    # Charger les données extraites à partir du fichier CSV
    file_path = "C:/Users/OUQSSIM/Desktop/st/GSITD/Data/HealthApp.log"
    parsed_logs = parse_log_file(file_path)
    data = pd.DataFrame(parsed_logs, columns=['Timestamp', 'Module', 'Identifier', 'Content'])
    data.drop('Identifier', axis=1, inplace=True)
    return data


def parse_log_line(line):
    parts = line.split('|')
    if len(parts) >= 4:
        timestamp = parts[0]
        module = parts[1]
        identifier = parts[2]
        message = '|'.join(parts[3:])
        return timestamp, module, identifier, message
    else:
        return None

def parse_log_file(filename):
    parsed_logs = []
    with open(filename, 'r') as file:
        for line in file:
            parsed_line = parse_log_line(line.strip())
            if parsed_line:
                parsed_logs.append(parsed_line)
    return parsed_logs

def modules_frequency():
    data = load_data()
    # plot the frequency of each module
    module_count = data['Module'].value_counts()
    # convert to DataFrame
    module_count = module_count.reset_index()
    module_count.columns = ['Module', 'count']
    # order the modules by count
    module_count = module_count.sort_values('count', ascending=False)
    
    return module_count


def count_error_frequency():
    data = load_data()
    error_keywords = ["error", "exception", "failed", "warning", "fatal", "crash", "failure", "out of memory"]
    # filter the data by error keywords
    error_data = data[data['Content'].str.contains('|'.join(error_keywords), case=False)]
    # plot the frequency of errors as pie chart
    error_count = error_data['Module'].value_counts()
    # convert to DataFrame
    error_count = error_count.reset_index()
    error_count.columns = ['Module', 'count']

    return error_count

def logs_by_day():
    data = load_data()
    data = extract_timestamp_components(data)
    logs_per_day = data.groupby('day').size()
    # convert to DataFrame
    logs_per_day = logs_per_day.reset_index()
    logs_per_day.columns = ['day', 'count']
    return logs_per_day
    

def logs_by_hour():
    data = load_data()
    data = extract_timestamp_components(data)
    # plot the number of logs by hour
    logs_per_hour = data.groupby('hour').size()
    # convert to DataFrame
    logs_per_hour = logs_per_hour.reset_index()
    logs_per_hour.columns = ['hour', 'count']
    return logs_per_hour

def logs_by_month():
    data = load_data()
    data = extract_timestamp_components(data)
    # plot the number of logs by month
    logs_per_month = data.groupby('month').size()
    # convert to DataFrame
    logs_per_month = logs_per_month.reset_index()
    logs_per_month.columns = ['month', 'count']

    return logs_per_month