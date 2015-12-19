import math

# calculate stop-current distance
# getDistanceFromLatLonInKm
def dis(lat1,lon1,lat2,lon2):
    R = 6371 #Radius of the earth in km
    dLat = deg2rad(lat2-lat1)
    dLon = deg2rad(lon2-lon1)
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(deg2rad(lat1)) * math.cos(deg2rad(lat2)) * math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c #Distance in km
    return d

def deg2rad(deg):
    return deg * (math.pi/180)
