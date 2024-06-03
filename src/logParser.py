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

