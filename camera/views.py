from django.shortcuts import render

def camera(requests):
    return render(requests, 'test/camera.html', {})