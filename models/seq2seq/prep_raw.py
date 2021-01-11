import os
import re
import tensorflow as tf

# hyper parameters
min_count = 32
sep_tag = "</SEP>"
value_mask = "</VALUE>"

punctuation = r'[!"#$%&()\*\+,-\./:;<=>?@\[\\\]^_{|}~\']'


def prep_docs(allow_list=None):
    # load docs
    DOCS_PATH = "../raw_data/docs"
    doc_paths = [os.path.join(DOCS_PATH, filename) for filename in os.listdir(DOCS_PATH) if
                 allow_list is not None and filename in allow_list]

    doc_content = []
    for doc_path in doc_paths:
        doc_file = open(doc_path, encoding="utf-8")
        lines = [line.strip() for line in doc_file.readlines()]
        doc_content.append(" ".join(lines))

    for line in doc_content:
        line = re.sub(r'https?:\/\/.*[\r\n]*', '', line, flags=re.MULTILINE)
        line = re.sub(r'\<a href', ' ', line)
        line = re.sub(r'&amp;', '', line)
        line = re.sub(r'[_"\-;%()|+&=*%.,!?:#$@\[\]/]', ' ', line)
        line = re.sub(r'<br />', ' ', line)
        line = re.sub(r'\'', ' ', line)

    with open("pdata/context", "w", encoding="utf-8") as prep_docs_file:
        prep_docs_file.writelines(doc_content)


def prep_codes(allow_list=None):
    # load codes
    CODES_PATH = "../raw_data/codes"
    codes_paths = [os.path.join(CODES_PATH, filename) for filename in os.listdir(CODES_PATH) if
                   allow_list is not None and filename in allow_list]

    code_content = []
    for code_path in codes_paths:
        code_file = open(code_path, encoding="utf-8")
        lines = [line for line in code_file.readlines() if not line.startswith("$")]
        lines = [(line[:line.find(":")] + " : " +value_mask).strip() for line in lines if ":" in line]
        code_content.append((" " + sep_tag + " ").join(lines) + "\n")
        print(lines)

    with open("pdata/template", "w", encoding="utf-8") as prep_codes_file:
        prep_codes_file.writelines(code_content)


def select_tasks():
    banlist = ["traffic-management.tcp-traffic-shifting", "security.authentication.authn-policy",
               "security.authentication.mtls-migration", "observability.metrics.tcp-metrics",
               "observability.distributed-tracing.overview"]
    CODES_PATH = "../raw_data/codes"
    codes_paths = {filename: os.path.join(CODES_PATH, filename) for filename in os.listdir(CODES_PATH) if
                   filename not in banlist}

    selected_tasks = []
    for code_filename, code_path in codes_paths.items():
        code_file = open(code_path, encoding="utf-8")
        lines = [line for line in code_file.readlines() if not line.startswith("$")]
        lines = [line[:line.find(":") + 1] + value_mask for line in lines if ":" in line]
        if len(lines) > 0:
            selected_tasks.append(code_filename)
        code_file.close()
    return selected_tasks


if __name__ == '__main__':
    selected_tasks = select_tasks()
    prep_codes(selected_tasks)
    prep_docs(selected_tasks)
