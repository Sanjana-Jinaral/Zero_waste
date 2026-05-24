import math
from datetime import datetime

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    if None in [lat1, lon1, lat2, lon2]:
        return None
        
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

def calculate_eta(distance_km, speed_kmh=20):
    """
    Calculate ETA in minutes based on distance and average speed.
    Default speed is 20km/h (suitable for Bangalore traffic).
    """
    if distance_km is None:
        return None
    if distance_km == 0:
        return 0
    
    hours = distance_km / speed_kmh
    minutes = hours * 60
    return round(minutes)

def get_expiry_status(expiry_time):
    """
    Returns a human-readable string of time remaining before expiry.
    """
    if not expiry_time:
        return "Unknown"
    
    now = datetime.utcnow()
    diff = expiry_time - now
    
    if diff.total_seconds() <= 0:
        return "Expired"
    
    hours = int(diff.total_seconds() // 3600)
    minutes = int((diff.total_seconds() % 3600) // 60)
    
    if hours > 0:
        return f"{hours}h {minutes}m remaining"
    else:
        return f"{minutes}m remaining"
