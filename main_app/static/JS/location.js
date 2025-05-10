let map;
let marker;

document.addEventListener("DOMContentLoaded", () => {
    const detectBtn = document.getElementById("detect-location");

    // Detect location on page load
    detectLocation();

    // Detect on button click
    detectBtn.addEventListener("click", () => {
        detectLocation(true);
    });
});

function detectLocation(forceUserAction = false) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const { latitude, longitude } = position.coords;
                handleLocation(latitude, longitude);
            },
            (error) => {
                console.warn("Geolocation denied or unavailable, using default.");
                handleLocation(19.0760, 72.8777, true); // Mumbai
            }
        );
    } else {
        alert("Geolocation is not supported by this browser.");
        handleLocation(19.0760, 72.8777, true); // Mumbai
    }
}

function handleLocation(lat, lng, isDefault = false) {
    const latlng = { lat, lng };

    // Update hidden inputs
    updateLatLngFields(lat, lng);

    // Initialize or update map
    initMap(latlng);

    // Reverse geocoding if it's not the default
    if (!isDefault) reverseGeocode(latlng);
}

function initMap(latlng) {
    // First time only
    if (!map) {
        map = new google.maps.Map(document.getElementById("map"), {
            center: latlng,
            zoom: 15,
        });
    } else {
        map.setCenter(latlng);
    }

    // Create or move marker
    if (!marker) {
        marker = new google.maps.Marker({
            position: latlng,
            map: map,
            draggable: true, // Let user drag the pin
        });

        // Update fields on marker drag
        marker.addListener("dragend", () => {
            const newPos = marker.getPosition();
            const lat = newPos.lat();
            const lng = newPos.lng();
            updateLatLngFields(lat, lng);
            reverseGeocode({ lat, lng });
        });

    } else {
        marker.setPosition(latlng);
    }
}

function updateLatLngFields(lat, lng) {
    document.getElementById("latitude").value = lat;
    document.getElementById("longitude").value = lng;
}

function reverseGeocode(latlng) {
    const geocoder = new google.maps.Geocoder();
    geocoder.geocode({ location: latlng }, (results, status) => {
        if (status === "OK" && results[0]) {
            const components = results[0].address_components;

            let street = "", city = "", state = "", zip = "", country = "";

            components.forEach(component => {
                const types = component.types;
                if (types.includes("route")) street = component.long_name;
                if (types.includes("locality")) city = component.long_name;
                if (types.includes("administrative_area_level_1")) state = component.long_name;
                if (types.includes("postal_code")) zip = component.long_name;
                if (types.includes("country")) country = component.long_name;
            });

            document.getElementById("street").value = street;
            document.getElementById("city").value = city;
            document.getElementById("state").value = state;
            document.getElementById("zip_code").value = zip;
            document.getElementById("country").value = country;
        }
    });
}
