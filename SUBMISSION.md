# Submission text (paste into Builder Center, edit the numbers)

**Title:** Care Gap Map: how far is a hospital from every village in Karnataka?

**Tagline:** I mapped every OpenStreetMap village in Karnataka against its nearest hospital or clinic. 16.2% are more than 10 km away. Click any spot to see the real drive.

**Dataset:** OpenStreetMap healthcare facilities (hospitals, clinics, doctors, pharmacies) and villages/towns in Karnataka, pulled via Overpass. No personal data.

**How I put it on the map:** A Python script computes each village's distance to its nearest hospital or clinic and writes GeoJSON to Amazon S3, hosted with S3 static website hosting. MapLibre renders the Amazon Location Standard map with clustered facilities and villages colored by distance. Amazon Location Places geocodes searches, Routes gives the real driving route and time from any clicked point, and Routes isolines draw the 30 and 60 minute service area of the nearest facility, so you can see which villages fall outside it.

**AWS services:** Amazon Location Service (Maps, Places, Routes incl. isolines), Amazon S3 (data storage and static website hosting).

**What people can explore:** access grade A-F for any point, nearest 3 facilities, driving route, 30/60 minute service area, facility filters, most remote villages, guided tour, shareable links.

**Reuse:** swap the Overpass query and the state code for any region or facility type (schools, banks, ATMs).

**Limits:** OSM coverage varies, so figures describe mapped villages. Distance coloring is straight-line; road routes and isolines are shown on click. Next step: Athena/Iceberg tables and population weighting.
