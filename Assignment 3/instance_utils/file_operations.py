import json


def write_to_file(instances, *filenames):
    '''
    Write instance to files in dictionary structure.
    Parameters
    ----------
    instance : obj
        Instance.
    '''

    for filename in filenames:
        dict_string = '{"instances": ['
        for index, instance in enumerate(instances):
            dict_string += f'{{"{instance.__class__.__name__}": ' + json.dumps(instance, default=lambda item: item.__dict__) + \
                f'{"}," if index != len(instances) - 1 else "}"}'
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
    json_dictionaries = []

    for filename in filenames:
        with open(filename) as file:
            json_dictionaries.append(json.load(file))
    return json_dictionaries


def convert_to_instances(json_dictionaries, vars):
    instance_list = []
    for json_dictionary in json_dictionaries:
        for instances in json_dictionary['instances']:
            instance_list.append(getattr(vars[list(instances.keys())[0]], 'from_json')
                                 (instances[list(instances.keys())[0]]))
    return instance_list
