from django.shortcuts import render
from .models import Student

def register(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        Student.objects.create(
            name=name,
            email=email,
            password=password
        )

        return render(request, "register.html")

    return render(request, "register.html")
