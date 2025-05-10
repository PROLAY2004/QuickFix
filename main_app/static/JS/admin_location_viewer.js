function initMap() {
  // Get coordinates from hidden inputs
  const lat = parseFloat(document.getElementById('latitude').value) || 22.5726; // Default to Kolkata
  const lng = parseFloat(document.getElementById('longitude').value) || 88.3639;
  
  // Create map
  const map = new google.maps.Map(document.getElementById('map'), {
    center: { lat, lng },
    zoom: 15,
    mapTypeControl: true,
    streetViewControl: true
  });

  // Add marker
  new google.maps.Marker({
    position: { lat, lng },
    map: map,
    title: 'Location'
  });
}

// Fallback in case callback fails
if (typeof google !== 'undefined' && google.maps) {
  initMap();
} else {
  window.initMap = initMap;
}