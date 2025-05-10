let map;
let marker;
let geocoder;

document.addEventListener("DOMContentLoaded", () => {
    const detectBtn = document.getElementById("detect-location");

    const lat = parseFloat(document.getElementById("latitude").value) || 22.5726;
    const lng = parseFloat(document.getElementById("longitude").value) || 88.3639;

    const initialLatLng = { lat: lat, lng: lng };
    handleLocation(initialLatLng.lat, initialLatLng.lng);

    detectBtn.addEventListener("click", () => {
        detectLocation();
    });
});

function detectLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const { latitude, longitude } = position.coords;
                handleLocation(latitude, longitude);
            },
            (error) => {
                alert("Location access denied or unavailable. Try again.");
            }
        );
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

function handleLocation(lat, lng) {
    const latlng = { lat, lng };
    updateLatLngFields(lat, lng);
    initMap(latlng);
    reverseGeocode(latlng); // <-- fill the other fields
}

function initMap(latlng) {
    if (!map) {
        map = new google.maps.Map(document.getElementById("map"), {
            center: latlng,
            zoom: 15,
        });
        geocoder = new google.maps.Geocoder();
    } else {
        map.setCenter(latlng);
    }

    if (!marker) {
        marker = new google.maps.Marker({
            position: latlng,
            map: map,
            draggable: true,
        });

        marker.addListener("dragend", () => {
            const newPos = marker.getPosition();
            const lat = newPos.lat();
            const lng = newPos.lng();
            updateLatLngFields(lat, lng);
            reverseGeocode({ lat, lng }); // <-- also reverse geocode on drag
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
    if (!geocoder) geocoder = new google.maps.Geocoder();

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

