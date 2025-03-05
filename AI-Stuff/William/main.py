from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import pandas as pd
import tensorflow as tf
import keras
import keras_tuner as kt
from keras import layers
from baseline_model import base_model

dataset = pd.read_csv('Synthetic_Data_For_Students.csv')

tf.config.list_physical_devices('GPU')

redundant_labels = ['Accident Description', 'Injury Description', 'Claim Date', 'Accident Date',
                    'SpecialHealthExpenses', 'SpecialReduction', 'SpecialOverage', 'GeneralRest',
                    'SpecialAdditionalInjury', 'SpecialEarningsLoss', 'SpecialUsageLoss', 'SpecialMedications',
                    'SpecialAssetDamage', 'SpecialRehabilitation', 'SpecialFixes', 'GeneralFixed', 'GeneralUplift',
                    'SpecialLoanerVehicle', 'SpecialTripCosts', 'SpecialJourneyExpenses', 'SpecialTherapy']

category_labels = ['AccidentType', 'Exceptional_Circumstances', 'Minor_Psychological_Injury', 'Dominant injury',
                   'Whiplash', 'Vehicle Type', 'Weather Conditions',
                   'Police Report Filed', 'Witness Present', 'Gender']

numerical_labels = ['SettlementValue', 'Injury_Prognosis',
                    'Vehicle Age', 'Driver Age', 'Number of Passengers']


def clean_dataset(data):
    data.dropna(inplace=True)
    data.drop(redundant_labels, axis=1, inplace=True)
    return data


def categorise_data(data, label):
    categories = pd.get_dummies(data[label])
    data.drop(label, axis=1, inplace=True)
    data = pd.concat([data, categories], axis=1)
    return data


def extract_months(prognosis):
    return int(''.join(filter(str.isdigit, prognosis)))


def scale_data(data):
    scaler = StandardScaler()
    data[numerical_labels] = scaler.fit_transform(data[numerical_labels])
    return data


def preprocess_data(data):
    data = clean_dataset(data)
    data['Injury_Prognosis'] = data['Injury_Prognosis'].apply(extract_months)
    data = scale_data(data)
    for label in category_labels:
        data = categorise_data(data, label)
    return data


def build_model(hyper_parameters):
    model = keras.Sequential()
    model.add(layers.Dense(hyper_parameters.Int('units_1', min_value=32, max_value=256, step=32),
                           activation=hyper_parameters.Choice(
                               'activation_1', ['relu', 'tanh', 'leaky_relu']),
                           input_shape=(X_train_tf.shape[1],)))

    for i in range(hyper_parameters.Int('num_layers', 1, 3)):
        model.add(layers.Dense(hyper_parameters.Int(f'units_{i+2}', min_value=32, max_value=256, step=32),
                               activation=hyper_parameters.Choice(f'activation_{i+2}', ['relu', 'tanh', 'leaky_relu'])))
    model.add(layers.Dense(1))

    model.compile(
        optimizer=keras.optimizers.Adam(
            learning_rate=hyper_parameters.Choice('learning_rate', [0.01, 0.001, 0.0001])),
        loss='mse',
        metrics=['mae']
    )

    return model


def evaluate_model(model):
    test_loss, test_mae = model.evaluate(X_test_tf, y_test_tf)
    print(f'Test Loss: {test_loss}')
    print(f'Test MAE (Mean Absolute Error): {test_mae}')


dataset = preprocess_data(dataset)

X = dataset.drop('SettlementValue', axis=1)
y = dataset['SettlementValue']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)
X_train_np = X_train.values
X_test_np = X_test.values
y_train_np = y_train.values
y_test_np = y_test.values

X_train_tf = tf.convert_to_tensor(X_train_np, dtype=tf.float32)
X_test_tf = tf.convert_to_tensor(X_test_np, dtype=tf.float32)
y_train_tf = tf.convert_to_tensor(y_train_np, dtype=tf.float32)
y_test_tf = tf.convert_to_tensor(y_test_np, dtype=tf.float32)


base_model = base_model(X_train_tf)
base_model.fit(X_train_tf, y_train_tf, epochs=50,
               batch_size=32, validation_data=(X_test_tf, y_test_tf))

print("Base model results: No hyper parameter tuning:")
evaluate_model(base_model)

tuner = kt.RandomSearch(
    build_model,
    objective='val_mae',
    max_trials=15,
    executions_per_trial=2,
    directory='tuner_results',
    project_name='nerual_network_test'
)

tuner.search(X_train_tf, y_train_tf, epochs=50, batch_size=32,
             validation_data=(X_test_tf, y_test_tf))

best_hyper_parameters = tuner.get_best_hyperparameters(num_trials=1)[0]

tuned_model = tuner.hypermodel.build(best_hyper_parameters)

history = tuned_model.fit(X_train_tf, y_train_tf, epochs=50,
                          batch_size=32, validation_data=(X_test_tf, y_test_tf))

print("tuned model results: hyper parameters tuned:")
evaluate_model(tuned_model)

print(f'Best Hyper Parameters \n {best_hyper_parameters.get_config()}')
