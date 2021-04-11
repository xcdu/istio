#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import re
import io

"""
Template converter is to convert the format of yaml template.
Specifically, template converter only cares about the keys in yaml template.

Due to the requirement of Istio configuration format, we assume that the type 
of yaml template must be a dict.
"""

# It is the delimiter used in template prefix format
TEMPLATE_PREFIX_DELIMITER = "||"
# When convert from yaml to yaml with prefixed keys, the list shall be also changed
# into dict. The items in list should have a key and the key can also avoid conflict
# with numeric keys in original yaml.
REGEX_FOR_LIST_ENUMERATE = r"<NUM_\d+>"
FORMATTER_FOR_LIST_ENUMERATE = "<NUM_{}>"

# default column names of converted dataframe
TEMPLATE_PREFIXED_DATAFRAME_KEY_NAME = "key"
TEMPLATE_PREFIXED_DATAFRAME_VALUE_NAME = "value"


def convert_from_yaml_to_prefixed(yaml_content):
    prefixed_yaml = __convert_from_yaml_to_prefixed(yaml_content)
    return prefixed_yaml


def __convert_from_yaml_to_prefixed(yaml_content, prefixes=None):
    # 'prefixes' records the ancestors' keys, which consist of the prefixes of current key.
    if prefixes is None:
        prefixes = list()

    value_to_return = dict()
    delimiter = TEMPLATE_PREFIX_DELIMITER

    # To avoid directly changes when iterating the items in yaml, we copy the keys and values,
    # replacing keys with prefixed keys.
    if type(yaml_content) is dict:
        for key in yaml_content:
            prefixes.append(str(key))
            value_to_return[delimiter.join(prefixes)] = __convert_from_yaml_to_prefixed(yaml_content[key], prefixes)
            prefixes.pop()
    elif type(yaml_content) is list:
        for i, item in enumerate(yaml_content):
            prefixes.append(__prefix_of_enumerative_index(i))
            value_to_return[delimiter.join(prefixes)] = __convert_from_yaml_to_prefixed(item, prefixes)
            prefixes.pop()
    else:
        value_to_return = yaml_content
    return value_to_return


def convert_from_prefixed_to_yaml(prefixed_yaml):
    yaml_content = __convert_from_prefixed_to_yaml(prefixed_yaml)
    return yaml_content


def __convert_from_prefixed_to_yaml(prefixed_yaml):
    value_to_return = None
    delimiter = TEMPLATE_PREFIX_DELIMITER

    if type(prefixed_yaml) is dict:
        if len(prefixed_yaml) == 0:
            # avoid convert empty dict '{}' into None
            value_to_return = prefixed_yaml
        else:
            for key in prefixed_yaml:
                actual_key = str(list(key.split(delimiter)).pop())
                if value_to_return is None:
                    value_to_return = list() if __match_prefix_of_enumerative_index(actual_key) else dict()

                if __match_prefix_of_enumerative_index(actual_key):
                    # Convert dict into list and remove the enumerative prefixes
                    value_to_return.append(__convert_from_prefixed_to_yaml(prefixed_yaml[key]))
                elif actual_key.isnumeric():
                    # Convert numeric keys from string to int
                    value_to_return[int(actual_key)] = __convert_from_prefixed_to_yaml(prefixed_yaml[key])
                else:
                    # normally remove the prefix
                    value_to_return[actual_key] = __convert_from_prefixed_to_yaml(prefixed_yaml[key])
    else:
        value_to_return = prefixed_yaml
    return value_to_return


def convert_from_prefixed_to_dataframe(prefixed_yaml) -> pd.DataFrame:
    # just rename the constant variable
    key_name = TEMPLATE_PREFIXED_DATAFRAME_KEY_NAME
    value_name = TEMPLATE_PREFIXED_DATAFRAME_VALUE_NAME

    lines_of_prefixed = __convert_from_prefixed_to_lines_of_prefixed(prefixed_yaml)
    return pd.DataFrame(data=lines_of_prefixed, columns=[key_name, value_name], index=range(len(lines_of_prefixed)))


def __convert_from_prefixed_to_lines_of_prefixed(prefixed_yaml):
    value_to_return = list()
    for key, value in prefixed_yaml.items():
        if type(value) is dict:
            value_to_return.append([key, value])
            value_to_return += __convert_from_prefixed_to_lines_of_prefixed(value)
        else:
            value_to_return.append([key, value])
    return value_to_return


def convert_from_dataframe_to_prefixed(dataframe: pd.DataFrame):
    # just rename the default value for convenient usage
    key_name = TEMPLATE_PREFIXED_DATAFRAME_KEY_NAME
    value_name = TEMPLATE_PREFIXED_DATAFRAME_VALUE_NAME

    lines_of_prefixed = {}
    for index, row in dataframe.iterrows():
        key = row[key_name]
        value = row[value_name]
        lines_of_prefixed[key] = value

    delimiter = TEMPLATE_PREFIX_DELIMITER
    prefixed_yaml = dict()
    for key in lines_of_prefixed.keys():
        prefixed_keys = key.split(delimiter)
        if len(prefixed_keys) == 1:
            prefixed_yaml[key] = lines_of_prefixed[key]
    return prefixed_yaml


def __prefix_of_enumerative_index(i: int):
    return FORMATTER_FOR_LIST_ENUMERATE.format(i)


def __match_prefix_of_enumerative_index(prefix: str):
    return re.match(REGEX_FOR_LIST_ENUMERATE, prefix)


def __check_int(s: str):
    if not s or len(s) < 2:
        return s.isdigit()
    elif s[0] in ['-', "+"]:
        return s[1].isdigit()
    return s.isdigit()


def convert_from_dataframe_to_json(dataframe: pd.DataFrame):
    return dataframe.to_json()


def convert_from_json_to_dataframe(csv_data):
    return pd.read_json(io.StringIO(csv_data))
