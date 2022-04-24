import json


def write_to_file(instance_groups, *filenames):
    '''
    Write instance to files in dictionary structure.
    Parameters
    ----------
    instance_groups : list
        List of grouped instances.
    filenames: string

    '''
    for instance_group, filename in zip(instance_groups, filenames):
        if (len(instance_groups) != len(filenames)):
            print('Instance groups and filename lengths should be the same.')
            return

        dict_string = '{"instances": ['

        for index, instance in enumerate(instance_group):

            dict_string += f'{{"{instance.__class__.__name__}": ' + json.dumps(instance, default=lambda item: item.__dict__) + \
                f'{"}," if index != len(instance_group) - 1 else "}"}'

        dict_string += ']}'

        with open(filename, 'w') as file:
            file.write(dict_string)


def load_from_file(*filenames):
    '''
    Load dictionaries from files that represent instances.
    Returns
    ----------
    dict
        Dictionaries that represent instances.
    '''
    try:
        json_dictionaries = []

        for filename in filenames:
            with open(filename) as file:
                json_dictionaries.append(json.load(file))
        return json_dictionaries
    except FileNotFoundError as not_found:
        print(f'File {not_found.filename} is not found.')


def convert_to_instances(json_dictionaries, vars_):
    try:
        instance_list = []
        for json_dictionary in json_dictionaries:
            for instances in json_dictionary['instances']:
                instance_list.append(getattr(vars_[list(instances.keys())[0]], 'from_json')
                                     (instances[list(instances.keys())[0]]))
        return instance_list
    except TypeError:
        print(f'Passed arguments should not be empty and should be iterable.')
