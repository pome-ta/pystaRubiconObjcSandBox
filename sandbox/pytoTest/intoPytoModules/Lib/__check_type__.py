from enum import Enum, IntFlag

func = None


def check(_object, name, types):

    for _type in types:
        if _type is None:
            _type = type(None)

        if _type is func and callable(_object):
            return

        try:
            if _type.__name__ == "View" and _type.__module__ == "pyto_ui":
                if "__py_view__" in dir(_object):
                    return
        except AttributeError:
            pass

        if isinstance(_object, _type):
            return
        
    if "value" in dir(_object) and (isinstance(_object, Enum) or isinstance(_object, IntFlag)) and check(_object.value, name, types):
        return
        
    msg = f"Invalid value type. The '{name}' parameter must be an instance of one of the following types:"
    for _type in types:
        msg += f"\n{_type}"

    raise TypeError(msg)


func = type(check)
