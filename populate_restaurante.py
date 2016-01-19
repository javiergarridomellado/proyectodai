import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ProyectoDAI.settings')

import django
django.setup()

from restaurante.models import Bar, Tapa


def populate():
    cervezeros_bar = add_bar('Cervezeros')

    add_tapa(bar=cervezeros_bar,
        nombre="Carne en salsa")

    add_tapa(bar=cervezeros_bar,
        nombre="Bocadillo jamon")

    add_tapa(bar=cervezeros_bar,
        nombre="Lomo en salsa")

    bardjango_bar = add_bar("BarDjango")

    add_tapa(bar=bardjango_bar,
        nombre="Ensalada del Sur")

    add_tapa(bar=bardjango_bar,
        nombre="Potaje de lentejas")

    add_tapa(bar=bardjango_bar,
        nombre="Tapa autoctona")

    paco_bar = add_bar("Bar de Paco")

    add_tapa(bar=paco_bar,
        nombre="Jamon")

    add_tapa(bar=paco_bar,
        nombre="Chorizo")

    # Print out what we have added to the user.
    for c in Bar.objects.all():
        for p in Tapa.objects.filter(bar=c):
            print "- {0} - {1}".format(str(c), str(p))

def add_tapa(bar, nombre, votos=0):
    p = Tapa.objects.get_or_create(bar=bar, nombre=nombre)[0]
    p.votos=votos
    p.save()
    return p

def add_bar(nombre):
    c = Bar.objects.get_or_create(nombre=nombre)[0]
    return c

# Start execution here!
if __name__ == '__main__':
    print "Starting Rango population script..."
    populate()
