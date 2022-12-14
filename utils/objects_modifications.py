def convert_models_objects_to_json(objects):
    """
    Convert objects from package models into a json object in a list
    :param objects: the list of objects to convert in json
    :return: a new list of converted object in json
    """
    converted_objects = []
    for obj in objects:
        # TODO to optimize for creation with inline for
        converted_objects.append(obj.convert_to_json())
    return converted_objects
