#!/usr/bin/env python

import argparse
import os

def print_sorted_groups(sorted_groups):
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
                            
def count_group_values(log_groups, log_list_len):
    for group_logs in log_groups.values():
        
        total_bytes = 0
        
        if (args.order == 'count' or args.order == 'count_p'):  
            count = len(group_logs['logs'])
            group_logs['count'] = count
            
            if(args.order == 'count_p'):
                group_logs['count_p'] = (group_logs['count'] / log_list_len) * 100
                   
        elif (args.order == 'bytes'):
            for group_log in group_logs['logs']:
                if (group_log['size_in_bytes'] != '-' and group_log['size_in_bytes'] != '"-"\n'):
                    total_bytes+=(group_log['size_in_bytes'])
            group_logs['total_bytes'] = total_bytes
     
    sorted_groups = dict(sorted(log_groups.items(), reverse=True))
    return sorted_groups
         
def group_logs(log_list):
    
    log_groups={}
    
    for log in log_list:
        if (args.group == 'ip'):
            
            if log['ip_address'] in log_groups:
                log_groups[log['ip_address']]['logs'].append(log)
            else:
                log_groups[log['ip_address']] = {'logs': [log]}
                if (args.order == 'bytes'):
                    log_groups[log['ip_address']].setdefault("total_bytes", 0)
                elif (args.order == 'count' or args.order == 'count_p'):
                    log_groups[log['ip_address']].setdefault("count", 0)
                else:
                    log_groups[log['ip_address']].setdefault("count_p", 0)
        else:
            if log['status'] in log_groups:
                log_groups[log['status']]['logs'].append(log)
            else:
                log_groups[log['status']] = {'logs': [log]}
                if (args.order == 'bytes'):
                    log_groups[log['status']].setdefault("total_bytes", 0)
                elif (args.order == 'count' or args.order == 'count_p'):
                    log_groups[log['status']].setdefault("count", 0)
                else:
                    log_groups[log['status']].setdefault("count_p", 0)
                
    return log_groups

def parse_log_file(log_file):
    log_list=[]
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
        log_list.append(logs_dictionary)
    
    return log_list

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse Common Log Format file, '\
                                     'group logs by IP address or HTTP status code.')
    parser.add_argument('filename', help='A name of a non empty, CML format file')
    parser.add_argument('group', choices=['ip', 'status'], help='Grouping logs by '\
                        'IP address or HTTP status code')
    parser.add_argument('order', choices=['count', 'count_p', 'bytes'],
                        help='Grouped logs will be ordered by their count, '\
                        'count percentage of all logged requests (count_p) '\
                        'or by total number of bytes transferred (bytes)')
    parser.add_argument('-limit','-l', help='Amount of grouped logs to print')
    args = parser.parse_args()

    filename = args.filename
 
    with open(filename, 'r') as log_file:
        if not os.path.getsize(filename):
            print(f'File \"{filename.split("/").pop()}\" cannot be empty')
            quit()
       
        log_list=parse_log_file(log_file)
        log_list_len=len(log_list)
        print_sorted_groups(count_group_values(group_logs(log_list), log_list_len))
        