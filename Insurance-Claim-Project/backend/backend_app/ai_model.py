import joblib
from django.core.files import File
from .models import InsuranceModel

HYPER_PARAMETERS = {}

def train_new_model(training_data):
    # model training code to go here, here is an example of how to save it
    # joblib.dump(model, 'insurance_model_temp.pkl')
    # insurance_model = InsuranceModel(name="InsuranceModel")
    # with open('insurance_model_temp.pkl', 'rb') as f:
    # insurance_model.model_file.save('insurance_model.pkl', File(f))
    # insurance_model.save()
    pass


def predict(claim_data):
    # loading model example
    # insurance_model = InsuranceModel.objects.get(name="InsuranceModel")
    # model = joblib.load(insurance_model.model_file.path)
    # predictions to return
    pass
