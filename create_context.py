import json


def create_context(path):
    file = open(path)
    lines = file.readlines()
    content = ""
    for line in lines:
        content += line
    content = content.replace('\n', ' ')
    context = {"contexts":content}
    jsonpath = path.split('.')[0]+'.json'
    with open(jsonpath, 'w') as f:
        json.dump(context, f)


if __name__ == "__main__":
    create_context("xlabs/context.txt")