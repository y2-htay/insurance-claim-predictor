from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import KFold
import pandas as pd
import tensorflow as tf
import keras
import keras_tuner as kt
from keras import layers
from tf_keras.callbacks import EarlyStopping
from baseline_model import base_model
import numpy as np

K = 5
test_results = []
k_fold = KFold(n_splits=K, shuffle=True, random_state=42)

dataset = pd.read_csv('../Dataset/Synthetic_Data_For_Students.csv')
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


def build_model(hyper_parameters, input_shape):
    model = keras.Sequential()
    model.add(layers.Dense(hyper_parameters.Int('units_1', min_value=32, max_value=256, step=32),
                           activation=hyper_parameters.Choice(
                               'activation_1', ['relu', 'tanh', 'leaky_relu']),
                           input_shape=(input_shape,)))

    model.add(layers.Dropout(hyper_parameters.Float(
        'dropout_1', 0.2, 0.5, step=0.05)))

    for i in range(hyper_parameters.Int('num_layers', 1, 3)):
        model.add(layers.Dense(hyper_parameters.Int(f'units_{i+2}', min_value=32, max_value=256, step=32),
                               activation=hyper_parameters.Choice(f'activation_{i+2}', ['relu', 'tanh', 'leaky_relu'])))

        model.add(layers.Dropout(hyper_parameters.Float(
            f'dropout_{i+2}', 0.2, 0.5, step=0.05)))

    model.add(layers.Dense(1))

    model.compile(
        optimizer=keras.optimizers.Adam(
            learning_rate=hyper_parameters.Choice('learning_rate', [0.01, 0.001, 0.0001])),
        loss='mse',
        metrics=['mae']
    )

    return model


def evaluate_model(model, X_test_tf, y_test_tf):
    test_mae = model.evaluate(X_test_tf, y_test_tf)
    return test_mae


def cross_validate_model(model_builder, X_np, y_np, k_fold):
    fold_mae_scores = []
    for fold_num, (train_index, test_index) in enumerate(k_fold.split(X_np), start=1):
        print(f"Processing fold {fold_num}/{k_fold.get_n_splits()}")
        X_train_fold, X_test_fold = X_np[train_index], X_np[test_index]
        y_train_fold, y_test_fold = y_np[train_index], y_np[test_index]

        X_train_tf = tf.convert_to_tensor(X_train_fold, dtype=tf.float32)
        X_test_tf = tf.convert_to_tensor(X_test_fold, dtype=tf.float32)
        y_train_tf = tf.convert_to_tensor(y_train_fold, dtype=tf.float32)
        y_test_tf = tf.convert_to_tensor(y_test_fold, dtype=tf.float32)

        model = model_builder(X_train_tf)

        early_stopping = EarlyStopping(
            monitor='val_mae',
            patience=10,
            restore_best_weights=True,
            verbose=1
        )

        model.fit(
            X_train_tf, y_train_tf,
            epochs=50,
            batch_size=32,
            validation_data=(X_test_tf, y_test_tf),
            callbacks=[early_stopping]  # Apply early stopping
        )

        fold_mae = evaluate_model(model, X_test_tf, y_test_tf)
        fold_mae_scores.append(fold_mae)

    average_mae = np.mean(fold_mae_scores)
    print(f'Average MAE across {k_fold.get_n_splits()} folds: {average_mae}')
    return average_mae


dataset = preprocess_data(dataset)

X = dataset.drop('SettlementValue', axis=1)
y = dataset['SettlementValue']

X_np = X.values
y_np = y.values

print("Base model results: No hyperparameter tuning:")
test_results.append(cross_validate_model(base_model, X_np, y_np, k_fold))

tuner = kt.RandomSearch(
    lambda hp: build_model(hp, X_np.shape[1]),
    objective='val_mae',
    max_trials=15,
    executions_per_trial=2,
    directory='tuner_results',
    project_name='neural_network_test'
)

# Use a single train-test split for hyperparameter tuning
X_train_tf = tf.convert_to_tensor(X_np, dtype=tf.float32)
y_train_tf = tf.convert_to_tensor(y_np, dtype=tf.float32)

early_stopping = EarlyStopping(
    monitor='val_mae', patience=10, restore_best_weights=True, verbose=1)

tuner.search(X_train_tf, y_train_tf, epochs=50, batch_size=32,
             validation_split=0.2, callbacks=[early_stopping])

best_hyper_parameters = tuner.get_best_hyperparameters(num_trials=1)[0]


def tuned_model_builder(X_train_tf):
    return build_model(best_hyper_parameters, X_train_tf.shape[1])


test_results.append(cross_validate_model(
    tuned_model_builder, X_np, y_np, k_fold))


print("Average Mean Absolute Error for untuned model:")
print(test_results[0])

print("Average Mean Absolute Error for tuned model:")
print(test_results[1])

print(f'Best Hyper Parameters \n {best_hyper_parameters.get_config()}')
