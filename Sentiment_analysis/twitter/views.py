import os
import subprocess  # noqa
import sys

from Sentiment_analysis import settings

from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import User
from .models import Usernames
from .tasks import get_statistics

sys.path.append("..")


def index(request):  # noqa
    form = User(request.POST or None)

    if request.method == "POST":
        form = User(request.POST)

        if form.is_valid():
            user = form.cleaned_data["username"]

            if not Usernames.objects.filter(username=user):
                output, error = get_tweets(user)

                if error:
                    remove_dir(user)  # noqa
                    messages.error(request, "Invalid username!")
                    context = {
                        "info": {"error": "/Users/admin/wrong.jpg"},
                        "form": form,
                    }
                    return render(request, "twitter/index.html", context)

                else:
                    get_statistics.delay(user)
                    form.save()
                    return redirect(f"http://127.0.0.1:8000/profiles/{user}/")
            else:
                return redirect(f"http://127.0.0.1:8000/profiles/{user}/")

    return render(request, "twitter/index.html", {"form": form})


def get_tweets(user):
    os.mkdir(os.path.join(settings.BASE_DIR, f"../Users/{user}"))
    begin = "2020-01-01"
    end = "2020-12-31"

    command = f"twint -u {user} --since {begin} --until {end} -o ../Users/{user}/{user}.csv --csv"  # noqa
    process = subprocess.Popen(  # noqa
        command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    return process.communicate()


def remove_dir(user):
    os.rmdir(os.path.join(settings.BASE_DIR, f"../Users/{user}"))


def profile(request, username):
    path_bars = f"Users/{username}/{username}_bars_plot.png"
    path_pie = f"Users/{username}/{username}_pie_plot.png"
    info = {"path_bars": path_bars, "path_pie": path_pie, "user": username}
    context = {"info": info}
    return render(request, "twitter/profile.html", context)


def profiles(request):
    users = Usernames.objects.all()

    all_users = []
    for user in users:
        user_info = {
            "user": user,
        }
        all_users.append(user_info)

    context = {"all_info": all_users}
    return render(request, "twitter/profiles.html", context)
