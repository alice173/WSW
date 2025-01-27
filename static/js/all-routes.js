document.addEventListener("DOMContentLoaded", function () {
  const mapOptions = {
    minZoom: 9,
    maxZoom: 20,
    center: [50.5264, -4.5193],
    zoom: 9,
    maxBounds: [
      [49.528423, -10.76418],
      [61.331151, 1.9134116],
    ],
  };

  const routeMap = L.map("route-map", mapOptions);

  L.tileLayer("https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png", {
    attribution:
      '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  }).addTo(routeMap);

  // Utility function to parse coordinates
  function parseCoordinates(coordString) {
    if (!coordString) {
      console.error("No coordinate string provided");
      return null;
    }
    const [lat, lng] = coordString
      .split(",")
      .map((coord) => parseFloat(coord.trim()));
    if (isNaN(lat) || isNaN(lng)) {
      console.error("Parsing failed for coordinate string:", coordString);
      return null;
    }
    return { lat, lng };
  }

  // Function to load and display a saved route
  function loadSavedRoute(routeData) {
    const startCoords = parseCoordinates(routeData.start_point);
    const endCoords = parseCoordinates(routeData.end_point);

    // Validate coordinates
    if (
      !startCoords ||
      !endCoords ||
      isNaN(startCoords.lat) ||
      isNaN(startCoords.lng) ||
      isNaN(endCoords.lat) ||
      isNaN(endCoords.lng)
    ) {
      console.error("Invalid coordinates for route:", routeData);
      return;
    }

    const apiKey = "5b3ce3597851110001cf6248019e60e78b254057a4a19879ff29e229";
    const url = `https://api.openrouteservice.org/v2/directions/foot-walking?api_key=${apiKey}&start=${startCoords.lng},${startCoords.lat}&end=${endCoords.lng},${endCoords.lat}`;

    fetch(url)
      .then((response) => response.json())
      .then((data) => {
        const coordinates = data.features[0].geometry.coordinates.map(
          (coord) => [coord[1], coord[0]]
        );

        // Create polyline for saved route
        const polyline = L.polyline(coordinates, {
          color: "#ffd60a",
          weight: 4,
          opacity: 0.7,
        }).addTo(routeMap);

        // // Adjust map view to include all routes
        // routeMap.fitBounds(polyline.getBounds());
      })
      .catch((error) => console.error("Error loading saved route:", error));
  }

  // Function to load all saved routes
  function loadAllSavedRoutes() {
    if (typeof allRoutesData !== "undefined") {
      allRoutesData.forEach(loadSavedRoute);
    }
  }

  // Initial load of saved routes
  loadAllSavedRoutes();
});
