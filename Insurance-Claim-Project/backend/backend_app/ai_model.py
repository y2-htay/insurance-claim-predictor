import keras
from keras import layers, regularizers, optimizers, losses
from django.core.files import File

from .models import InsuranceModel

HYPER_PARAMETERS = {}
MODEL_FILE_NAME = 'insurance_model.tmp'


def train_new_model(input_shape):
    model = keras.Sequential()
    model.add(layers.Input(shape=input_shape))
    model.add(layers.Dense(96, activation='tanh', kernel_regularizer=regularizers.l2(0.00018614191986076204)))
    model.add(layers.Dropout(0.24474266394256658))
    model.add(layers.Dense(32, activation='tanh', kernel_regularizer=regularizers.l2(0.0001299876307582759)))
    model.add(layers.Dropout(0.1432658754821588))
    model.add(layers.BatchNormalization())
    model.add(layers.Dense(32, activation='relu', kernel_regularizer=regularizers.l2(0.00011991372800004211)))
    model.add(layers.Dropout(0.0493930126234396))
    model.add(layers.BatchNormalization())
    model.add(layers.Dense(1, activation='softplus'))
    model.compile(optimizer=optimizers.Adam(
        learning_rate=0.003225943238477045
    ),
        loss=losses.Huber(delta=0.5359404627944264),
        metrics=['mae'])

    model.save(MODEL_FILE_NAME)
    insurance_model = InsuranceModel(name="InsuranceModel")
    with open(MODEL_FILE_NAME, 'rb') as f:
        insurance_model.model_file.save(MODEL_FILE_NAME, File(f))
        insurance_model.save()


def predict(claim_data):
    try:
        insurance_model = InsuranceModel.objects.latest('id')
        model = keras.models.load_model(insurance_model.model_file.path)
    except InsuranceModel.DoesNotExist:
        raise ValueError("No trained model found.")

    predictions = model.predict(claim_data)

    return predictions
