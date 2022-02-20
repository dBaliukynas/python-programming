#!/usr/bin/env python3

import argparse
import os
import sys

def print_group_value (group, order):
    '''Print group value.

    Parameters
    ----------
    group : dictionary
        Dictionary of group logs and its values (count, count_p or bytes)
    order: string
        Group value by which groups are being ordered.
    space_symbols: string
        Space symbols to dynamically shift table.
    dash_symbols: string
        Dash symbols to dynamically shift table.
    equal_symbols: string
        Equal symbols to dynamically shift table.
    '''
    order_value_digit_count = len(str(group[order]))
    
    if (order == 'count'):
        order_name = 'COUNT'
    elif (order == 'count_p'):
        order_name = 'COUNT PERCENTAGE'
    else:
        order_name = 'TOTAL BYTES'
        
    order_name_digit_count = len(order_name)
    
    if (order_value_digit_count > order_name_digit_count):
        digit_count = order_value_digit_count
    else:
        digit_count = order_name_digit_count

    print(f'''+--{'-' * digit_count}+
| {order_name}{' ' * (digit_count - order_name_digit_count )} |
+=={'=' * digit_count}+
| {group[order]}{' ' * (digit_count - order_value_digit_count) 
                 if digit_count == order_name_digit_count else ''} |
+--{'-' * digit_count}+''')


def print_sorted_groups(sorted_groups, order, limit_number):
    '''Print sorted log groups.

    Parameters
    ----------
    sorted_groups : dictionary
        Dictionary of sorted groups in descending order.
    limit_number: string / None
        Amount of rows to print.
    '''
    limit_index = 0
    for group_key, group in sorted_groups.items():

        if limit_number is not None and limit_index == int(limit_number):
            sys.exit()
        print(f'\n{group_key}:')

        for sorted_log in group['logs']:

            if limit_number is not None and limit_index == int(limit_number):
                print_group_value (group, order)
                sys.exit()

            print(f'{sorted_log}\n')
            limit_index +=1

        print_group_value (group, order)

def count_group_values(log_groups, log_list_len, order):
    '''Count grouped logs values.

    Parameters
    ----------
    log_groups : dictionary
        Dictionary of logs that are grouped by IP address or HTTP status code.
    log_list_len: int
        Length of all logs.

    Returns
    -------
    log_groups: dictionary
        Dictionary of logs grouped by IP address or HTTP status code
        and its values (count, count_p or total_bytes).
    '''
    for group in log_groups.values():

        total_bytes = 0

        if order in ('count','count_p'):
            count = len(group['logs'])
            group['count'] = count

            if order == 'count_p':
                group['count_p'] = (group['count'] / log_list_len) * 100

        elif order == 'total_bytes':
            for log in group['logs']:
                if log['size_in_bytes'] != '-' and log['size_in_bytes'] != '"-"\n':
                    total_bytes += (log['size_in_bytes'])
            group['total_bytes'] = total_bytes
            
    return log_groups

def group_logs(log_list, group, order):
    '''Group logs by IP address or HTTP status code.

    Parameters
    ----------
    log_list : list
        List of log dictionaries.

    Returns
    -------
    log_groups: dictionary
        Dictionary of logs grouped by IP address or HTTP status code.

    '''
    log_groups = {}

    for log in log_list:     
        if log[group] in log_groups:
            log_groups[log[group]]['logs'].append(log)
                
        else:
            log_groups[log[group]] = {'logs': [log]}

    return log_groups

def parse_log_file(log_file):
    '''Parse log file.

    Parameters
    ----------
    log_file : file
        File that contains Common Log Format HTTP request logs.

    Returns
    -------
    log_list: list
        List of log dictionaries.

    '''
    log_list = []
    for line in log_file:
        line_split = line.split(' ')

        ip_address = line_split[0]
        client_identity = line_split[1]
        auth_user = line_split[2]
        date = ' '.join(line_split[3:5])
        if line_split[5] != '"-"' and line_split[5] != '-':
            request = ' '.join(line_split[5:8])
            if line_split[8] != '-':
                status = line_split[8]
            if line_split[9] != '-' and \
            line_split[9] != '"-"' and line_split[9] != '"-"\n' :
                size_in_bytes = int(line_split[9])
            else:
                size_in_bytes = line_split[9]
        else:
            request = line_split[5]
            status = line_split[6]
            size_in_bytes = int(line_split[7])

        logs_dictionary = {
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

def main():
    parser = argparse.ArgumentParser(description='Parse Common Log Format file, '\
                                     'group logs by IP address or HTTP status code ' \
                                     'and print sorted (by count, count percentage '\
                                     'or total bytes of group) grouped logs.')
    parser.add_argument('filename', help='A name of a non empty, CML format file')
    parser.add_argument('group', choices=['ip', 'status'], help='Grouping logs by '\
                        'IP address or HTTP status code')
    parser.add_argument('order', choices=['count', 'count_p', 'bytes'],
                        help='Grouped logs will be ordered by their count, '\
                        'count percentage of all logged requests (count_p) '\
                        'or by total number of bytes transferred (bytes)')
    parser.add_argument('-limit','-l', help='Amount of rows to print')
    args = parser.parse_args()

    with open(args.filename, 'r') as log_file:
        if not os.path.getsize(args.filename):
            print(f'File \"{args.filename.split("/").pop()}\" cannot be empty.')
            sys.exit()
            
        if (args.order == 'bytes'):
            args.order = 'total_bytes'
        if (args.group == 'ip'):
            args.group = 'ip_address'
            
        log_list=parse_log_file(log_file)
        log_list_len = len(log_list)
        
        log_groups = count_group_values(group_logs(log_list, args.group, args.order),
                                      log_list_len, args.order)
        
        sorted_groups = dict(sorted(log_groups.items(),
                                    key=lambda item: (item[1][args.order], item[0]),
                                    reverse=True))

        print_sorted_groups(sorted_groups, args.order, args.limit)

if __name__ == '__main__':
    main()
