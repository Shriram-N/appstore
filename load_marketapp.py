import sys, os
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mymarketapp.settings")

import django
django.setup()

from reviews.models import MarketApp


def save_marketapp_from_row(marketapp_row):
    marketapp = MarketApp()
    marketapp.id = marketapp_row[0]
    marketapp.name = marketapp_row[1]
    marketapp.save()


if __name__ == "__main__":

    if len(sys.argv) == 2:
        print "Reading from file " + str(sys.argv[1])
        marketapps_df = pd.read_csv(sys.argv[1])
        print marketapps_df

        marketapps_df.apply(
            save_marketapp_from_row,
            axis=1
        )

        

    else:
        print "Please, provide marketapp file path"
