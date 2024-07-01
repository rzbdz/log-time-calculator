def define_multiple_div_trace(name, start, end, kill_collapsed=False):
    """
    add tracer for multiple divisions, log
    like name1, name2, name3....
    """
    for i in range(start, end + 1):
        rule.append((f"{name}{i}", f"{name}{i}", dict(force_kill_collapsed=kill_collapsed)))

input_log = "7noreset-ravd-hpi.log"
output_csv = input_log.split(".")[0]+".csv"

rule=[
    ("resume device", "resume-device"),
    ("non generic driver resume", "resume-call"),
    ("generic driver resume", "generic"),
    ("port resume", "port"),
    ("finish port resume", "finish-port"),
    ("finport set state", "finport-state"),
    ("usb reset resume", "finport-reset-resume"),
    ("retry reset resume", "finport-retry-reset-resume"),
    ("usb dis remote std", "finport-dis-remote"),
]
define_multiple_div_trace("ravd", 1, 6)
define_multiple_div_trace("hpi", 0, 2, kill_collapsed=True)
hpi_rule = [
    ("hpi1_newscheme", "hpi1_newscheme"),
    ("hpi1_address", "hpi1_address"),
    ("hpi2_port_reset", "hpi2_port_reset"),
    ("hpi2_epinit", "hpi2_epinit"),
    ("hpi2_desc", "hpi2_desc"),
]
rule.extend(hpi_rule)

match_pattern = r'\[\s+(\d+\.\d+)\] usb ((usb)*\d(-\d(.\d)*)*): (.+)'
match_dev_name_group = 2
match_timestamp_group = 1
match_logmsg_group = 6
