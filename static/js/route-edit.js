import {
  mapOptions,
  addMarker,
  parseCoordinates,
  formatCoordinates,
} from "./map_shared.js";

// Initialize route editing

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

function formatCoordinates(latlng) {
  return `${latlng.lat.toFixed(6)}, ${latlng.lng.toFixed(6)}`;
}

// Add marker function
function addMarker(coordinates, label) {
  const customMarker = L.icon({
    iconUrl: "/static/images/location-marker.png",
    iconSize: [20, 25],
  });

  const marker = L.marker(coordinates, {
    draggable: true,
    opacity: 0.8,
    icon: customMarker,
  })
    .addTo(map)
    .bindPopup(label)
    .openPopup();

  marker.on("dragend", function () {
    if (currentRoute?.startMarker && currentRoute?.endMarker) {
      fetchRoute(currentRoute);
    }
  });

  return marker;
}

function initializeRouteEdit() {
  console.log("Initializing route edit with data:", routeData); // Debug log

  if (routeData && routeData.startPoint && routeData.endPoint) {
    const startCoords = parseCoordinates(routeData.startPoint);
    const endCoords = parseCoordinates(routeData.endPoint);

    console.log("Parsed coordinates:", startCoords, endCoords); // Debug log

    if (startCoords && endCoords) {
      currentRoute = {
        startMarker: addMarker(
          [startCoords.lat, startCoords.lng],
          "Start Point"
        ),
        endMarker: addMarker([endCoords.lat, endCoords.lng], "End Point"),
        polyline: null,
      };

      console.log("Created current route:", currentRoute); // Debug log
      fetchRoute(currentRoute);
    }
  }
}

// Initialize the map for editing if we have route data
initializeRouteEdit();
