from django import template
from magnitude import Magnitude, mg, new_mag

lb = Magnitude(0.45359237, kg=1)
new_mag('lb', lb)
new_mag('lbs', lb)

register = template.Library()

@register.filter()
def unit(value, unit=None):

    if not isinstance(value, tuple) and not len(value) is 2:
        return None
    
    if unit is not None:
        wtf = float(value[0])
        value = mg(wtf, value[1]).ounit(unit).toval()

    return value

