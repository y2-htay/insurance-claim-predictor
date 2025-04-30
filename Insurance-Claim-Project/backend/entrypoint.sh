#!/bin/bash

python manage.py migrate



if ! python manage.py shell -c "
from backend_app.models import UserProfile, VehicleType, WeatherCondition;
admin_exists = UserProfile.objects.filter(username='anadmin').exists()
ai_exists = UserProfile.objects.filter(username='drfirst').exists()
vehicle_exists = VehicleType.objects.exists()
weather_exists = WeatherCondition.objects.exists()
print(admin_exists and ai_exists and vehicle_exists and weather_exists)
" | grep -q True; then
    echo "Creating dummy data"
    python manage.py create_dummy_data
else
    echo "Dummy data already exists. "
fi


exec "$@"
