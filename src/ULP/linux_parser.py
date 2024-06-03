import sys
sys.path.append('../../')
from ULP import LogParser

input_dir  = '../../Data/' # The input directory of log file
output_dir = 'demo_result/'  # The output directory of parsing results
log_file   = 'Linux.log'  # The input log file name
log_format = '<Month> <Date> <Time> <Level> <Component>(\[<PID>\])?: <Content>'  # HDFS log format
# Regular expression list for optional preprocessing (default: [])
regex      = [r"(\d+\.){3}\d+", r"\d{2}:\d{2}:\d{2}"]

parser = LogParser(log_format, indir=input_dir, outdir=output_dir, rex=regex)
parser.parse(log_file)