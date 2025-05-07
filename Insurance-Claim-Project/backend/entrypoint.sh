#!/bin/bash

python manage.py migrate



if ! python manage.py shell -c "
from backend_app.models import UserProfile, VehicleType, WeatherCondition, UserClaims
import sys
if not (UserProfile.objects.filter(username='anadmin').exists() and UserProfile.objects.filter(username='drfirst').exists() and VehicleType.objects.exists() and WeatherCondition.objects.exists() and UserClaims.objects.exists()):
    sys.exit(1)
" ; then
    echo "Creating dummy data"
    python manage.py create_dummy_data
else
    echo "Dummy data already exists."
fi





exec "$@"
