#!/usr/bin/env python

import sys
import os

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
        print(logs_dictionary)

if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename, 'r') as log_file:
        if not os.path.getsize(filename):
            print(f'File \"{filename.split("/").pop()}\" cannot be empty')
            quit()
        if (len(sys.argv) > 5):
            print(f'''Maximum amount of arguments is 5. 
Passed {len(sys.argv)} arguments.''')
            quit()
        parse_log_file(log_file)
        
# =============================================================================
#         for line in log_file:
#             print("")
# =============================================================================
            


