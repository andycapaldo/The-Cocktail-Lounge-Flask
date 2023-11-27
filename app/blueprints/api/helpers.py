import re



def camel_to_snake(camel_case):
    snake_string = re.sub('([a-z0-9])([A-Z])', lambda x: x.group(1) + '_' + x.group(2), camel_case)
    return re.sub('\d+', lambda x: '_' + x.group(), snake_string.lower())

