import json


def write_to_file(instances, *filenames, separate=False,):
    '''
    Write instance to files in dictionary structure.
    Parameters
    ----------
    instance : obj
        Instance.
    '''
    if separate == True:
        for (index, instance), filename in zip(enumerate(instances), filenames):
            print(index)

            dict_string = '{"instances": ['

            dict_string += f'{{"{instance.__class__.__name__}": ' + json.dumps(instance, default=lambda item: item.__dict__) + \
                f'{"}"}'
            dict_string += ']}'

            with open(filename, 'w') as file:
                file.write(dict_string)
    else:

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


def convert_to_instances(json_dictionaries, vars_):
    instance_list = []
    for json_dictionary in json_dictionaries:
        for instances in json_dictionary['instances']:
            instance_list.append(getattr(vars_[list(instances.keys())[0]], 'from_json')
                                 (instances[list(instances.keys())[0]]))
    return instance_list
