import sys

sys.path.append("..")
from Source.clean_user_data import cleaning  # noqa
from Source.get_prediction import create_plots  # noqa

from celery import shared_task  # noqa


@shared_task(bind=True)
def get_statistics(self, user):
    cleaning(user)
    create_plots(user)
    path_bars = f"Users/{user}/{user}_bars_plot.png"
    path_pie = f"Users/{user}/{user}_pie_plot.png"
    return {"path_bars": path_bars, "path_pie": path_pie}
