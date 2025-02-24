import os
import base64

from dotenv import load_dotenv

from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets

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
                        "content" : f"Your name is Maria if you detect a mistake when the user speaks you say the correct way to speak or say the sentence, {topic}."
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

            #Audio de la respuesta
            audio_response = client.audio.speech.create(
               model = "tts-1",
               voice = 'nova',
               input= assistant_message
            )

            # Añadir la respuesta del asistente al historial
            conversation_history[conversation_id].append({
                "role": "assistant",
                "content": assistant_message
            })

            audio_data = audio_response.content

            with open("output.mp3", 'wb') as f:
                f.write(audio_data)

            audio_base64 = base64.b64encode(audio_data).decode('utf-8')


            return Response({
                'text' : assistant_message,
                'audio' : audio_base64
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                'error' : str(e)} , status=status.HTTP_500_INTERNAL_SERVER_ERROR)