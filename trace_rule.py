def define_multiple_div_trace(name, start, end, kill_collapsed=True):
    """
    add tracer for multiple divisions, log
    like name1, name2, name3....
    """
    for i in range(start, end + 1):
        rule.append((f"{name}{i}", f"{name}{i}", dict(force_kill_collapsed=kill_collapsed)))

input_log = "12who_set_reset_resume_for_everyone.log"
# add_suffix = "port-feat"
add_suffix = ""
output_csv = input_log.split(".")[0]+f"{add_suffix}.csv"

rule=[
    ("resume device", "resume-device"),
    ("usb non generic driver resume", "resume-call"),
    ("usb generic driver resume", "generic",  dict(force_kill_collapsed=True)),
    ("usb port resume", "port", dict(force_kill_collapsed=True)),
    ("hub port feat", "port-feat"),
    ("usb finish port resume", "finish-port"),
    ("usb finport set state", "finport-state"),
    ("usb reset resume", "finport-reset-resume"),
    ("usb retry reset resume", "finport-retry-reset-resume"),
    ("usb dis remote std", "finport-dis-remote"),
]
define_multiple_div_trace("ravd", 1, 6, kill_collapsed=True)
define_multiple_div_trace("hpi", 0, 2, kill_collapsed=True)
hpi_rule = [
    ("hpi1_newscheme", "hpi1_newscheme"),
    ("hpi1_address", "hpi1_address"),
    ("hpi2_port_reset", "hpi2_port_reset"),
    ("hpi2_epinit", "hpi2_epinit"),
    ("hpi2_desc", "hpi2_desc"),
    ("uep0reinit", "uep0reinit"),
    ("ravd2waitlck", "ravd2waitlck"),
    ("ravd2looselck", "ravd2looselck"),
]
rule.extend(hpi_rule)

match_pattern = r'\[\s+(\d+\.\d+)\] usb ((usb)*\d(-\d(.\d)*)*): (.+)'
match_dev_name_group = 2
match_timestamp_group = 1
match_logmsg_group = 6
