import os
import re

from django import template
import json

register = template.Library()


@register.filter(name="trim_file_name")
def get_api_badge(value):
    name = value.split("/")
    file_name = name[-1]
    trimmed_name = file_name.strip()
    # print(trimmed_name)
    return "".join(trimmed_name)


@register.filter(name="file_name_align")
def get_file_name(value):
    name = value.split("/")
    file_name = name[-1]
    base_name, extension = os.path.splitext(file_name)
    remove_auto_generator_name = re.split(r'[_]', base_name)
    result = remove_auto_generator_name[0]
    result += extension
    # print(result)
    return "".join(result)