#!/usr/bin/env python

import argparse
import os

def print_groups(sorted_groups):
    for ip_address, sorted_logs in sorted_groups.items():
        print(f'\n{ip_address}:')
        
        for sorted_log in sorted_logs['logs']:
            
            print(f'{sorted_log}\n')
        if (args.order == 'bytes'):
            digit_count=len(str(sorted_logs['total_bytes']))
        elif (args.order == 'count'):
            digit_count=len(str(sorted_logs['count']))
        else:
            digit_count=len(str(sorted_logs['count_p']))
        space_symbols=' ' * digit_count
        dash_symbols='-'  * digit_count
        equal_symbols='=' * digit_count
            
    
        if (args.order == 'bytes'):                 
            print(f'''+------------{dash_symbols}+
| TOTAL BYTES{space_symbols}|
+============{ equal_symbols}+
| {sorted_logs['total_bytes']}           |
+------------{dash_symbols}+''')
        elif (args.order == 'count'):
            print(f'''+------{dash_symbols}+
| COUNT{space_symbols}|
+======{ equal_symbols}+
| {sorted_logs['count']}     |
+------{dash_symbols}+''')
        else:
            print(f'''+-----------------{dash_symbols}+
| COUNT PERCENTAGE{space_symbols}|
+================={ equal_symbols}+
| {sorted_logs['count_p']}%               |
+-----------------{dash_symbols}+''')
                            
def count_ip(logs_grouped_by_ip, list_of_logs_length):

    for log_groups in logs_grouped_by_ip.values():
        total_bytes = 0
        if (args.order == 'count' or args.order == 'count_p'):  
            count = len(log_groups['logs'])
            log_groups['count'] = count
            
            if(args.order == 'count_p'):
                log_groups['count_p'] = (log_groups['count'] / list_of_logs_length) * 100
                print(log_groups['count'])
                   
        elif (args.order == 'bytes'):
            for log_group in log_groups['logs']:
                if (log_group['size_in_bytes'] != '-' and log_group['size_in_bytes'] != '"-"\n'):
                    total_bytes+=(log_group['size_in_bytes'])
            log_groups['total_bytes'] = total_bytes
     
        
    sorted_groups = dict(sorted(logs_grouped_by_ip.items(), reverse=True))
    return sorted_groups
         
def group_requests_by_ip(list_of_logs):

    logs_grouped_by_ip={}
    for log in list_of_logs:
        if log['ip_address'] in logs_grouped_by_ip:
            logs_grouped_by_ip[log['ip_address']]['logs'].append(log)
        else:
            logs_grouped_by_ip[log['ip_address']] = {'logs': [log]}
            if (args.order == 'bytes'):
                logs_grouped_by_ip[log['ip_address']].setdefault("total_bytes", 0)
            elif (args.order == 'count' or args.order == 'count_p'):
                logs_grouped_by_ip[log['ip_address']].setdefault("count", 0)
            else:
                logs_grouped_by_ip[log['ip_address']].setdefault("count_p", 0)
         
    # print(len(list_of_logs))
    return logs_grouped_by_ip

def parse_log_file(log_file):
    list_of_logs=[]
    for line in log_file:
    
        ip_address=line.split(' ')[0]
        client_identity=line.split(' ')[1]
        auth_user=line.split(' ')[2]
        date=' '.join(line.split(' ')[3:5])
        if (line.split(' ')[5] != '"-"' and line.split(' ')[5] != '-'):
            request=' '.join(line.split(' ')[5:8])
            if (line.split(' ')[8] != '-'):
                status=line.split(' ')[8]
            if (line.split(' ')[9] != '-' and line.split(' ')[9] != '"-"' and line.split(' ')[9] != '"-"\n' ):
                size_in_bytes=int(line.split(' ')[9])
            else:
                size_in_bytes=line.split(' ')[9]
        else:
            request=line.split(' ')[5]
            status=line.split(' ')[6]
            size_in_bytes=int(line.split(' ')[7])
            

        logs_dictionary={
            'ip_address':ip_address,
            'client_identity':client_identity,
            'auth_user':auth_user,
            'date':date,
            'request':request,
            'status':status,
            'size_in_bytes':size_in_bytes,
            }
        list_of_logs.append(logs_dictionary)
    return list_of_logs


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse Common Log Format file.')
    parser.add_argument('filename', help='A name of a non empty, CML format file')
    parser.add_argument('group', choices=['ip', 'status'], help='Grouping requests by IP or HTTP Status Code')
    parser.add_argument('order', choices=['count', 'count_p', 'bytes'],
                        help='Grouped requests will be ordered by their count, '\
                        'count percentage of all logged requests (count_p) '\
                        'or by total number of bytes transferred (bytes)')
    parser.add_argument('-limit','-l', help='Amount of rows to print')
    args = parser.parse_args()

    filename = args.filename
 
    with open(filename, 'r') as log_file:
        if not os.path.getsize(filename):
            print(f'File \"{filename.split("/").pop()}\" cannot be empty')
            quit()
       
        list_of_logs=parse_log_file(log_file)
        list_of_logs_length=len(list_of_logs)
        print_groups(count_ip(group_requests_by_ip(list_of_logs), list_of_logs_length))
        