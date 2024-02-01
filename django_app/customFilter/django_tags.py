from django import template


register = template.Library()


@register.simple_tag()
def digit_beatify(value):
    num = str(value)
    c = 0
    for i in range(len(num)-1,-1,-1):
        c+=1
        if c == 3:
            num = num[:i] +' '+num[i:]
            c=0
    return num