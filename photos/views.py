from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Category, Photo

def gallery(request):
    category = request.GET.get('category')
    if category == None:
        photos = Photo.objects.all()
    else:
        photos = Photo.objects.filter(category__name=category)
        
    context = {'categories': Category.objects.all(), 'photos': photos}
    return render(request, 'photos/gallery.html', context)

def viewPhoto(request, pk):
    context = {'photo': Photo.objects.get(id=pk)}
    return render(request, 'photos/photo.html', context)

@login_required
def addPhoto(request):
    context = {'categories': Category.objects.all()}

    if request.method == "POST":
        data = request.POST
        images = request.FILES.getlist('image') # name of input files in add.html 

        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        else:
            category = None

        for image in images:
            photo = Photo.objects.create(
                category=category,
                description=data['description'],
                image=image,
            )
        return redirect('gallery')

    return render(request, 'photos/add.html', context)