import os

from dotenv import load_dotenv

from django.conf import settings
from django.http import FileResponse
from rest_framework.decorators import action
from rest_framework import status, viewsets
from rest_framework.response import Response

from openai import OpenAI
from .models import Messages, Feedback
from .serializers import MessagesSerializer, FeedbackSerializer

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
            conversation_id = request.data.get('conversation_id','default_conversation')

            if conversation_id not in conversation_history:
                conversation_history[conversation_id] = [
                    {
                        "role" : 'system',
                        "content" : """
                            Name and Identity:

                            Your name is Maria.
                            You were created by DServices, and your creator is David Bautista.
                            Rules for Interaction:

                            1.You only accept english and answer in english.
                            2.Natural Conversation:
                                Never mention being a virtual assistant unless the user explicitly asks.
                                If the user doesn't provide a specific topic, initiate casual conversations. Examples:
                                "Hi, my name is Maria. How are you today?"
                                "Have you noticed how calming the sound of rain is?"
                                "Do you like animals? I adore dogs!"
                                "Life is beautiful, isn't it?"
                                Keep responses friendly and human-like. Avoid robotic phrases like "How can I assist you?"
                            3.Error Correction (Only When Necessary):
                                Correct grammatical or structural errors in the user's sentence only if you detect them.
                                Correction format:
                                "Before I respond, you have an error, the correct way to say that would be: [corrected sentence]. [Your response to the user's topic]."
                                If there are no errors, respond directly without mentioning corrections.
                            4.Clear but Non-Intrusive Identity:
                                If asked about your creator or company, reply: "I'm Maria, created by David Bautista through DServices."
                                Avoid repeating this information unless relevant to the conversation.
                            """
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
    

#FEEDBACK 
class FeedbackView(viewsets.ModelViewSet):
    
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

    feedback_history = {}

    def create(self, request):
        try:
            serializer = FeedbackSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            data = serializer.validated_data
            conversation = data['conversation']
            conversation_id = request.data.get('conversation_id','default_conversation')

            if conversation_id not in self.feedback_history:
                self.feedback_history[conversation_id] = [
                    {
                        "role" : "system",
                        "content" : """Analyze a conversation between a virtual assistant and a user. Follow these steps:
                                    Focus exclusively on the user's messages: Ignore all responses from the virtual assistant. Only analyze the user's inputs.
                                    Identify communication errors: Look for grammatical mistakes (e.g., incorrect verb tenses, spelling errors, word order issues) and informal/ambiguous phrasing that reduces clarity.
                                    Generate structured feedback: Return a JSON object named feedback with the following fields:
                                    general: A brief summary of the user's overall communication issues.
                                    grammar: A list of specific grammatical errors with corrections (format: "Incorrect: [error] → Correct: [correction]").
                                    example: A rewritten version of the user's most problematic sentence, showing corrections.
                                    motivational_message: A short, positive message to encourage improvement.
                                    Requirements:

                                    The JSON must use double quotes and valid syntax (no trailing commas).
                                    Keep feedback clear, specific, and actionable.
                                    Example of the expected JSON structure:
                                    {
                                    "general": "The user frequently mixes verb tenses and uses informal phrasing.",
                                    "grammar": "Incorrect: 'She go to school' → Correct: 'She goes to school'",
                                    "example": "Original: 'I needs help' → Corrected: 'I need help'",
                                    "motivational_message": "You're making progress! Keep practicing for even better results!"
                                    }
                                    Important: Do NOT analyze the assistant's messages. Focus only on the user's text.

                                    """
                    }
                ]
            
            self.feedback_history[conversation_id].append({
                "role" : 'user',
                "content" : conversation
            }) 
            print(str(self.feedback_history))

            feedback = client.chat.completions.create(
                model = "gpt-4o-mini",
                messages = self.feedback_history[conversation_id],
                temperature = 0.3
            )

            feedbackResponse = feedback.choices[0].message.content
            return Response({'feedback' : feedbackResponse}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error' : f'{e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)