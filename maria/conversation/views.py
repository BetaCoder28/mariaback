import os

from dotenv import load_dotenv

from django.conf import settings
from django.http import FileResponse
from rest_framework.decorators import action
from rest_framework import status, viewsets
from rest_framework.response import Response

from openai import OpenAI
from .models import Messages
from .serializers import MessagesSerializer

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
conversation_history = {}


class ChatView(viewsets.ModelViewSet):

    queryset = Messages.objects.all()
    serializer_class = MessagesSerializer

    def create(self, request):

        print("Received data:", request.data) 

        try:
            serializer = MessagesSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            data = serializer.validated_data
            role = data['role']
            content = data['content']
            topic = data.get('topic', 'if user dont ask anything, introduce yourself')
            conversation_id = request.data.get('conversation_id','default_conversation')

            if conversation_id not in conversation_history:
                conversation_history[conversation_id] = [
                    {
                        "role" : 'system',
                        "content" : f"Your name is Maria you was created by DServices the owner is David Bautista, if you detect a mistake in the user sentence you say 'the correct way of the sentence is ', {topic}."
                    }   
                ]

            conversation_history[conversation_id].append({
                "role" : role,
                "content" : content
            }) 
            #Guardar respuesta del asistente
            response = client.chat.completions.create(
                model = 'gpt-4o-mini',
                temperature = 0.8,
                messages = conversation_history[conversation_id]
            )

            assistant_message = response.choices[0].message.content

            # Añadir la respuesta del asistente al historial
            conversation_history[conversation_id].append({
                "role": "assistant",
                "content": assistant_message
            })

            #Audio de la respuesta
            audio_response = client.audio.speech.create(
               model = "tts-1",
               voice = 'nova',
               input= assistant_message
            )

            audio_data = audio_response.content
            
            # Determinar el nombre del archivo
            media_path = os.path.join(settings.MEDIA_ROOT, 'audios')
            os.makedirs(media_path, exist_ok=True)

            existing_files = sorted([
                int(f.replace("audio_", "").replace(".mp3", ""))
                for f in os.listdir(media_path) if f.startswith("audio_") and f.endswith(".mp3")
            ], reverse=True)

            next_id = (existing_files[0] + 1) if existing_files else 1
            audio_filename = f"audio_{next_id}.mp3"
            audio_filepath = os.path.join(media_path, audio_filename)

            # Construir la URL del audio
            audio_url = request.build_absolute_uri(settings.MEDIA_URL + f'audios/{audio_filename}')

            # Guardar el archivo en MEDIA_ROOT/audios/
            with open(audio_filepath, 'wb') as f:
                f.write(audio_data)


            return Response({
                'text' : assistant_message,
                'audio' : audio_url
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                'error' : str(e)} , status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Endpoint para reproducir un archivo de audio
    @action(detail=False, methods=['get'], url_path='audio/(?P<filename>[^/]+)')
    def get_audio(self, request, filename):
        """ Devuelve un archivo de audio almacenado en el servidor """
        file_path = os.path.join(settings.MEDIA_ROOT, 'audios', filename)
        if os.path.exists(file_path):
            return FileResponse(open(file_path, 'rb'), content_type='audio/mpeg')
        return Response({"error": "Archivo no encontrado"}, status=status.HTTP_404_NOT_FOUND)