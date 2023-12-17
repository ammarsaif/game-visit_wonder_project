
// Leaflet Library

let map = L.map('map').setView([0, 0], 1.5);  // Center of the world, zoom level

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

let helsinki = L.marker([60.3172, 24.963]).addTo(map);
helsinki.bindPopup("<b>Default Location</b><br>Helsinki").openPopup();

let parthenon = L.marker([37.971, 23.72]).addTo(map);
parthenon.bindPopup("<b>Parthenon</b><br>Greece").openPopup();

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



function updateGameData(play_game) {
    document.getElementById('num-target-wonders').textContent = play_game.difficulty;
    document.getElementById('num-visited-wonders').textContent = play_game.num_visited_destinations;
    document.getElementById('co2-budget').textContent = play_game.difficulty;
    document.getElementById('co2-spent').textContent = play_game.co2_calculated;
    document.getElementById('co2-available').textContent = play_game.co2_available;
    document.getElementById('current-destination').textContent = play_game.current_destination_name;
}

document.addEventListener('DOMContentLoaded', function () {
    let selectedDestination;  // Declare selectedDestination in a broader scope

    const buttons = document.querySelectorAll('.destination-btn');

    buttons.forEach(button => {
        button.addEventListener('click', function () {
            selectedDestination = this.getAttribute('data-destination');

            // Send the selected destination to the server using AJAX
            fetch('/play_game', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `selected_destination=${selectedDestination}`,
            })
            .then(response => response.text())
            .then(data => {
                console.log(data);  // Handle the server response
                // Assuming the server response contains game data, update the UI
                updateGameData(JSON.parse(data));
            })
            .catch(error => console.error('Error:', error));
        }); // <- Add this closing brace
    });
});


// click event on play again button

/*let playButton = document.querySelector(".btn-play_game")*/

/*
playButton.addEventListener('click', function () {
    alert('Play Again button has been clicked');
});


/*
// You can use selectedDestination elsewhere in your code
fetch('/play_game', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: `selected_destination=${selectedDestination}`,
})
.then(response => response.text())
.then(data => {
    console.log(data);  // Handle the server response
    // Assuming the server response contains game data, update the UI
    updateGameData(JSON.parse(data));
})
.catch(error => console.error('Error:', error));
});


*/