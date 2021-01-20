from django.shortcuts import render
import subprocess  # noqa
import os
from Sentiment_analysis import settings
from .forms import User
import subprocess  # noqa
import sys
sys.path.append("..")
from Source.clean_user_data import cleaning
from Source.get_prediction import create_plots
from django.contrib import messages

# Create your views here.
def index(request):
    path_bars = ''
    path_pie = ''
    form = User(request.POST or None)

    if request.method == 'GET':
        form = User(request.GET)
        if form.is_valid():
            user = form.cleaned_data['user']
            path_bars = f'Users/{user}/{user}_bars_plot.png'
            path_pie = f'Users/{user}/{user}_pie_plot.png'
            if not os.path.exists(os.path.join(settings.BASE_DIR, '../' + path_bars)):
                os.mkdir(os.path.join(settings.BASE_DIR,f"../Users/{user}"))
                command = f"twint -u {user} --since 2020-01-01 --until 2020-12-31 -o ../Users/{user}/{user}.csv --csv"
                process = subprocess.Popen(
                    command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )
                output, error = process.communicate()
                if error:
                    path_bars = '/Users/admin/wrong.jpg'
                    os.rmdir(os.path.join(settings.BASE_DIR,f"../Users/{user}"))
                    path_pie = ''
                    messages.error(request, 'Invalid username!')
                else:
                    cleaning(user)
                    create_plots(user)

    plots = {'path_bars' : path_bars, 'path_pie':path_pie}
    context = {'info': plots, 'form':form}
    return render(request, 'twitter/index.html',context)

