from django.shortcuts import render
from .services import get_tutor_response


def chat_view(request):
    context = {}
    if request.method == "POST":
        question = request.POST.get("question", "").strip()

        if not question:
            context["error"] = "Iltimos, savol kiriting."
        else:
            try:
                result = get_tutor_response(question)
                context["question"] = question
                context["answer"] = result["final"]
            except RuntimeError as e:
                context["error"] = str(e)
                context["question"] = question

    return render(request, "tutor/chat.html", context)