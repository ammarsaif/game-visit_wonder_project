
// Leaflet Library

let map = L.map('map').setView([0, 0], 1.5);  // Center of the world, zoom level

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

let markersData = [
    { coordinates: [60.3172, 24.963], tooltipContent: "Helsinki, Finland" },
    { coordinates: [37.971, 23.72], tooltipContent: "Parthenon, Greece" },
    { coordinates: [-27.12, -109.34], tooltipContent: "Easter Islands, Chile" },
    { coordinates: [26.007, 78.04], tooltipContent: "Taj Mahal, India" },
    { coordinates: [41.89, 12.49], tooltipContent: "Colosseum, Italy" },
    { coordinates: [13.41, 103.86], tooltipContent: "Angkor, Cambodia" },
    { coordinates: [19.68, -98.87], tooltipContent: "Teotihuacan, Mexico" },
    { coordinates: [20.93, -88.56], tooltipContent: "Chichen Itza, Mexico" },
    { coordinates: [-13.22, -72.49], tooltipContent: "Machu Picchu, Peru" },
    { coordinates: [30.32, 35.44], tooltipContent: "Petra, Jordan" },
    { coordinates: [40.43, 116.58], tooltipContent: "Great Wall of China" },
    { coordinates: [30.12, 31.40], tooltipContent: "Pyramids of Giza, Egypt" },
    { coordinates: [51.17, -1.82], tooltipContent: "Stonehenge, UK" },
    { coordinates: [41.261, 28.741], tooltipContent: "Hagia Sofia, Turkey" },
    { coordinates: [30.61, 72.89], tooltipContent: "Harappa, Pakistan" },
    { coordinates: [29.53, 52.89], tooltipContent: "Persepolis, Iran" },
    { coordinates: [37.888, -4.779], tooltipContent: "The Mezquita of Córdoba, Spain" },
];

// Loop through the marker data and create markers
for (let markerData of markersData) {
    let marker = L.marker(markerData.coordinates).addTo(map);
    marker.bindTooltip(markerData.tooltipContent).openTooltip();

    // Show popup on mouse hover
    marker.on('mouseover', function () {
        marker.openPopup();
    });

    // Close popup when mouse is not hovering
    marker.on('mouseout', function () {
        marker.closePopup();
    });
}


/*
let helsinki = L.marker([60.3172, 24.963]).addTo(map);
helsinki.bindPopup("<b>Default Location</b><br>Helsinki").openPopup();
helsinki.bindTooltip("Helsinki").openTooltip();

let parthenon = L.marker([37.971, 23.72]).addTo(map);
parthenon.bindPopup("<b>Parthenon</b><br>Greece").openPopup();
parthenon.bindTooltip("Parthenon").openTooltip();

let easterIsland = L.marker([-27.12, -109.34]).addTo(map);
easterIsland.bindPopup("<b>Easter Islands</b><br>Chile").openPopup();

let tajMahal = L.marker([26.007, 78.04]).addTo(map);
tajMahal.bindPopup("<b>Taj Mahal</b><br>India").openPopup();

let colosseum = L.marker([41.89, 12.49]).addTo(map);
colosseum.bindPopup("<b>Colosseum</b><br>Italy").openPopup();

let angkor = L.marker([13.41, 103.86]).addTo(map);
angkor.bindPopup("<b>Angkor</b><br>Cambodia").openPopup();

let teotihuacan = L.marker([19.68, -98.87]).addTo(map);
teotihuacan.bindPopup("<b>Teotihuacan</b><br>Mexico").openPopup();

let petra = L.marker([30.32, 35.44]).addTo(map);
petra.bindPopup("<b>Petra</b><br>Jordan").openPopup();

let machuPicchu = L.marker([-13.22, -72.49]).addTo(map);
machuPicchu.bindPopup("<b>Machu picchu</b><br>Mexico").openPopup();

let wallChina = L.marker([40.43, 116.58]).addTo(map);
wallChina.bindPopup("<b>Great wall of China</b><br>China").openPopup();

let pyramidsGiza = L.marker([30.12, 31.40]).addTo(map);
pyramidsGiza.bindPopup("<b>Pyramids of Giza</b><br>Egypt").openPopup();

let stonehenge = L.marker([51.17, -1.82]).addTo(map);
stonehenge.bindPopup("<b>Stonehenge</b><br>UK").openPopup();

let hagiaSophia = L.marker([41.261, 28.741]).addTo(map);
hagiaSophia.bindPopup("<b>Hagia Sophia</b><br>Turkiye").openPopup();

let chichenItza = L.marker([20.93, -88.56]).addTo(map);
chichenItza.bindPopup("<b>Chichen Itza</b><br>Mexico").openPopup();

let harappa = L.marker([30.61, 72.89]).addTo(map);
harappa.bindPopup("<b>Harappa</b><br>Pakistan").openPopup();

let persepolis = L.marker([29.53, 52.89]).addTo(map);
persepolis.bindPopup("<b>Persepolis</b><br>Iran").openPopup();

let cordoba = L.marker([37.888, -4.779]).addTo(map);
cordoba.bindPopup("<b>The Mezquita of Córdoba</b><br>Spain").openPopup();


let popup = L.popup();

function onMapClick(e) {
    popup
        .setLatLng(e.latlng)
        .setContent("You clicked the map at " + e.latlng.toString())
        .openOn(map);
}

map.on('click', onMapClick);
*/


// Form submit function
document.addEventListener('DOMContentLoaded', function () {
    const registerForm = document.querySelector('#registerPlayerForm');

    if (registerForm) {
        registerForm.addEventListener('submit', async function (event) {
            event.preventDefault();

            try {
                const formData = new FormData(this);
                const response = await fetch('/register_player', {
                    method: 'POST',
                    body: formData
                });

                if (response.ok) {
                    const result = await response.json();

                    // Log the result to the console
                    console.log('Server Response:', result);

                    if (result.status === 'success') {
                        console.log('Player registered successfully');
                    } else {
                        console.error('Player registration failed:', result.error);
                    }
                } else {
                    console.error('Failed to submit the form. HTTP status:', response.status);
                }
            } catch (error) {
                console.error('Error:', error);
            }
        });
    } else {
        console.error('Register form not found');
    }
});


/* Game Play Async Function */
document.addEventListener("DOMContentLoaded", function () {
    let destinationButtons = document.querySelectorAll(".btn-destination");

    destinationButtons.forEach(function (button) {
        button.addEventListener("click", function () {
            button.style.display = 'none';
            let selectedDestination = button.getAttribute("data-destination");

            if (selectedDestination) {
                // AJAX request to handle form submission
                fetch('/play_game', {
                    method: 'POST',
                    body: JSON.stringify({ 'data-destination': selectedDestination }),
                    headers: {
                        'Content-Type': 'application/json',
                    },
                })
                .then(response => response.json())
                .then(data => {
                    // Update the relevant elements with the new data
                    document.querySelector("#budget").textContent = data.co2_budget;
                    document.querySelector("#spent").textContent = data.total_co2_spent;
                    document.querySelector("#available").textContent = data.co2_available;
                    document.querySelector("#visited").textContent = data.num_visited_destinations;
                    document.querySelector("#target").textContent = data.game_win_threshold;
                    document.querySelector("#location").textContent = data.current_location_name;
                    document.querySelector("#distance").textContent = data.distance_in_kilometer;

                    // Check if the game is won or lost and show the modal
                    if (data.status === 'won' || data.status === 'lost') {
                        let message = data.status === 'won' ? 'Congratulations! You won!' : 'Sorry! You lost!';
                        showModal(message);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    // Handle the error, e.g., display an error message to the user
                });
            } else {
                console.error('Selected destination is not set.');
            }
        });
    });
});

function showModal(message) {
    var modal = document.getElementById("gameResultModal");
    var modalLabel = document.getElementById("gameResultModalLabel");

    modalLabel.textContent = message;
    modal.style.display = "block";
}

function closeModal() {
    var modal = document.getElementById("gameResultModal");
    modal.style.display = "none";
}

function playAgain() {
    // Your logic for restarting the game
    closeModal();

    // Clear session data related to the game
    fetch('/clear_session', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Redirect to the player_info route to start a new game
            window.location.href = '/player_info';
        } else {
            console.error('Error clearing session data.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        // Handle the error, e.g., display an error message to the user
    });
}

