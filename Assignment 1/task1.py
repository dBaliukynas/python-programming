#!/usr/bin/env python3

import argparse
import os
import sys

def print_group_value (group, order, space_symbols,
                               dash_symbols, equal_symbols):
    '''Print group value.

    Parameters
    ----------
    sorted_group : dictionary
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
    if order == 'bytes':
        print(f'''+------------{dash_symbols}+
| TOTAL BYTES{space_symbols}|
+============{ equal_symbols}+
| {group['total_bytes']}           |
+------------{dash_symbols}+''')
    elif order == 'count':
        print(f'''+------{dash_symbols}+
| COUNT{space_symbols}|
+======{ equal_symbols}+
| {group['count']}     |
+------{dash_symbols}+''')
    else:
        print(f'''+-----------------{dash_symbols}+
| COUNT PERCENTAGE{space_symbols}|
+================={ equal_symbols}+
| {group['count_p']}%               |
+-----------------{dash_symbols}+''')


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
        if order == 'bytes':
            digit_count = len(str(group['total_bytes']))
        elif order == 'count':
            digit_count = len(str(group['count']))
        else:
            digit_count = len(str(group['count_p']))

        space_symbols=' ' * digit_count
        dash_symbols='-'  * digit_count
        equal_symbols='=' * digit_count

        if limit_number is not None and limit_index == int(limit_number):
            sys.exit()
        print(f'\n{group_key}:')

        for sorted_log in group['logs']:

            if limit_number is not None and limit_index == int(limit_number):
                print_group_value (group, order, space_symbols,
                                               dash_symbols, equal_symbols)
                sys.exit()

            print(f'{sorted_log}\n')
            limit_index +=1

        print_group_value (group, order, space_symbols,
                                       dash_symbols, equal_symbols)

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

        elif order == 'bytes':
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
        if group == 'ip':

            if log['ip_address'] in log_groups:
                log_groups[log['ip_address']]['logs'].append(log)
            else:
                log_groups[log['ip_address']] = {'logs': [log]}
                if order == 'bytes':
                    log_groups[log['ip_address']].setdefault("total_bytes", 0)
                elif order in ('count', 'count_p'):
                    log_groups[log['ip_address']].setdefault("count", 0)
                else:
                    log_groups[log['ip_address']].setdefault("count_p", 0)
        else:
            if log['status'] in log_groups:
                log_groups[log['status']]['logs'].append(log)
            else:
                log_groups[log['status']] = {'logs': [log]}
                if order == 'bytes':
                    log_groups[log['status']].setdefault("total_bytes", 0)
                elif order in ('count', 'count_p'):
                    log_groups[log['status']].setdefault("count", 0)
                else:
                    log_groups[log['status']].setdefault("count_p", 0)

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
        log_list=parse_log_file(log_file)
        log_list_len = len(log_list)

        log_groups = count_group_values(group_logs(log_list, args.group, args.order),
                                      log_list_len, args.order)
        if args.order != 'bytes':
            sorted_groups = dict(sorted(log_groups.items(),
                                        key=lambda item: (item[1]['count'], item[0]),
                                        reverse=True))
        else:
            sorted_groups = dict(sorted(log_groups.items(),
                                        key=lambda item: (item[1]['total_bytes'], item[0]),
                                        reverse=True))

        print_sorted_groups(sorted_groups, args.order, args.limit)

if __name__ == '__main__':
    main()
