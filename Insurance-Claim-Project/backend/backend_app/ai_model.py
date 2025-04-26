import keras
import tensorflow as tf
import pandas as pd
from keras import layers, regularizers, optimizers, losses
from django.core.files import File
from .models import InsuranceModel, ClaimTrainingData

HYPER_PARAMETERS = {}
MODEL_FILE_NAME = 'insurance_model.h5'


def get_input_shape():
    claim_training_data_object = ClaimTrainingData.objects.latest('id')
    path = claim_training_data_object.data_file.path
    data = pd.read_csv(path)
    X = data.drop('SettlementValue', axis=1)
    y = data['SettlementValue']
    X_np = X.to_numpy()
    X_train_tf = tf.convert_to_tensor(X_np, dtype=tf.float32)
    return X_train_tf.shape[1]


def train_new_model():
    model = keras.Sequential()
    model.add(layers.Input(shape=(get_input_shape(),)))
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
    insurance_model = InsuranceModel(model_file="InsuranceModel")
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
