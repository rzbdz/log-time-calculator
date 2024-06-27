rule=[
    ("resume device", "resume-device"),
    ("non generic driver resume", "resume-call"),
    ("generic driver resume", "generic"),
    ("port resume", "port"),
    ("finish port resume", "finish-port"),
]
input_log = "1.log"
output_csv = "result1.csv"

match_pattern = r'\[\s+(\d+\.\d+)\] usb ((usb)*\d(-\d(.\d)*)*): usb (.+)'

match_dev_name_group = 2
match_timestamp_group = 1
match_logmsg_group = 6
