function geolocation_validtain(){
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(client_location_lon_lat)
        console.log("valid");
    }
    else
    {
        alert("Location plugin is not supported on this devices")
    }
}
function client_location_lon_lat(position) {
    console.log("latitude,longitude");
    var latitude = position.coords.latitude
    var longitude = position.coords.longitude
    getweather(longitude,latitude)
}
async function getweather(lon,lat) {
    weather_request = await fetch(`https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=f39852f5c9a18c25e7470fa77f1523a5`)
    response_parsing = await weather_request.json()
    console.log(JSON.stringify(response_parsing));
    var data_to_pass = {
        "response_parsing" : response_parsing,
        "SessionId" : CurrentSessionId
    }
    $.ajax({
        type: "POST",
        url: "/weatherdata", // Change this URL to match your Python server endpoint
        data: JSON.stringify(data_to_pass), // Convert data to JSON string
        contentType: "application/json",
        dataType: "json",
        encode: true,
    }).done(function(response){
        console.log(response);
    })
    .fail(function(error){
        console.log(error);
    })
   
    
}