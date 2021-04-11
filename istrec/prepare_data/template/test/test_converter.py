#!/usr/bin/env python
# -*- coding: utf-8 -*-
from prepare_data.template.template_converter import convert_from_yaml_to_prefixed
from prepare_data.template.template_converter import convert_from_prefixed_to_yaml
from prepare_data.template.template_converter import convert_from_prefixed_to_dataframe
from prepare_data.template.template_converter import convert_from_dataframe_to_prefixed
from prepare_data.template.template_converter import convert_from_dataframe_to_json
from prepare_data.template.template_converter import convert_from_json_to_dataframe
from prepare_data.template.template_helper import load_templates_from_dir

in_template_dir = "../test_templates/"
templates = load_templates_from_dir(in_template_dir)


def test_convert_between_yaml_and_prefix():
    for yaml_template in templates:
        print(f"original template:\t{yaml_template}")
        prefixed_template = convert_from_yaml_to_prefixed(yaml_template)
        template = convert_from_prefixed_to_yaml(prefixed_template)
        print(f"recovered template:\t{template}")
        assert (template == yaml_template) is True


def test_convert_between_prefixed_and_dataframe():
    for yaml_template in templates:
        print(f"original template:\t{yaml_template}")
        prefixed_template = convert_from_yaml_to_prefixed(yaml_template)
        dataframe_template = convert_from_prefixed_to_dataframe(prefixed_template)
        template = convert_from_dataframe_to_prefixed(dataframe_template)
        print(f"recovered template:\t{template}")
        assert (template == prefixed_template) is True


def test_convert_between_yaml_and_dataframe():
    for yaml_template in templates:
        print(f"original template:\t{yaml_template}")
        prefixed_template = convert_from_yaml_to_prefixed(yaml_template)
        dataframe_template = convert_from_prefixed_to_dataframe(prefixed_template)
        recovered_prefixed_template = convert_from_dataframe_to_prefixed(dataframe_template)
        recovered_yaml_template = convert_from_prefixed_to_yaml(recovered_prefixed_template)
        print(f"recovered template:\t{recovered_yaml_template}")
        assert (recovered_yaml_template == yaml_template) is True


def test_convert_between_yaml_and_csv():
    for yaml_template in templates:
        print(f"original template:\t{yaml_template}")
        prefixed_template = convert_from_yaml_to_prefixed(yaml_template)
        dataframe_template = convert_from_prefixed_to_dataframe(prefixed_template)
        csv_template = convert_from_dataframe_to_json(dataframe_template)
        print(csv_template)
        recovered_dataframe_template = convert_from_json_to_dataframe(csv_template)
        recovered_prefixed_template = convert_from_dataframe_to_prefixed(recovered_dataframe_template)
        recovered_yaml_template = convert_from_prefixed_to_yaml(recovered_prefixed_template)
        print(f"recovered template:\t{recovered_yaml_template}")
        assert (recovered_yaml_template == yaml_template) is True


if __name__ == '__main__':
    test_convert_between_yaml_and_prefix()
    test_convert_between_prefixed_and_dataframe()
    test_convert_between_yaml_and_dataframe()
    test_convert_between_yaml_and_csv()
