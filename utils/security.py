from markupsafe import Markup

from Exceptions.FatalException import FatalException


def prevent_xss(data):
    """
    Transform strings to a format to avoid xss.
    :param data: must be a string OR a dict non str object will be ignored
    :return: a new string or dict with modified string(s) to prevent xss security issue
    """
    markup = Markup()
    if type(data) is str:
        return markup.escape(data)
    if type(data) is dict:
        new_data = {}
        for attribute_name in data:
            s = data[attribute_name]
            if type(s) is str:
                new_data[attribute_name] = markup.escape(s)
            else:
                # Not a string
                new_data[attribute_name] = s
        return new_data
    raise FatalException("Data in prevent_xss must be a str or a dict, for sub-objects it's not yet implemented")
