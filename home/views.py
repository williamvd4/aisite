from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from .forms import MyForm
from .models import MyFormModel, Lesson, Material, Resource, Curriculum
from .ai.ai_review import review_lesson, generate_ai_response
from .ai.ai_utils import analyze_text
from django.conf import settings
import cohere
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def lesson_detail(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    ai_feedback = analyze_text(lesson.description)
    return render(
        request, "lesson_detail.html", {"lesson": lesson, "ai_feedback": ai_feedback}
    )


def home(request):
    return render(request, "pages/home.html")


def mylessonplans(request):
    return render(request, "pages/mylessonplans.html")


def welcome(request):
    return render(request, "pages/welcome.html")


def createnewlesson(request):
    if request.method == "POST":
        form = MyForm(request.POST)
        if form.is_valid():
            # Process the form data
            # Process the form data
            lesson = form.save()
            messages.success(request, "Lesson created successfully!")
    else:
        form = MyForm()

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        # This is an AJAX request for AI chat
        user_input = request.POST.get("ai_input", "")
        ai_response = generate_ai_response(user_input)
        return JsonResponse({"ai_response": ai_response})

    return render(request, "pages/createnewlesson.html", {"form": form})


def mycalendar(request):
    return render(request, "pages/mycalendar.html")


@login_required
def mycurriculums(request):
    curriculums = Curriculum.objects.filter(user=request.user)
    return render(request, "pages/mycurriculums.html", {"curriculums": curriculums})


def myresources(request):
    return render(request, "pages/myresources.html")


def signup(request):
    return render(request, "pages/signup.html")


def ai_chat(request):
    ai_response = ""
    user_input = ""

    if request.method == "POST":
        user_input = request.POST.get("ai_input", "")
        co = cohere.Client(settings.COHERE_API_KEY)

        if user_input:
            try:
                response = co.generate(
                    model="command-xlarge-nightly",
                    prompt=user_input,
                    max_tokens=150,
                    temperature=0.7,
                    k=0,
                    stop_sequences=[],
                    return_likelihoods="NONE",
                )
                ai_response = response.generations[0].text.strip()
            except cohere.CohereError as e:
                ai_response = f"Error: {str(e)}"

    return render(
        request,
        "ai/ai_chat.html",
        {"ai_response": ai_response, "user_input": user_input},
    )


@require_POST
def upload_curriculum(request):
    if request.FILES.get("file"):
        file = request.FILES["file"]
        curriculum = Curriculum(title=file.name, user=request.user, file=file)
        curriculum.save()
        return JsonResponse(
            {
                "message": "File uploaded successfully",
                "file_name": file.name,
                "file_url": curriculum.file.url,
            }
        )
    return JsonResponse({"error": "No file uploaded"}, status=400)


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        remember_me = request.POST.get("remember_me")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if not remember_me:
                request.session.set_expiry(0)
            return redirect("home")  # Redirect to a success page.
        else:
            # Return an 'invalid login' error message.
            return render(
                request, "pages/welcome.html", {"error": "Invalid username or password"}
            )
    else:
        return render(request, "pages/welcome.html")


@require_POST
def ai_chat(request):
    user_input = request.POST.get("ai_input", "")
    ai_file = request.FILES.get("ai_file")

    # Process the user input and file (if any) using your AI logic
    ai_response = generate_ai_response(user_input)

    return JsonResponse({"ai_response": ai_response})
