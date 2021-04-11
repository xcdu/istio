#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pathlib

__OPENAPI_JSON_SCHEMA_CONFIGURATION_FILE_PATH__ = pathlib.Path(__file__).parent
__OJSCFP__ = __OPENAPI_JSON_SCHEMA_CONFIGURATION_FILE_PATH__

# Default path of Istio JSON schema directory filename
ISTIO_JSON_SCHEMA_DIR_FILENAME = "istio_json_schema"

# Default path of Istio JSON schema directory
ISTIO_JSON_SCHEMA_DIR = __OJSCFP__ / ISTIO_JSON_SCHEMA_DIR_FILENAME

# Default path of Kubernetes JSON schema
KUBERNETES_JSON_SCHEMA_DIR_FILENAME = "kubernetes_json_schema"

# Default path of Kubernetes JSON schema directory
KUBERNETES_JSON_SCHEMA_DIR = __OJSCFP__ / KUBERNETES_JSON_SCHEMA_DIR_FILENAME
