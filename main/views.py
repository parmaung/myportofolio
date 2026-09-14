from django.shortcuts import render

from main.models import Experience, Project


def show_main(request):
    context = {
        "name": "Rafif Ananta Marpaung",
        "npm": "2506585151",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "IT Enthusiast, Third semester, Studying at Fasilkom UI"
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Rafif Ananta Marpaung",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)


def show_projects(request):
    context = {
        "name": "Rafifs Ananta Marpaung",
        "project_list": Project.objects.all(),
    }
    return render(request, "project.html", context)
