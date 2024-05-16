from django.shortcuts import render
from django.http import JsonResponse
from .forms import ImageGenerationForm
from . import SDGEN
from django.contrib import messages

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
