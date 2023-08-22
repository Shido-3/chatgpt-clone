# Second file to be executed

from django.shortcuts import render, redirect
from django.http import JsonResponse
import openai

from django.contrib import auth # Authentication library 
from django.contrib.auth.models import User # Allows us to access Django user model, which provides us a table to store the users
from .models import Chat # Imports our database called "Chat"

from django.utils import timezone

openai_api_key = '' # Open ai api key goes here
openai.api_key = openai_api_key

def ask_openai(message):

    # ChatCompletion takes into account the conversation as a whole while generating a response
    # TextCompletion only takes into account the current question/sentence while generating a response

    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo", # There is currently a waitlist to access gpt-4 as of this comment, https://help.openai.com/en/articles/7102672-how-can-i-access-gpt-4
        messages=[
            {"role": "system", "content": "You are an helpful assistant."}, # Here you specify what you would like for the chatbot to focus on
            # "role" Here you tell the ai what you would like it to be an expert on for exmaple "Web Developer"
            # "content" is the starting information the ai has to work with
            {"role": "user", "content": message},
        ]
    )
    
    answer = response.choices[0].message.content.strip()
    return answer

    # "choices[0]" selects the first response from the list of respsones available
    # "content" pulls only the text portion of the response
    # "strip" removes any leading or trailing whitespace

    # refer to https://platform.openai.com/docs/guides/gpt/chat-completions-api for further documentation

    ''' 
    response = openai.Completion.create(
        model = "text-davinci-003",
        prompt = message, # the message to generate completion for
        max_tokens = 150,
        n = 1, # How many responses to generate for each prompt. Note: Because this parameter generates many completions, 
        # it can quickly consume token quota. Use carefully and ensure reasonable settings for max_tokens and stop.
        stop = None, # Up to 4 sequences where the API will stop generating further tokens. The returned text will not 
        # contain the stop sequence.
        temperature = 0.7, # What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output 
        # more random, while lower values like 0.2 will make it more focused and deterministic.
    )

    answer = response.choices[0].text.strip()

    return answer
    '''

def chatbot(request):
    if request.user.is_authenticated: # Checks if the current user is registered/authenticated in the database
        chats = Chat.objects.filter(user=request.user) # Pulls up the chat history of the currently logged in user
        # Filters the "chat" database so that only the column "user" matching request.user is pulled from the database
    else:
        chats = None
        # If the current user is not registered/authenticated the "chats" variable is assigned a "null" value

    if request.method == 'POST': # Function is called when the user hits enter/submits their message
        message = request.POST.get('message')
        response = ask_openai(message)

        if request.user.is_authenticated: # If the current user is not registered/authenticated the user's chats and messages will not be saved into the database
            chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now()) # "request.user" gets the "user" field from the request (request is basically all the data that is sent from the user to the server)
            # Chat() it is assigning all the fields of the database to their respected values 
            chat.save()
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot.html', {'chats': chats}) # Renders "chatbot.html" with information from "request", send "chats" as dictionary containing the value of "chat"

def login(request):
    if request.method == 'POST':
        username = request.POST['username'] # Matches the corresponding id of the input box
        password = request.POST['password'] # Matches the corresponding id of the input box
        user = auth.authenticate(request, username=username, password=password) # Authenticates if the user actually exists
        if user is not None:
            auth.login(request, user)
            return redirect('chatbot') # If the user is authenticated/registered redirects back to the chatbot page
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1) # Creates a new user
                user.save() # Saves the user to the table provided by from django.contrib.auth.models import User (The data table is called "auth_user")
                auth.login(request, user) # Once the user creates their account they are automatically logged in
                return redirect('chatbot') # They are then automatically redirected to the chatbot
            except:
                error_message = 'Error creating account'
                return render(request, 'register.html', {'error_message': error_message})
        else:
            error_message = 'Password dont match'
            return render(request, 'register.html', {'error_message': error_message})
    return render(request, 'register.html')

def logout(request):
    auth.logout(request)
    return redirect('login')