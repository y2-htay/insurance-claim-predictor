#!/bin/bash

# Run database migrations
python manage.py migrate

# Create dummy data only if database is empty
if ! python manage.py shell -c "
from backend_app.models import UserProfile, VehicleType, WeatherCondition;
admin_exists = UserProfile.objects.filter(username='admin_user').exists()
vehicle_exists = VehicleType.objects.exists()
weather_exists = WeatherCondition.objects.exists()
print(admin_exists and vehicle_exists and weather_exists)
" | grep -q True; then
    echo " Creating dummy data"
    python manage.py create_dummy_data
else
    echo " Dummy data already exists."
fi


# Start the server
exec "$@"
