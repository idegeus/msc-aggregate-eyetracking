var mymap = L.map('mapid').setView([51.505, -0.09], 13);
var layerGroup = L.layerGroup().addTo(mymap);

L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
    maxZoom: 18,
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, ' +
        'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1
}).addTo(mymap);

function show_0(){
    list_segment_load("05-Jan-2021-12_14_18.json");
}
function show_1(){
    list_segment_load("06-Jan-2021-14_41_38.json");
}
function show_2(){
    list_segment_load("06-Jan-2021-14_46_43.json");
}
function show_3(){
    list_segment_load("06-Jan-2021-14_51_48.json");
}

function list_segment_load(path_file){
    var xhr = new XMLHttpRequest();
    xhr.overrideMimeType("application/json");
    xhr.open('GET', path_file, true); // Replace 'my_data' with the path to your file
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == "200") {
            show(JSON.parse(xhr.responseText).list_segment);
        }
    };
    xhr.send(null);  
}

function componentToHex(c) {
    var hex = c.toString(16);
    return hex.length == 1 ? "0" + hex : hex;
}

function rgbToHex(r, g, b) {
    return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
}

function show(list_segment){
    layerGroup.clearLayers();
    lat_min = list_segment[0].lat_start
    lat_max = list_segment[0].lat_start
    long_min = list_segment[0].long_start
    long_max = list_segment[0].long_start
    for (i = 0; i < list_segment.length; i++) {
        segment = list_segment[i]
        
        lat_min = Math.min(lat_min, segment.lat_end)
        lat_max = Math.max(lat_max, segment.lat_end)
        long_min = Math.min(long_min, segment.long_end)
        long_max = Math.max(long_max, segment.long_end)

        var polygon = L.polygon([
            [segment.lat_start, segment.long_start],
            [segment.lat_end, segment.long_end]
        ]).addTo(layerGroup);  
        color_hex = rgbToHex(segment.color_rgb[0], segment.color_rgb[1], segment.color_rgb[2])  
        polygon.setStyle({color: color_hex});

    }
    lat_view = (lat_max + lat_min) / 2
    long_view = (long_max + long_min) / 2
    mymap.setView([lat_view, long_view], 15);   
}