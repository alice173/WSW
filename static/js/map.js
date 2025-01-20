console.log("map.js is loaded");

// Initialize Leaflet map
const baseMap = L.tileLayer(
  "https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png",
  {
    attribution:
      '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  }
);

const mapOptions = {
  minZoom: 9,
  maxZoom: 20,
  center: [50.5264, -4.5193],
  zoom: 9,
  maxBounds: [
    [49.528423, -10.76418],
    [61.331151, 1.9134116],
  ],
  layers: [baseMap],
};

const map = L.map("map", mapOptions);

const baseLayers = {
  "Base Map": baseMap,
};

// Create a layer group to hold all polylines
const polylineLayer = L.layerGroup([]).addTo(map);

// Add controls to switch layers
const layerControl = L.control
  .layers(baseLayers, {}, { collapsed: false, position: "topleft" })
  .addTo(map);

// Initialize Geocoder
const geocoder = L.Control.Geocoder.nominatim();
L.Control.geocoder({
  geocoder: geocoder,
  placeholder: "Enter location or postcode...",
  errorMessage: "Nothing found.",
})
  .on("markgeocode", function (e) {
    const coordinates = e.geocode.center;
    addMarker(coordinates, e.geocode.name);
  })
  .addTo(map);

// Arrays to track multiple routes and markers
const routes = [];
let coords = [];

// Click event handler function
function onMapClick(e) {
  const coordinates = e.latlng;
  console.log("Clicked coordinates:", coordinates);

  if (
    routes.length === 0 || // No routes exist yet
    routes[routes.length - 1].endMarker // Last route is complete
  ) {
    // Start a new route
    const newRoute = {
      startMarker: addMarker(coordinates, "Start Point"),
      endMarker: null,
      polyline: null,
    };
    coords.push(coordinates);
    console.log("diatnce a", coords);
    routes.push(newRoute);
    console.log("Started new route:", newRoute);
  } else {
    // Complete the active route
    const activeRoute = routes[routes.length - 1];
    activeRoute.endMarker = addMarker(coordinates, "End Point");
    console.log("End marker set:", activeRoute);
    coords.push(coordinates);
    console.log("diatnce c", coords);

    // Fetch and draw the route
    fetchRoute(activeRoute);

    // Calculate distance between the two markers
    const distanceEl = document.querySelector("#distance span");
    const distanceInput = document.getElementById("id_distance");
    console.log("element" + distanceEl);
    let distance = map.distance(coords[0], coords[1]);
    console.log("dist calc", distance);
    const distanceMiles = parseFloat((distance / 1609).toFixed(2)); // Convert to string with 2 decimal places - parse float to convert back to number
    distanceEl.innerText = `${distanceMiles} Miles`;
    distanceInput.value = distanceMiles;
  }
}

// Add event listener to the toggle button
document
  .getElementById("toggle-polylines")
  .addEventListener("click", function () {
    if (map.hasLayer(polylineLayer)) {
      map.removeLayer(polylineLayer);
      map.off("click", onMapClick); // Remove click event listener
    } else {
      map.addLayer(polylineLayer);
      map.on("click", onMapClick); // Add click event listener
    }
  });

// Initially add the click event listener
map.on("click", onMapClick);

// Function to add a marker
const customMarker = L.icon({
  iconUrl: ".../images/location-marker.png",
  iconSize: [20, 25],
});

function addMarker(coordinates, label) {
  const marker = L.marker(coordinates, {
    draggable: true,
    opacity: 0.8,
    icon: customMarker,
  })
    .addTo(map)
    .bindPopup(label)
    .openPopup();

  // Add event listener for drag end to update the route dynamically
  marker.on("dragend", function () {
    const routeToUpdate = routes.find(
      (route) => route.startMarker === marker || route.endMarker === marker
    );
    if (routeToUpdate && routeToUpdate.startMarker && routeToUpdate.endMarker) {
      fetchRoute(routeToUpdate);
    }
  });

  return marker;
}

// Function to fetch route and update the polyline
function fetchRoute(route) {
  const startPoint = route.startMarker.getLatLng();
  const endPoint = route.endMarker.getLatLng();

  console.log("Fetching route for:", route);
  const apiKey = "5b3ce3597851110001cf6248019e60e78b254057a4a19879ff29e229";
  const url = `https://api.openrouteservice.org/v2/directions/foot-walking?api_key=${apiKey}&start=${startPoint.lng},${startPoint.lat}&end=${endPoint.lng},${endPoint.lat}`;

  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      const coordinates = data.features[0].geometry.coordinates.map((coord) => [
        coord[1],
        coord[0],
      ]);

      // Remove existing polyline if it exists
      if (route.polyline) {
        polylineLayer.removeLayer(route.polyline);
      }

      // Draw the new polyline
      route.polyline = L.polyline(coordinates, {
        color: "#ffd60a",
        weight: 6,
      }).addTo(polylineLayer);

      // Adjust map view to fit the new polyline
      map.fitBounds(route.polyline.getBounds());
    })
    .catch((error) => console.error("Error fetching route:", error));
}

// Function to search location using ORS API
function searchLocation() {
  const query = document.getElementById("search-box").value;
  const apiKey = "5b3ce3597851110001cf6248019e60e78b254057a4a19879ff29e229";
  const url = `https://api.openrouteservice.org/geocode/search?api_key=${apiKey}&text=${query}`;

  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      const coordinates = data.features[0].geometry.coordinates;
      const latLng = [coordinates[1], coordinates[0]]; // [latitude, longitude]
      addMarker(latLng, query);
    })
    .catch((error) => console.error("Error:", error));
}
