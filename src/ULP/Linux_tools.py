import re
import pandas as pd
import seaborn as sns
file_path = "C:/Users/OUQSSIM/Desktop/st/GSITD/Data/Linux.log"
import plotly.express as px


def extract_log_info_from_file(file_path):
    # Regular expression pattern to extract information
    pattern = r'(\w{3})\s+(\d{1,2})\s(\d{2}:\d{2}:\d{2})\s(\w+)\s(\w+)(\(\w+\))?(\[\d+\])?:(.*)'
    
    # Read log content from the file
    with open(file_path, 'r') as file:
        log_content = file.read()
    
    # Find all matches in the log content
    matches = re.findall(pattern, log_content)
    
    # Create a list to store extracted data
    data = []
    
    # Iterate over matches and append to data list
    for match in matches:
        Month = match[0]
        Day = match[1]
        Time = match[2]
        hostname = match[3]
        service = match[4]
        pam_unix = match[5] if match[5] else ''  # Handle optional part
        process_id = match[6] if match[6] else ''
        message = match[7]

        # replace () with '' in pam_unix
        pam_unix = pam_unix.replace('(', '').replace(')', '') if pam_unix else ''

        # replace [] with '' in process_id
        process_id = process_id.replace('[', '').replace(']', '') if process_id else ''
        data.append([Month, Day, Time, hostname, service, pam_unix, process_id, message])
    
    # Create DataFrame from the data list
    df = pd.DataFrame(data, columns=['Month', 'Day', 'Time', 'Hostname', 'Service', 'PAM_UNIX', 'Process_Id', 'Message'])
    
    return df

def get_matches(file_path, regex_pattern):
    matches = []
    with open(file_path, 'r') as file:
        for line in file:
            match = re.search(regex_pattern, line)
            if match:
                matches.append(match.group(0))
    return matches
def convert_event_template_to_regex(event_template):
    regex_event_template = re.sub(r'<\*>', r'.+', event_template)
    # delete first and last spaces
    regex_event_template = regex_event_template.strip()
    # replace double spaces with single spaces
    regex_event_template = regex_event_template.replace('  ', ' ')
    # count spaces in the regex pattern
    return regex_event_template

def count_occurrences(file_path , event_templates):
    occurrences = {}
    for event_template in event_templates:
        regex_event_template = convert_event_template_to_regex(event_template)
        matches = get_matches(file_path, regex_event_template)
        occurrences[event_template] = len(matches)
    # convert to DataFrame
    occurrences = pd.DataFrame(list(occurrences.items()), columns=['Event Template', 'Occurrences'])
    #sort the occurrences by values
    occurrences = occurrences.sort_values('Occurrences', ascending=False)
    return occurrences

def plot_occurrences(occurrences):
    import plotly.express as px
    fig = px.bar(occurrences, x='Event Template', y='Occurrences', title='Occurrences of Event Templates')
    return fig

def filter_error(log_df):
    error_keywords = ["error", "exception", "failed", "warning", "fatal", "crash", "failure", "out of memory"]
    error_df = log_df[log_df['Message'].str.contains('|'.join(error_keywords), case=False)]
    return error_df

def count_error_occurrences_by_service():
    data = extract_log_info_from_file(file_path)
    error_data = filter_error(data)
    error_occurrences = error_data['Service'].value_counts().to_dict()
    print(error_occurrences)
    return error_occurrences

def count_error_occurrences_by_service_filtered(error_type):
    data = extract_log_info_from_file(file_path)
    if error_type == "All":
        error_data = filter_error(data)
    elif error_type == "Authentification":
        error_data = data[data['Message'].str.contains('auth', case=False)]
    elif error_type == "Memoire":
        error_data = data[data['Message'].str.contains('memory', case=False)]

    error_occurrences = error_data['Service'].value_counts().to_dict()
    return error_occurrences

def plot_error_occurrences_by_service(erroe_type):
    error_occurrences = count_error_occurrences_by_service_filtered(error_type=erroe_type)
    # sort the error occurrences by values
    error_occurrences = dict(sorted(error_occurrences.items(), key=lambda x: x[1], reverse=True))
    # plot the error occurrences
    import plotly.express as px
    fig = px.bar(x=list(error_occurrences.keys()), y=list(error_occurrences.values()), title='Error Occurrences by Service',color=list(error_occurrences.values()) )
    return fig

def services_frequency():
    data = extract_log_info_from_file(file_path)
    services = data['Service'].value_counts()
    return services

def plot_services_frequency():
    services = services_frequency()
    # top 10 services
    services = services[:10]
    # plot the frequency of each service
    import plotly.express as px
    fig = px.bar(services, x=services.index, y=services.values, title='Services Frequency')
    return fig
