// https://codepen.io/sebastienfi/pen/pqNxEa
// <!DOCTYPE html>
// <html>
// <body>

// <p id="demo">Click the button to get your coordinates:</p>

// <button onclick="getLocation()">Try It</button>

// <script>
var x = document.getElementById("demo");

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            // Success function
            showPosition, 
            // Error function
            null, 
            // Options. See MDN for details.
            {
               enableHighAccuracy: true,
               timeout: 5000,
               maximumAge: 0
            });
    } else { 
        x.innerHTML = "Geolocation is not supported by this browser.";
    }
}

function showPosition(position) {
    x.innerHTML="Latitude: " + position.coords.latitude + 
    "<br>Longitude: " + position.coords.longitude;  
}
// </script>

// </body>
// </html>