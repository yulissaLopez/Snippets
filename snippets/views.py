from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer

# El root de la API sera una vista que liste todos las instancias de Snippets o Cree una nueva
@csrf_exempt
def snippet_list(request):
    """Listar todos los snippets o crear uno nuevo"""
    if request.method == 'GET':
        # Obtener todas las instancias del modelo Snippet
        # Lo que obtengo son modelos de snippets no comprensibles por el cliente
        snippets = Snippet.objects.all()
        # Serializa (los conviento en diccionario) los objetos snippets para covertirlos en JSON y ser enviado al cliente
        serializer = SnippetSerializer(snippets, many = True)
        # serializer.data contiene una lista de diccionarios que representa los objetos 
        # safe = False es para que django acepte enviar una lista en lugar de un diccionario
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        # analiza(parsea) los datos de la solicitud y los convierte de JSON a diccionario
        data = JSONParser().parse(request)
        # SnippetSerializer valida y convierte el diccionario data en una instancia del modelo Snippet
        # data le indica al serializer que los datos provienen del cliente
        serializer = SnippetSerializer(data = data)
        # Verifica si los datos son validos y de acuerdo las validacion definida en el serializer y el modelo
        if serializer.is_valid():
            # Guarda los datos validados y crea un nuevo objeto
            serializer.save()
            return JsonResponse(serializer.data, status = 201)
        return JsonResponse(serializer.errors, status = 400)

@csrf_exempt
def snippet_detail(request, pk):
    """actualizar, eliminar un Snippet"""
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        # al pasar la instancia y la data 
        # el serializer valida y prepara los datos para actualizar ese objeto
        serializer = SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    
    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status = 204)
