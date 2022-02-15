#!/usr/bin/env python

import argparse
import os

def count_ip(requests_grouped_by_ip):
    # print(requests_grouped_by_ip)
    ip_addresses=list(requests_grouped_by_ip.keys())
    
    for ip_address in ip_addresses:
        ip_count=len(requests_grouped_by_ip[ip_address])
        #print(requests_grouped_by_ip[ip_address])
        print(f'{ip_address}, COUNT: {ip_count}')

def group_requests_by_ip(list_of_logs):

    requests_grouped_by_ip={}
    for log in list_of_logs:
        if log['ip_address'] in requests_grouped_by_ip:
            requests_grouped_by_ip[log['ip_address']].append(log)
        else:
            requests_grouped_by_ip[log['ip_address']] = [log]
    # print (requests_grouped_by_ip.keys())
    # ip_addresses=list(requests_grouped_by_ip.keys())
    # print(requests_grouped_by_ip[list(requests_grouped_by_ip.keys())[0]])
    return requests_grouped_by_ip



def parse_log_file(log_file):
    list_of_logs=[]
    for line in log_file:
    
        ip_address=line.split(' ')[0]
        client_identity=line.split(' ')[1]
        auth_user=line.split(' ')[2]
        date=' '.join(line.split(' ')[3:5])
        request=' '.join(line.split(' ')[5:8])
        status=line.split(' ')[8]
        size_in_bytes=line.split(' ')[9]

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
    args = parser.parse_args()
    filename = args.filename
 
    with open(filename, 'r') as log_file:
        if not os.path.getsize(filename):
            print(f'File \"{filename.split("/").pop()}\" cannot be empty')
            quit()
# =============================================================================
#         if (len(args) > 5):
#             print(f'''Maximum amount of arguments is 5. 
# Passed {len(args)} arguments.''')
#             quit()
# =============================================================================
        # count_ip_occurences()
       
        count_ip(group_requests_by_ip(parse_log_file(log_file)))
        
# =============================================================================
#         for line in log_file:
#             print("")
# =============================================================================
            


