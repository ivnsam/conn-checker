#!/bin/python3

'''
Plan:
0. parse input vars
1. open csv file
2. parse rules.csv file
3. ssh to src host
4. check connection: telnet (python equivalent) to dst host:port
    - if connection is OK:
        1. save result to list
    -  elif dst host refused connection:
        1. ssh to dst host
        2. check is socket free on dst host
        3. run python server on dst host:port with timer to exit
        4. return to src host
        5. check connection (4)
        6. save to result list
'''

'''
To-Do:
add traceroute functionality
'''

import csv

if __name__ == "__main__":
    print("######################")
    print("## connChecker v0.1 ##")
    print("######################")
    
    delimiter = ';'
    quotechar = '"'
    
    source_address_column = 2
    source_ip_column = 3
    source_port_column = 4
    destination_address_column = 6
    destination_ip_column = 7
    destination_port_column = 8
    
    rules_file = []
    rules = []
    
    # read whole csv to `rules`
    with open('test_rule.csv', 'r') as file:
        reader = csv.reader(file, delimiter=delimiter, quotechar=quotechar)
        for row in reader:
            rules_file.append(row)

    # save rules only to variable with key-value arrays
    for rule in rules_file[1:]:
        # skip rule if destination port is empty
        if rule[destination_port_column].split("/")[0] == '':
            continue

        # check source address and ip, select one of them, skip if they are empty
        if rule[source_address_column] != "":
            src_host = rule[source_address_column]
        elif rule[source_address_column] == "" and rule[source_ip_column] != "" :
            src_host = rule[source_ip_column]
        else:
            continue
        # check destination address and ip, select one of them, skip if they are empty
        if rule[destination_address_column] != "":
            dst_host = rule[destination_address_column]
        elif rule[destination_address_column] == "" and rule[destination_ip_column] != "" :
            dst_host = rule[destination_ip_column]
        else:
            continue

        # src_host = rule[source_address_column]
        src_port = rule[source_port_column]
        # dst_host = rule[destination_address_column]
        dst_port = rule[destination_port_column].split("/")[1]
        proto = rule[destination_port_column].split("/")[0]
        rules.append([
            {"src_host": src_host}, 
            {"src_port": src_port}, 
            {"dst_host": dst_host}, 
            {"dst_port": dst_port}, 
            {"proto": proto}
            ])

    print(rules)

    with open('output.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter=delimiter, quotechar=quotechar)
        for rule in rules_file[1:]:
            writer.writerow([ rule[source_address_column], rule[source_port_column], rule[destination_address_column], rule[destination_port_column] ])
    file.close()
