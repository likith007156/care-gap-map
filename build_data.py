"""Pull Karnataka healthcare facilities + villages from OpenStreetMap, compute each
village's distance to the nearest hospital/clinic, write GeoJSON, optionally upload to S3.
Usage: pip install requests numpy boto3 ; python build_data.py [your-s3-bucket]"""
import json, os, sys, requests, numpy as np

import time
MIRRORS = ["https://overpass-api.de/api/interpreter", "https://overpass.kumi.systems/api/interpreter",
           "https://overpass.private.coffee/api/interpreter"]
HEADERS = {"User-Agent": "care-gap-map/1.0 (AWS Builder Center hackathon project)", "Accept": "application/json"}
def q(body):
    query = f'[out:json][timeout:300];area["ISO3166-2"="IN-KA"]->.a;{body};out center tags;'
    for attempt in range(6):
        url = MIRRORS[attempt % len(MIRRORS)]
        try:
            r = requests.post(url, data={"data": query}, headers=HEADERS, timeout=400)
            if r.status_code == 200:
                return r.json()["elements"]
            print(f"  {url} returned {r.status_code}, retrying...")
        except requests.RequestException as ex:
            print(f"  {url} failed ({ex.__class__.__name__}), retrying...")
        time.sleep(10)
    raise SystemExit("Overpass is busy or blocked. Wait a few minutes and run again.")
def pt(e): return (e["lon"], e["lat"]) if "lon" in e else (e["center"]["lon"], e["center"]["lat"])

fac = []
for e in q('nwr["amenity"~"^(hospital|clinic|doctors|pharmacy)$"](area.a)'):
    x, y = pt(e)
    fac.append({"type": "Feature", "geometry": {"type": "Point", "coordinates": [x, y]},
                "properties": {"name": e["tags"].get("name", ""), "type": e["tags"]["amenity"]}})
vil = [(pt(e), e["tags"].get("name:en") or e["tags"].get("name", "")) for e in q('node["place"~"^(village|town|hamlet)$"](area.a)')]
print(len(fac), "facilities,", len(vil), "villages")

care = np.radians(np.array([f["geometry"]["coordinates"] for f in fac if f["properties"]["type"] in ("hospital", "clinic")]))
V = np.radians(np.array([v for v, _ in vil])); km = np.empty(len(V))
for i in range(0, len(V), 500):  # haversine in chunks
    b = V[i:i+500, None, :]; d = care[None, :, :] - b
    h = np.sin(d[..., 1]/2)**2 + np.cos(b[..., 1])*np.cos(care[None, :, 1])*np.sin(d[..., 0]/2)**2
    km[i:i+500] = (12742*np.arcsin(np.sqrt(h))).min(axis=1)

os.makedirs("data", exist_ok=True)
json.dump({"type": "FeatureCollection", "features": fac}, open("data/facilities.geojson", "w"))
json.dump({"type": "FeatureCollection", "features": [
    {"type": "Feature", "geometry": {"type": "Point", "coordinates": list(v)}, "properties": {"km": round(float(k), 1), "name": n}}
    for (v, n), k in zip(vil, km)]}, open("data/villages.geojson", "w"))

if len(sys.argv) > 1:
    import boto3; s3 = boto3.client("s3")
    for f in ("facilities", "villages"):
        s3.upload_file(f"data/{f}.geojson", sys.argv[1], f"data/{f}.geojson", ExtraArgs={"ContentType": "application/geo+json"})
    s3.upload_file("index.html", sys.argv[1], "index.html", ExtraArgs={"ContentType": "text/html"})
    print("uploaded to s3://" + sys.argv[1])
