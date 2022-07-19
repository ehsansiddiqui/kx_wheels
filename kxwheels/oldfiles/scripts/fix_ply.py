from apps.kx.models.tire import *

for ts in TireSize.objects.filter(ply='C'):
    ts.ply = '6C'
    ts.save()

for ts in TireSize.objects.filter(ply='D'):
    ts.ply = '8D'
    ts.save()

for ts in TireSize.objects.filter(ply='E'):
    ts.ply = '10E'
    ts.save()

