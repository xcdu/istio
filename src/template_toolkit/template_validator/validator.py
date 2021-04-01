#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import jsonschema
import yaml
import json
import codecs


schema_files_dir = "openapi_json_schema/isio_json_schema"
schema_file = "/Users/xcdu/repos/istio-project/istio/src/template_toolkit/template_validator/openapi_json_schema/isio_json_schema/networking/v1alpha3/envoy_filter.json"
in_file_p = "/Users/xcdu/repos/istio-project/istio/src/template_toolkit/template_validator/test_templates/productpage_envoy_ratelimit.yaml"
schema_id = "istio.networking.v1alpha3.WorkloadGroup"


schema_store = dict()
for root, _, filenames in os.walk(schema_files_dir):
    for filename in filenames:
        if not filename.endswith(".json"):
            continue
        in_file_path = os.path.join(root, filename)
        with codecs.open(in_file_path, "r", encoding="utf-8") as in_file:
            schema = json.load(in_file)
            for key in schema["components"]["schemas"]:
                print(key)
                schema_store[key] = schema["components"]["schemas"][key]
try:
    resolver = jsonschema.RefResolver("file://" + schema_file, schema_store[schema_id], schema_store)
    with codecs.open(in_file_p, "r", encoding="utf-8") as in_file:
        datas = yaml.load_all(in_file, Loader=yaml.SafeLoader)
        for data in datas:
            jsonschema.Draft4Validator(schema_store[schema_id], resolver=resolver).validate(data)


except jsonschema.ValidationError as error:
    print(error.message)
except jsonschema.SchemaError as error:
    print(error.message)



