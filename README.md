# Care Gap Map: Karnataka

How far is the nearest hospital or clinic from every village? An explorable map built on Amazon Location Service.

**Pipeline:** OpenStreetMap (Overpass) -> `build_data.py` (distance per village) -> Amazon S3 (GeoJSON, static website hosting) -> MapLibre + Amazon Location (maps, geocoding, routing, isolines).

## Run
1. `pip install requests numpy boto3`
2. `python build_data.py YOUR_BUCKET` (omit the bucket to write `data/` locally)
3. Create an Amazon Location API key (Maps, Places, Routes), restrict it to your site's domain, and put it in `config.js` (key and region).
4. Host `index.html`, `config.js` and `data/` on S3 static website hosting.

## Explore
Click anywhere for an access grade (A-F), the 3 nearest facilities, a driving route and a 30/60 minute drive-time service area (Amazon Location isolines). Search a place, filter facility types, jump to the most remote villages, play the guided tour, or copy a link to the current view.

## Amazon Location features used
Maps (Standard style), Places (geocode), Routes (calculate routes + isolines).

Data: OpenStreetMap contributors (ODbL). No personal data.

## Method and limits
- Data: OpenStreetMap contributors (ODbL), pulled with Overpass: 7,395 healthcare facilities and 24,573 villages/towns/hamlets in Karnataka.
- Coverage metric: straight-line (haversine) distance from each village to its nearest hospital or clinic. 16.2% of mapped villages are 10 km or more away.
- On click: Amazon Location Routes (driving route and time) and isolines (30/60 minute drive area of the nearest facility).
- Limits: OSM coverage varies, so figures describe mapped villages only. Colours use straight-line distance, not road distance. Not a substitute for official health-facility registries.
- Your own API key goes in `config.js` (restrict it to your site's domain).
