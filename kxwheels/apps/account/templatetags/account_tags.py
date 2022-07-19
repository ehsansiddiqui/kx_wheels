from django import template

register = template.Library()

@register.inclusion_tag('account/account_menu.html')
def get_menu():
    menu = {}
    return {'jathas': menu}


@register.filter()
def telephone(value):
    """docstring for telephone"""
    if not value:
        return '-'

    # https://gist.github.com/1031560
    # pad the string with 0s until it's at least 10 digits
    string = value
    while len(string) < 10:
        string = "0%s" % string
    string_list = list(string)
    string_list.reverse()
    string = "".join(string_list)

    index = 0
    output_number = ""
    for char in string:
        output_number = "%s%s" % (char, output_number)
        if index == 3:
            output_number = "-%s" % output_number
        elif index == 6:
            output_number = ") %s" % output_number
        elif index == 9:
            output_number = "(%s" % output_number
        index += 1

    return output_number