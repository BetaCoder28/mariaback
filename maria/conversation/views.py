import os
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
        try:
            serializer = MessagesSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            data = serializer.validated_data
            role = data['role']
            content = data['content']
            topic = data.get('topic', 'introduce yourself')
            conversation_id = request.data.get('conversation_id','default_conversation')

            if conversation_id not in conversation_history:
                conversation_history[conversation_id] = [
                    {
                        "role" : 'system',
                        "content" : f"You're an virtual assistant, your name is Maria, initialize the conversation talking about {topic}."
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

            return Response(assistant_message, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                'error' : str(e)} , status=status.HTTP_500_INTERNAL_SERVER_ERROR)