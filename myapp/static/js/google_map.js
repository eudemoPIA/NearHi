function initAutocomplete() {
    // Ensure google object is available
    if (typeof google !== 'undefined' && google.maps && google.maps.places) {
        const locationInputs = document.getElementsByClassName('location-input');

        Array.from(locationInputs).forEach((locationInput) => {
            const type = locationInput.getAttribute('data-autocomplete-type');
            const options = {
                types: type === 'city' ? ['(cities)'] : ['geocode'],
            };

            const autocomplete = new google.maps.places.Autocomplete(locationInput, options);

            if (type === 'detailed') {
                locationInput.addEventListener('input', function () {
                    // Allow manual input for detailed addresses
                });
            }

            autocomplete.addListener('place_changed', function() {
                const place = autocomplete.getPlace();

                if (!place.geometry) {
                    console.error("Could not retrieve a valid address: '" + locationInput.value + "'");
                    return;
                }

                console.log("Selected address:", place.formatted_address);
                console.log("Coordinates:", place.geometry.location.lat(), place.geometry.location.lng());
            });
        });
    } else {
        console.error("Google Maps API not loaded");
    }
}
