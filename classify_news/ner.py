from .models import NamedEntityRecognition
import pandas as pd

ner = NamedEntityRecognition.objects.all()


def get_ner_df():
    df = pd.DataFrame.from_records(ner.values())
    return df