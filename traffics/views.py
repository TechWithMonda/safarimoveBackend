import requests
from django.http import JsonResponse
from django.conf import settings

def get_traffic_data(request):
    origin = request.GET.get('origin', 'Kasarani,Nairobi')
    destination = request.GET.get('destination', 'CBD,Nairobi')
    api_key = settings.GOOGLE_MAPS_API_KEY

    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": origin,
        "destinations": destination,
        "departure_time": "now",
        "key": api_key,
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data['status'] != "OK":
        return JsonResponse({"error": "API error", "details": data}, status=400)

    element = data['rows'][0]['elements'][0]

    distance = element['distance']['text']
    duration = element['duration']['text']
    traffic_duration = element.get('duration_in_traffic', {}).get('text', duration)

    # Compute traffic level
    normal_time = element['duration']['value']
    traffic_time = element.get('duration_in_traffic', {}).get('value', normal_time)
    diff = traffic_time - normal_time

    if diff > 1200:
        traffic_level = "severe"
    elif diff > 600:
        traffic_level = "heavy"
    elif diff > 300:
        traffic_level = "moderate"
    else:
        traffic_level = "light"

    return JsonResponse({
        "origin": origin,
        "destination": destination,
        "distance": distance,
        "duration": duration,
        "duration_in_traffic": traffic_duration,
        "traffic_level": traffic_level
    })
