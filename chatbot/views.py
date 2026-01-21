from django.shortcuts import render,get_object_or_404,redirect
from google import genai
from PIL import Image
from chatbot.models import *
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.
client = genai.Client(api_key="AIzaSyDLvm5XQXI3deeqp--jiNx0TYpp7xcxe98")
def home(request):
    if request.method == "POST":
        text = request.POST.get('text')
        image = request.FILES.get('image')

        if text or image:
            if image:
                response = client.models.generate_content(
                    model='gemini-2.5-flash-lite',
                    contents=[
                        text if text else "What's in this image? Describe",
                        Image.open(image),
                    ]
                ).text
            else:    
                response = client.models.generate_content(
                    model='gemini-2.5-flash-lite',
                    contents=text 
                ).text
        
        chat =Chat.objects.create(
            text = text,
            image = image,
            response = response,
        )

        title = client.models.generate_content(
            model='gemini-2.5-flash-lite',
            contents= f'Create a short title (3-5 words) for this query: {text}'
        ).text

        room = Room.objects.create(
            user = request.user,
            title = title,
        )
        room.chat.add(chat)
        return redirect('chat',room.id)

    rooms = request.user.room_user.all()  
    context = {
        'rooms':rooms
    }    
    
    return render(request,'index.html',context)

def chat_room(request,id):
    
    current_room = get_object_or_404(Room,id=id)

    if request.method == "POST":
        text = request.POST.get('text')
        image = request.FILES.get('image')

        if text or image:
            if image:
                response = client.models.generate_content(
                    model='gemini-2.5-flash-lite',
                    contents=[
                        text if text else "What's in this image? Describe",
                        Image.open(image),
                    ]
                ).text
            else:    
                response = client.models.generate_content(
                    model='gemini-2.5-flash-lite',
                    contents=text 
                ).text
        

        chat = Chat.objects.create(
            text = text,
            image = image,
            response = response
        )
        print(chat.image.url)
        current_room.chat.add(chat)
        return redirect('chat',id)
    rooms = request.user.room_user.all()
    context = {
        "rooms":rooms,
            'current_room':current_room,
        }
    return render(request,'chat.html',context)


def delete_room(request,id):
    room = get_object_or_404(Room,id=id)
    if room.user == request.user:
        room.delete()
        return redirect('home')