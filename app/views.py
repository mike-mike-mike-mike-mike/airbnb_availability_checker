from django.shortcuts import redirect, render


def home(request):
    if request.user.is_authenticated:
        return redirect("trips:trip_list")
    else:
        return render(request, "home.html")
