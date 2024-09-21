from django.db import models
"""
from pygments.lexers import get_all_lexers permite acceder a una lista de todos los lexers disponibles en Pygments, facilitando el resaltado de sintaxis para diferentes lenguajes de programación en tus aplicaciones.
"""
from pygments.lexers import get_all_lexers
"""
from pygments.styles import get_all_styles permite acceder a todos los estilos disponibles en Pygments, facilitando la personalización de la presentación visual del código resaltado en tus aplicaciones.
"""
from pygments.styles import get_all_styles

"""filtra los lexers de Pygments para crear una lista (LEXERS) que solo contiene aquellos lexers que tienen alias, facilitando su uso en aplicaciones que requieren resaltado de sintaxis."""
LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])

class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    # choices es un parametro que define una lista de opciones que el campo puede tomar
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)

    # se utiliza para configuraciones adicionales de ocmo se debe comprtar o manejar el modelo en el contexto de la base de datos
    class Meta:
        #Especifica el orden predeterminado para las consultas del modelo
        ordering = ['created']