from django.shortcuts import render

from main.models import Experience


def show_main(request):
    context = {
        "name": "Rapip Ananta Marpaung",
        "npm": "2506585151",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "IT Enthusiast, Third semester, Studying at Fasilkom UI"
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Rapip Ananta Marpaung",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)