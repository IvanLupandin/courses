from django.shortcuts import render, redirect
from .forms import AdvertisementForm, ResponseForm
from .models import Advertisement, Response, News
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, NewsForm


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # Действия после успешной регистрации
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def create_advertisement(request):
    if request.method == 'POST':
        form = AdvertisementForm(request.POST)
        if form.is_valid():
            advertisement = form.save(commit=False)
            advertisement.author = request.user
            advertisement.save()
            return redirect('advertisement_detail', pk=advertisement.pk)
    else:
        form = AdvertisementForm()
    return render(request, 'create_advertisement.html', {'form': form})


def edit_advertisement(request, pk):
    advertisement = Advertisement.objects.get(pk=pk)
    if request.user == advertisement.author:
        if request.method == 'POST':
            form = AdvertisementForm(request.POST, instance=advertisement)
            if form.is_valid():
                advertisement = form.save()
                return redirect('advertisement_detail', pk=advertisement.pk)
        else:
            form = AdvertisementForm(instance=advertisement)
        return render(request, 'edit_advertisement.html', {'form': form, 'advertisement': advertisement})
    else:
        # Обработка случая, когда пользователь не является автором объявления
        return redirect('home')


def private_responses(request):
    responses = Response.objects.filter(advertisement__author=request.user)
    return render(request, 'private_responses.html', {'responses': responses})


def send_response(request, pk):
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.advertisement = Advertisement.objects.get(pk=pk)
            response.author = request.user
            response.save()
            # Логика для отправки уведомлений по электронной почте
            return redirect('advertisement_detail', pk=pk)
    else:
        form = ResponseForm()
    return render(request, 'send_response.html', {'form': form})


def create_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save()
            # Дополнительные действия после сохранения новости
    else:
        form = NewsForm()
    return render(request, 'create_news.html', {'form': form})





