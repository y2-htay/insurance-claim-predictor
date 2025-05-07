import requests
from django.http import HttpResponseForbidden

backend_url = "http://backend:8000/api"


def prepare_model_evaluation(data):
    try:
        results = []
        for name, (sv, ae) in enumerate(zip(data['settlement_values'], data['absolute_errors']), start=1):
            accuracy = 100 - (ae / sv * 100) if sv != 0 else 0
            results.append({
                'settlement_value': round(sv),
                'accuracy': round(accuracy, 2)
            })
    except:
        return None

    return results


def get_user_perm_level(headers):
    current_user_response = requests.get(f"{backend_url}/auth/users/me/", headers=headers)
    if current_user_response.status_code != 200:
        return HttpResponseForbidden("Authentication failed.")
    current_user = current_user_response.json()
    #  Enforce admin access only
    return current_user.get("permission_level")
