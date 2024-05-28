from django.contrib.auth import login, authenticate, get_backends
from django.contrib.auth.forms import UserCreationForm, User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json
from .forms import ImageGenerationForm, UserCreationForm
from .models import Request, Model, Favourite, Profile, Gallery
from . import SDGEN

@login_required
def redirect_to_profile(request):
    return redirect('profile_view', user_id=request.user.id)
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('user_profile')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def profile_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user_requests = Request.objects.filter(user=user).order_by('-id')
    user_favourites = Favourite.objects.filter(user=user).select_related('request')
    return render(request, 'profile.html', {'profile_user': user, 'requests': user_requests, 'favourites': user_favourites})
@login_required
def profile(request):
    user_requests = Request.objects.filter(user=request.user).order_by('-id')
    favourites = Favourite.objects.filter(user=request.user)
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        favourite_id = request.POST.get('favourite_id')
        if request_id:
            selected_request = get_object_or_404(Request, id=request_id)
            Favourite.objects.create(user=request.user, request=selected_request)
            return redirect('user_profile')
        if favourite_id:
            favourite = get_object_or_404(Favourite, id=favourite_id, user=request.user)
            favourite.delete()
            return redirect('user_profile')
    return render(request, 'profile.html', {'requests': user_requests, 'favourites': favourites})

@login_required
def remove_favourite(request):
    if request.method == 'POST':
        favourite_id = request.POST.get('favourite_id')
        favourite = get_object_or_404(Favourite, id=favourite_id, user=request.user)
        favourite.delete()
        return JsonResponse({'status': 'removed from favourites'})

def gallery_view(request):
    gallery_items = Gallery.objects.all().order_by('-added_at')
    if request.method == 'POST':
        image_id = request.POST.get('image_id')
        selected_request = get_object_or_404(Request, id=image_id)
        Favourite.objects.create(user=request.user, request=selected_request)
        return redirect('gallery_view')
    return render(request, 'gallery.html', {'gallery_items': gallery_items})

def image_generation_view(request):
    if request.method == 'POST':
        form = ImageGenerationForm(request.POST)
        if form.is_valid():
            directory = 'media/generated_images/'
            prompt = form.cleaned_data['prompt']
            negative_prompt = form.cleaned_data['negative_prompt']
            width = form.cleaned_data['width']
            height = form.cleaned_data['height']
            seed = form.cleaned_data['seed']
            model = form.cleaned_data['model']
            print(model)
            SDreq = json.loads(SDGEN.txt2img_TEST(directory, model))#json.loads(SDGEN.txt2img(prompt, negative_prompt, seed, width, height, directory, model))
            generated_image_path = '/' + SDreq['path']
            if request.user.is_authenticated:
                generated_request = Request.objects.create(
                    user=request.user,
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    width=width,
                    height=height,
                    seed=SDreq['info']['seed'],
                    image=generated_image_path,
                    model=model
                )
                Gallery.objects.create(user=request.user, image=generated_request)

            return JsonResponse({'generated_image_path': generated_image_path})
        else:
            return JsonResponse({'error': 'Invalid form data'}, status=400)
    else:
        form = ImageGenerationForm()
        return render(request, 'image_generation.html', {'form': form})
