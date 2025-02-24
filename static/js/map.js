document.addEventListener("DOMContentLoaded", function () {
  console.log("hello");
  let elevationPoints = [];
  let currentRoute = null;
  let coords = [];

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

  // Utility functions (parse coordinates, format coordinates, etc.)
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

  // Update form fields
  function updateFormFields(startPoint, endPoint, distance, elevation) {
    const distanceInput = document.getElementById("id_distance");
    const elevationInput = document.getElementById("id_elevation");
    if (distanceInput) distanceInput.value = distance.toFixed(2);
    if (elevationInput) elevationInput.value = elevation.toFixed(2);

    const startInput = document.getElementById("id_start_point");
    const endInput = document.getElementById("id_end_point");

    if (startInput && startPoint) {
      startInput.value = formatCoordinates(startPoint);
    }
    if (endInput && endPoint) {
      endInput.value = formatCoordinates(endPoint);
    }

    const distanceDisplay = document.querySelector("#distance span");
    const elevationDisplay = document.querySelector("#elevation span");
    if (distanceDisplay)
      distanceDisplay.innerText = `${distance.toFixed(2)} Miles`;
    if (elevationDisplay)
      elevationDisplay.innerText = `${elevation.toFixed(2)} ft`;
  }

  // Fetch route details
  function fetchRoute(route) {
    const startPoint = route.startMarker.getLatLng();
    const endPoint = route.endMarker.getLatLng();

    console.log("Fetching route for points:", startPoint, endPoint); // Debug log

    const apiKey = "5b3ce3597851110001cf6248019e60e78b254057a4a19879ff29e229";
    const url = `https://api.openrouteservice.org/v2/directions/foot-walking?api_key=${apiKey}&start=${startPoint.lng},${startPoint.lat}&end=${endPoint.lng},${endPoint.lat}&elevation=true`;

    fetch(url)
      .then((response) => {
        console.log("API Response:", response); // Debug log
        return response.json();
      })
      .then((data) => {
        console.log("Route data:", data); // Debug log

        const coordinates = data.features[0].geometry.coordinates.map(
          (coord) => [coord[1], coord[0]]
        );

        if (route.polyline) {
          polylineLayer.removeLayer(route.polyline);
        }

        route.polyline = L.polyline(coordinates, {
          color: "#48636a",
          weight: 6,
        }).addTo(polylineLayer);

        coords = coordinates;

        const distance = calculateDistance(coordinates);

        getElevationData(coordinates, endPoint, distance, function (elevation) {
          updateFormFields(startPoint, endPoint, distance, elevation);
        });

        map.fitBounds(route.polyline.getBounds());
      })
      .catch((error) => {
        console.error("Error fetching route:", error);
        alert("Error fetching route. Please try again.");
      });
  }

  // Distance calculation
  function calculateDistance(coordinates) {
    let totalDistance = 0;
    for (let i = 1; i < coordinates.length; i++) {
      const point1 = L.latLng(coordinates[i - 1][0], coordinates[i - 1][1]);
      const point2 = L.latLng(coordinates[i][0], coordinates[i][1]);
      totalDistance += point1.distanceTo(point2);
    }
    return totalDistance / 1609.34;
  }

  // Elevation data retrieval
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

  // Add map click handler
  map.on("click", onMapClick);

  ["id_start_point", "id_end_point"].forEach((inputId) => {
    const input = document.getElementById(inputId);
    if (input) {
      const geocoder = L.Control.Geocoder.nominatim({
        geocodingQueryParams: {
          limit: 5, // Number of suggestions
          countrycodes: "gb",
          viewbox: "-6.4,49.96,0.35,51.4", // Southwest England bounding box
          bounded: 1,
        },
      });

      input.addEventListener("input", function () {
        const placeName = this.value;
        if (placeName.length > 2) {
          // Minimum characters to trigger suggestions
          geocoder.geocode(placeName, (results) => {
            // Clear previous suggestions
            const existingSuggestions = document.getElementById(
              "location-suggestions"
            );
            if (existingSuggestions) {
              existingSuggestions.remove();
            }

            // Create suggestions dropdown
            const suggestionContainer = document.createElement("div");
            suggestionContainer.id = "location-suggestions";

            suggestionContainer.style.maxWidth = `${input.offsetWidth}px`;

            results.forEach((result) => {
              const suggestionItem = document.createElement("div");
              suggestionItem.className = "location-suggestions--item";
              suggestionItem.textContent = result.name;
              suggestionItem.style.padding = "10px";
              suggestionItem.style.cursor = "pointer";
              suggestionItem.addEventListener("mouseover", () => {
                suggestionItem.style.backgroundColor = "var(--primary-200)";
              });
              suggestionItem.addEventListener("mouseout", () => {
                suggestionItem.style.backgroundColor = "var(--secondary-200)";
              });
              suggestionItem.addEventListener("click", () => {
                const coordinates = `${result.center.lat}, ${result.center.lng}`;
                input.value = coordinates;
                suggestionContainer.remove();

                // Trigger geocoding and marker placement
                const marker = addMarker(
                  [result.center.lat, result.center.lng],
                  result.name
                );

                if (inputId === "id_start_point") {
                  if (currentRoute && currentRoute.startMarker) {
                    map.removeLayer(currentRoute.startMarker);
                  }
                  currentRoute = {
                    startMarker: marker,
                    endMarker: currentRoute?.endMarker || null,
                    polyline: currentRoute?.polyline || null,
                  };
                } else {
                  if (currentRoute && currentRoute.endMarker) {
                    map.removeLayer(currentRoute.endMarker);
                  }
                  currentRoute = {
                    startMarker: currentRoute?.startMarker || null,
                    endMarker: marker,
                    polyline: currentRoute?.polyline || null,
                  };
                }

                if (currentRoute.startMarker && currentRoute.endMarker) {
                  fetchRoute(currentRoute);
                }
              });
              suggestionContainer.appendChild(suggestionItem);
            });

            // Position the suggestions near the input
            suggestionContainer.style.top = `${
              input.offsetTop + input.offsetHeight
            }px`;
            suggestionContainer.style.left = `${input.offsetLeft}px`;
            input.parentNode.appendChild(suggestionContainer);
          });
        }
      });
    }
  });

  initializeRouteEdit();

  // Allow search via input
  geocoder.on("markgeocode", function (e) {
    const { center, name } = e.geocode;
    const coordinates = { lat: center.lat, lng: center.lng };

    // If no current route, create start marker
    if (!currentRoute) {
      currentRoute = {
        startMarker: addMarker(coordinates, name),
        endMarker: null,
        polyline: null,
      };

      // Update start point input
      const startInput = document.getElementById("id_start_point");
      if (startInput) startInput.value = formatCoordinates(coordinates);
    }
    // If start exists but no end, create end marker
    else if (!currentRoute.endMarker) {
      currentRoute.endMarker = addMarker(coordinates, name);
      fetchRoute(currentRoute);

      // Update end point input
      const endInput = document.getElementById("id_end_point");
      if (endInput) endInput.value = formatCoordinates(coordinates);
    }
  });

  // Initialize route editing

  function initializeRouteEdit() {
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
});
