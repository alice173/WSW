document.addEventListener("DOMContentLoaded", function () {
  let elevationPoints = [];
  let currentRoute = null;
  let coords = [];
  const routeData = {
    id: "{{ route.id }}",
    startPoint: "{{ route.start_point }}",
    endPoint: "{{ route.end_point }}",
    distance: "{{ route.distance|default:'0'}}",
    elevation: "{{ route.elevation|default:'0' }}",
  };
  console.log("routeD" + routeData);

  // Initialize map
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
  const polylineLayer = L.layerGroup([]).addTo(map);

  // Function to parse coordinates from string format
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
      return null; // Return null if parsing fails
    }
    console.log("Parsed coordinates:", { lat, lng });
    return { lat, lng };
  }

  // Function to format coordinates for form input
  function formatCoordinates(latlng) {
    return `${latlng.lat.toFixed(6)}, ${latlng.lng.toFixed(6)}`;
  }

  // Function to initialize editing of existing route
  function initializeRouteEdit() {
    // Check if we have route data from Django
    if (typeof routeData !== "undefined") {
      const startCoords = parseCoordinates(routeData.startPoint);
      const endCoords = parseCoordinates(routeData.endPoint);

      if (startCoords && endCoords) {
        // Create markers for start and end points
        currentRoute = {
          startMarker: addMarker(startCoords, "Start Point"),
          endMarker: addMarker(endCoords, "End Point"),
          polyline: null,
        };

        // Fetch and draw the route
        fetchRoute(currentRoute);

        // Center map on route start point
        map.setView([startCoords.lat, startCoords.lng], 13);
      }
    }
  }

  // Function to update form fields
  function updateFormFields(startPoint, endPoint, distance, elevation) {
    // Update hidden distance and elevation fields
    const distanceInput = document.getElementById("id_distance");
    const elevationInput = document.getElementById("id_elevation");
    if (distanceInput) distanceInput.value = distance.toFixed(2);
    if (elevationInput) elevationInput.value = elevation.toFixed(2);

    // Update start and end point fields
    const startInput = document.getElementById("id_start_point");
    const endInput = document.getElementById("id_end_point");
    if (startInput && startPoint) {
      startInput.value = formatCoordinates(startPoint);
    }
    if (endInput && endPoint) {
      endInput.value = formatCoordinates(endPoint);
    }

    // Update display elements if they exist
    const distanceDisplay = document.querySelector("#distance span");
    const elevationDisplay = document.querySelector("#elevation span");
    if (distanceDisplay)
      distanceDisplay.innerText = `${distance.toFixed(2)} Miles`;
    if (elevationDisplay)
      elevationDisplay.innerText = `${elevation.toFixed(2)} ft`;
  }

  // FetchRoute function
  function fetchRoute(route) {
    const startPoint = route.startMarker.getLatLng();
    const endPoint = route.endMarker.getLatLng();

    const apiKey = "5b3ce3597851110001cf6248019e60e78b254057a4a19879ff29e229";
    const url = `https://api.openrouteservice.org/v2/directions/foot-walking?api_key=${apiKey}&start=${startPoint.lng},${startPoint.lat}&end=${endPoint.lng},${endPoint.lat}&elevation=true`;

    fetch(url)
      .then((response) => response.json())
      .then((data) => {
        const coordinates = data.features[0].geometry.coordinates.map(
          (coord) => [coord[1], coord[0]]
        );

        // Remove existing polyline if it exists
        if (route.polyline) {
          polylineLayer.removeLayer(route.polyline);
        }

        // Draw the new polyline
        route.polyline = L.polyline(coordinates, {
          color: "#48636a",
          weight: 6,
        }).addTo(polylineLayer);

        coords = coordinates;

        // Calculate distance in miles
        const distance = calculateDistance(coordinates);

        // Get elevation data
        getElevationData(coordinates, endPoint, distance, function (elevation) {
          // Update form fields with new values
          updateFormFields(startPoint, endPoint, distance, elevation);
        });

        // Adjust map view to fit the route
        map.fitBounds(route.polyline.getBounds());
      })
      .catch((error) => {
        console.error("Error fetching route:", error);
        alert("Error fetching route. Please try again.");
      });
  }

  // Calculate distance function
  function calculateDistance(coordinates) {
    let totalDistance = 0;
    for (let i = 1; i < coordinates.length; i++) {
      const point1 = L.latLng(coordinates[i - 1][0], coordinates[i - 1][1]);
      const point2 = L.latLng(coordinates[i][0], coordinates[i][1]);
      totalDistance += point1.distanceTo(point2);
    }
    // Convert meters to miles
    return totalDistance / 1609.34;
  }

  // Modified getElevationData function
  function getElevationData(coordinates, endPoint, distance, callback) {
    const apiKey = "5b3ce3597851110001cf6248019e60e78b254057a4a19879ff29e229";
    const url = `https://api.openrouteservice.org/elevation/line?api_key=${apiKey}`;
    const body = {
      format_in: "geojson",
      format_out: "geojson",
      geometry: {
        coordinates: coordinates.map((coord) => [coord[1], coord[0]]),
        type: "LineString",
      },
    };

    fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.geometry && data.geometry.coordinates) {
          const elevationData = data.geometry.coordinates.map(
            (coord) => coord[2]
          );
          const elevationGain =
            Math.max(...elevationData) - Math.min(...elevationData);
          const elevationGainFeet = elevationGain * 3.28084;

          if (callback) {
            callback(elevationGainFeet);
          }
        }
      })
      .catch((error) => console.error("Error fetching elevation data:", error));
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

  let savedRoutePolylines = new Map(); // Store polylines for saved routes

  // Function to load and display a saved route
  function loadSavedRoute(routeData) {
    console.log("Loading route:", routeData); // Log the route data being loaded
    const startCoords = parseCoordinates(routeData.startPoint);
    const endCoords = parseCoordinates(routeData.endPoint);

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
      return; // Skip this route
    }

    console.log("Valid coordinates:", startCoords, endCoords); // Log valid coordinates

    const apiKey = "5b3ce3597851110001cf6248019e60e78b254057a4a19879ff29e229";
    const url = `https://api.openrouteservice.org/v2/directions/foot-walking?api_key=${apiKey}&start=${startCoords.lng},${startCoords.lat}&end=${endCoords.lng},${endCoords.lat}`;

    fetch(url)
      .then((response) => response.json())
      .then((data) => {
        const coordinates = data.features[0].geometry.coordinates.map(
          (coord) => [coord[1], coord[0]]
        );

        console.log("Coordinates for route:", coordinates); // Log the coordinates

        // Create polyline with a different color for saved routes
        const polyline = L.polyline(coordinates, {
          color: "#ffd60a", // Different color for saved routes
          weight: 3,
          opacity: 0.7,
        }).addTo(polylineLayer);

        console.log("Polyline added to layer:", polyline); // Log the polyline

        // Store the polyline reference
        savedRoutePolylines.set(routeData.id, polyline);

        // Adjust map view to fit the route
        map.fitBounds(polyline.getBounds());
      })
      .catch((error) => console.error("Error loading saved route:", error));
  }

  // Function to load all saved routes
  function loadAllSavedRoutes() {
    if (typeof allRoutes !== "undefined") {
      allRoutes.forEach((route) => {
        if (route.id !== currentRouteId) {
          // Don't double-draw the route being edited
          loadSavedRoute(route);
        }
      });
    }
  }

  // Function to clear all saved routes from the map
  function clearSavedRoutes() {
    savedRoutePolylines.forEach((polyline) => {
      polylineLayer.removeLayer(polyline);
    });
    savedRoutePolylines.clear();
  }

  // Modified toggle button event listener
  document
    .getElementById("toggle-polylines")
    .addEventListener("click", function () {
      if (map.hasLayer(polylineLayer)) {
        map.removeLayer(polylineLayer);
        map.off("click", onMapClick);
        clearSavedRoutes();
      } else {
        console.log("Adding polyline layer to map");
        map.addLayer(polylineLayer);
        map.on("click", onMapClick);
        loadAllSavedRoutes();

        // If we're editing a route, redraw it
        if (currentRoute?.polyline) {
          currentRoute.polyline.addTo(polylineLayer);
        }
      }
    });

  // Get the current route ID if we're editing
  const currentRouteId = typeof routeData !== "undefined" ? routeData.id : null;

  // Modified initializeRouteEdit function
  function initializeRouteEdit() {
    if (typeof routeData !== "undefined") {
      const startCoords = parseCoordinates(routeData.startPoint);
      const endCoords = parseCoordinates(routeData.endPoint);

      if (startCoords && endCoords) {
        currentRoute = {
          startMarker: addMarker(startCoords, "Start Point"),
          endMarker: addMarker(endCoords, "End Point"),
          polyline: null,
        };

        fetchRoute(currentRoute);

        // Load all other saved routes
        loadAllSavedRoutes();
      }
    }
  }

  // Map click handler
  function onMapClick(e) {
    const coordinates = e.latlng;

    if (!currentRoute) {
      currentRoute = {
        startMarker: addMarker(coordinates, "Start Point"),
        endMarker: null,
        polyline: null,
      };
      coords = [coordinates];
    } else if (!currentRoute.endMarker) {
      currentRoute.endMarker = addMarker(coordinates, "End Point");
      coords.push(coordinates);
      fetchRoute(currentRoute);
    }
  }

  // Initialize the map for editing if we have route data
  initializeRouteEdit();

  // Add map click handler
  map.on("click", onMapClick);

  loadAllSavedRoutes();
});
