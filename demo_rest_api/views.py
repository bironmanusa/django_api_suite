from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import uuid

# Simulación de base de datos local en memoria
data_list = []

# Añadiendo algunos datos de ejemplo para probar el GET
data_list.append({'id': str(uuid.uuid4()), 'name': 'User01', 'email': 'user01@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User02', 'email': 'user02@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User03', 'email': 'user03@example.com', 'is_active': False}) # Ejemplo de item inactivo

class DemoRestApi(APIView):
    name = "Demo REST API"

    def get(self, request):

      # Filtra la lista para incluir solo los elementos donde 'is_active' es True
      active_items = [item for item in data_list if item.get('is_active', False)]
      return Response(active_items, status=status.HTTP_200_OK)

    def post(self, request):
      data = request.data

      # Validación mínima
      if 'name' not in data or 'email' not in data:
         return Response({'error': 'Faltan campos requeridos.'}, status=status.HTTP_400_BAD_REQUEST)

      data['id'] = str(uuid.uuid4())
      data['is_active'] = True
      data_list.append(data)

      return Response({'message': 'Dato guardado exitosamente.', 'data': data}, status=status.HTTP_201_CREATED)
    
class DemoRestApiItem(APIView):
    """
    Vista para manejar operaciones sobre un solo elemento identificado por su 'id'.
    """

    def put(self, request, id):
        # PUT: Reemplaza completamente los datos del elemento, excepto el id
        data = request.data
        # El id debe estar en el cuerpo y coincidir con el de la URL
        if 'id' not in data or data['id'] != id:
            return Response({'error': 'El campo id es obligatorio y debe coincidir con la URL.'}, status=status.HTTP_400_BAD_REQUEST)
        for idx, item in enumerate(data_list):
            if item['id'] == id:
                # Conserva el id, reemplaza el resto (is_active se mantiene si no se envía)
                is_active = data.get('is_active', item.get('is_active', True))
                data_list[idx] = {
                    'id': id,
                    'name': data.get('name', ''),
                    'email': data.get('email', ''),
                    'is_active': is_active
                }
                return Response({'message': 'Elemento reemplazado exitosamente.', 'data': data_list[idx]}, status=status.HTTP_200_OK)
        return Response({'error': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, id):
        # PATCH: Actualiza parcialmente los campos del elemento identificado por id
        data = request.data
        for item in data_list:
            if item['id'] == id:
                # Solo actualiza los campos presentes en data
                item.update({k: v for k, v in data.items() if k in item and k != 'id'})
                return Response({'message': 'Elemento actualizado parcialmente.', 'data': item}, status=status.HTTP_200_OK)
        return Response({'error': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        # DELETE: Eliminación lógica (is_active = False)
        for item in data_list:
            if item['id'] == id:
                item['is_active'] = False
                return Response({'message': 'Elemento eliminado lógicamente.'}, status=status.HTTP_200_OK)
        return Response({'error': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)