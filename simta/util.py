import datetime

def filter_obj_dict(obj, fields, allow=True):
    return filter_dict(obj.__dict__, fields, allow=allow)

def filter_dict(dict, fields, allow=True):
    if allow:
        return {k: v for k, v in dict.items() if k in fields}
    return {k: v for k, v in dict.items() if k not in fields}

def resolve_enums(dict, enums):
    for e in enums:
        if e in dict and dict[e] is not None:
            dict[e] = dict[e].value

def resolve_strs(dict, strs):
    for e in strs:
        if e in dict and dict[e] is not None:
            dict[e] = str(dict[e])

def cleanup_kwargs(allowed_kwargs, kwargs):
    kwargs = filter_dict(kwargs, allowed_kwargs)
    kwargs = {k: v for k, v in kwargs.items() if v}
    return kwargs

def apply_filters(stmt, allowed_filters, filters):
    return stmt.filter_by(**cleanup_kwargs(allowed_filters, filters))

def parse_time(time):
    return datetime.datetime.strptime(time,"%H:%M").time()