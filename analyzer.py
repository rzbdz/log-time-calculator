import re
from operator import itemgetter
import trace_rule
import parser_config

def parser(input):
    match = re.search(trace_rule.match_pattern, input)
    if not match:
        return False, None
    time = float(match.group(trace_rule.match_timestamp_group))
    usbnum = str(match.group(trace_rule.match_dev_name_group))
    msg = str(match.group(trace_rule.match_logmsg_group))
    return True, (usbnum,  msg ,time)

def tryadd(dicku, msg, kw, key, time, force_kill_collapsed):
    if not force_kill_collapsed:
        if kw in msg:
            if "begin" in msg:
                dicku[key][0] = time
            if "end" in msg or "down" in msg:
                dicku[key][1] = time
    else:
        if f"{kw} begin" in msg:
            dicku[key][0] = time
        if f"{kw} end" in msg:
            dicku[key][1] = time

def print_final(dick: dict):
    for usb, cl in dick.items():
        print(usb)
        for c, times in cl.items():
            print("\t", usb, c, times[1]-times[0])
        

def gen_csv(dick):
    import csv
    with open(trace_rule.output_csv, 'w', newline='',) as file:
        writer = csv.writer(file,quoting=csv.QUOTE_ALL)
        writer.writerow(["usb", ] + [c for c in dick['1-1'].keys()])
        rows = []
        for usb, cl in dick.items():
            if "usb" in usb:
                row = [f"{usb}", ]
            else:    
                row = [f"usb{usb}", ]
            for c, times in cl.items():
                row.append(times[1]-times[0])
            rows.append(row)
            #writer.writerow(row)
                #print(f"\"{usb}\"", f"\"{c}\"", times[1]-times[0], sep=", ")
        rows.sort(key=itemgetter(0))
        writer.writerows(rows)

init_display_keys = []

def load_display_keys():
    for r in trace_rule.rule:
        if len(r) == 2:
            _, display_key = r
        elif len(r) == 3:
            _, display_key, _ = r
        init_display_keys.append(display_key)

def gen_dick_val():
    dick_val = {}
    for key in init_display_keys:
        dick_val[key] = [0, 0]
    return dick_val

if __name__=="__main__":
    with open(trace_rule.input_log, "r") as f:
        lines = f.readlines()
    load_display_keys()
    tups = []
    for line in lines:
        if parser_config.skip_hashtag and line.startswith("#"):
            continue
        p =  parser(line)
        if p[0]:
            tups.append(p[1])
    dick = {}
    for tup in tups:
        usbnum = tup[0]
        msg = tup[1]
        time = tup[2]
        #print("tup", tup)
        if dick.get(usbnum, None) is None:
            dick[usbnum] = gen_dick_val()
        for item in trace_rule.rule:
            if len(item) == 2:
                log_key, display_key = item
                force_kill_collapsed = False
            else:
                log_key, display_key, args = item
                force_kill_collapsed = args.get("force_kill_collapsed")
            tryadd(dick[usbnum], msg, log_key, display_key, time, force_kill_collapsed=force_kill_collapsed)
    #print_final(dick)
    gen_csv(dick)





        
