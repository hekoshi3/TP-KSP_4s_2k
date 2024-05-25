from django.contrib.auth import login, authenticate, get_backends
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import ImageGenerationForm, UserCreationForm
from .models import Request, Model, Favourite
from . import SDGEN

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('user_profile')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def profile(request):
    user_requests = Request.objects.filter(user=request.user)
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        selected_request = get_object_or_404(Request, id=request_id)
        Favourite.objects.create(user=request.user, request=selected_request)
        return JsonResponse({'status': 'added to favourites'})
    return render(request, 'profile.html', {'requests': user_requests})

def image_generation_view(request):
    if request.method == 'POST':
        form = ImageGenerationForm(request.POST)
        if form.is_valid():
            prompt = form.cleaned_data['prompt']
            negative_prompt = form.cleaned_data['negative_prompt']
            width = form.cleaned_data['width']
            height = form.cleaned_data['height']
            seed = form.cleaned_data['seed']
            model = form.cleaned_data['model']
            directory = 'media/generated_images/'
            generated_image_path = '/' + SDGEN.txt2img_TEST(directory)

            if request.user.is_authenticated:
                Request.objects.create(
                    user=request.user,
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    width=width,
                    height=height,
                    seed=seed,
                    image=generated_image_path,
                    model=model
                )

            return JsonResponse({'generated_image_path': generated_image_path})
        else:
            return JsonResponse({'error': 'Invalid form data'}, status=400)
    else:
        form = ImageGenerationForm()
        return render(request, 'image_generation.html', {'form': form})
