import sys, os 
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "winerama.settings")

import django
django.setup()

from reviews.models import Wine 


def save_wine_from_row(wine_row):
    wine = Wine()
    wine.id = wine_row[0]
    wine.name = wine_row[1]
    wine.save()
    
    
if __name__ == "__main__":
    
    if len(sys.argv) == 2:
        print "Reading from file " + str(sys.argv[1])
        wines_df = pd.read_csv(sys.argv[1])
        print wines_df

        wines_df.apply(
            save_wine_from_row,
            axis=1
        )

        print "There are {} wines".format(Wine.objects.count())
        
    else:
        print "Please, provide Wine file path"
