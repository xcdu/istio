#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from shutil import copyfile


def extract_and_copy(istio_api_path, dst_dir):
    for root, _, filenames in os.walk(istio_api_path):
        for filename in filenames:
            if not filename.endswith(".gen.json"):
                continue
            abs_path = os.path.abspath(os.path.join(root, filename))
            kind, version, filename = abs_path.split(os.sep)[-3:]
            kind_version_dir = os.path.join(os.path.abspath(dst_dir), kind, version)
            if not os.path.exists(kind_version_dir):
                os.makedirs(kind_version_dir)
            copyfile(abs_path, os.path.join(kind_version_dir, filename.replace(".gen.json", ".json")))


def main(istio_api_repo_path="istio-api", destination_directory="."):
    if len(sys.argv) > 1:
        istio_api_repo_path = sys.argv[1]
    if len(sys.argv) > 2:
        destination_directory = sys.argv[2]
    extract_and_copy(istio_api_repo_path, destination_directory)


if __name__ == '__main__':
    main()
