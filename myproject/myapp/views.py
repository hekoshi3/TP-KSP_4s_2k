from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import ImageGenerationForm
from . import SDGEN
from .models import User
from .models import Request
from django.contrib import messages


def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            if user.password == password:
                # Успешная авторизация
                return redirect('image_generation')  # Перенаправление на страницу dashboard
            else:
                # Неверный пароль
                return render(request, 'login.html', {'error': 'Invalid password'})
        except User.DoesNotExist:
            # Пользователь не найден
            return render(request, 'login.html', {'error': 'User not found'})

    return render(request, 'login.html')
def register_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = request.POST.get('username')
        avatar = request.FILES.get('avatar')

        user = User(email=email, password=password, username=username, avatar=avatar)
        user.save()

        return redirect('login_user')  # Redirect to a success page

    return render(request, 'registration.html')
def image_generation_view(request):
    if request.method == 'POST':
        form = ImageGenerationForm(request.POST)
        if form.is_valid():
            prompt = form.cleaned_data['prompt']
            negative_prompt = form.cleaned_data['negative_prompt']
            width = form.cleaned_data['width']
            height = form.cleaned_data['height']
            seed = form.cleaned_data['seed']
            directory = 'media\\generated_images\\'
            generated_image_path = SDGEN.txt2img_TEST(directory) #txt2img(prompt, negative_prompt, seed, width, height, directory) ##
            return JsonResponse({'generated_image_path': generated_image_path})
        else:
            return JsonResponse({'error': 'Invalid form data'}, status=400)
            
    else:
        form = ImageGenerationForm()
        return render(request, 'image_generation.html', {'form': form})
