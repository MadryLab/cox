import argparse
import json
from collections import namedtuple
import os
import dill as pickle
import codecs
import itertools

def has_tensorboard(dirname):
    '''
    Given a directory path, return whether or not it has a tensorboard directory
    in it.

    Args:
        dirname (str): path to directory

    Returns:
        Whether or not the directory has a "tensorboard" folder in it.
    '''
    if not os.path.isdir(dirname):
        return False
    return 'tensorboard' in os.listdir(dirname)

def consistent(old, new):
    '''
    Asserts that either first argument is None or
    both arguments are equal, and returns the non-None
    argument.
    '''
    if old is None:
        return new
    assert old == new
    return old

def override_json(args, json_path, check_consistency=False):
    '''
    Overrides the null values in an arguments object with values extracted from
    a JSON file.

    Args:
        args (object): A python object with the arguments as properties.
        json_path (str): Path to the JSON file with which to override.
        check_consistency (bool): If true, make sure that the keys in the JSON
            file and the args object match up exactly
    Returns:
        A new args object with appropriately overriden None values.
    '''
    json_params = json.load(open(json_path))

    params = args.as_dict()

    if check_consistency:
        missing_keys = []
        for key in json_params:
            if key not in params:
                missing_keys.append(key)
        assert not missing_keys, "Following keys not in args: " + str(missing_keys)

        missing_keys = []
        for key in params:
            if key not in json_params and key != "config_path":
                missing_keys.append(key)
        assert not missing_keys, "Following keys not in JSON: " + str(missing_keys)

    json_params.update({k: params[k] for k in params if params[k] is not None})
    for k in [k for k in params if params[k] is None and not (k in json_params)]:
        json_params[k] = None

    params = json_params
    # for k, v in params.items():
    #     assert v is not None, k

    args = Parameters(params)
    return args

class Parameters():
    '''
    Parameters class, just a nice way of accessing a dictionary

    .. code-block:: python

        ps = Parameters({"a": 1, "b": 3})
        ps.A # returns 1
    '''
    def __init__(self, params):
        super().__setattr__('params', params)

        # ensure no overlapping (in case) params
        collisions = set()
        for k in self.params.keys():
            collisions.add(k.lower())

        assert len(collisions) == len(self.params.keys())

    def as_dict(self):
        return self.params

    def __getattr__(self, x):
        if x in vars(self):
            return vars(self)[x]

        k = x.lower()
        if k not in self.params:
            return None

        return self.params[k]

    def __setattr__(self, x, v):
        # Fix for some back-compatibility with some pickling bugs
        if x == 'params':
            super().__setattr__(x, v)
            return

        if x in vars(self):
            vars(self)[x.lower()] = v

        self.params[x.lower()] = v

    def __delattr__ (self, key):
        del self.params[key]

    def __iter__ (self):
        return iter(self.params)

    def __len__ (self):
        return len(self.params)

    def __str__(self):
        return json.dumps(self.params, indent=2)

    def __repr__(self):
        return str(self)

    def __getstate__(self):
        return self.params

    def __contains__(self, x):
        return x in self.params

    def __setstate__(self, x):
        self.params = x

def mkdirp(x, should_msg=False):
    '''
    Tries to make a directory, but doesn't error if the
    directory exists/can't be created.
    '''
    try:
        os.makedirs(x)
    except Exception as e:
        if should_msg:
            print("Failed to make directory (might already exist). \
            Exact message was %s" % (e.message,))

def obj_to_string(obj):
    '''
    Serialize an object to a string
    '''
    return codecs.encode(pickle.dumps(obj), "base64").decode()

def string_to_obj(s):
    '''
    Unserialize a string back into an object.
    '''
    if s is None or s == "":
        return None
    if not isinstance(s, str):
        return s
    try:
        return pickle.loads(codecs.decode(s.encode(), "base64"))
    except Exception as e:
        return s
