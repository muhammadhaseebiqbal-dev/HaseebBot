// Main plugin container
const plugins_toggler_main = document.getElementById('togglerball')
const plugins_main_container = document.getElementById('plugins')
var plugins_status = "disabled"
plugins_toggler_main.style.transition = ".6s"
plugins_toggler_main.addEventListener("click", () => {
    if (plugins_status == "disabled") {
        navigator.vibrate("50")
        plugins_toggler_main.style.transform = "translateX(120%)"
        plugins_main_container.style.filter = "none"
        weather_toggle_func()
        plugins_status = "enabled"
    }
    else {
        navigator.vibrate("50")
        plugins_toggler_main.style.transform = "translateX(0%)"
        plugins_main_container.style.filter = "grayscale(100)"
        plugins_status = "disabled"
    }

})

// Sub plugins
function weather_toggle_func() {
    const weather_switch_wrapper = document.getElementById('weathertogglers')
    const weather_switch_div = document.getElementById('weather_plugin')
    const weather_switch_ball = document.getElementById('w-togglerball')
    var w_switch_stat = "disbaled"
    weather_switch_wrapper.addEventListener("click", () => {
        if (w_switch_stat == "disabled") {
            console.log("1"+w_switch_stat);
            weather_switch_ball.style.transform = "translateX(85%)"
            weather_switch_ball.style.background = "#7cbbd5"
            navigator.vibrate("40")
            geolocation_validtain()
            w_switch_stat = "enabled"
        }
        else {
            console.log(w_switch_stat);
            weather_switch_ball.style.transform = "translateX(0%)"
            weather_switch_ball.style.background = "#fff"
            navigator.vibrate("40")
            w_switch_stat = "disabled"
            $.ajax({
                type: "POST",
                url: "/forgetweatherdata",
                data: JSON.stringify(CurrentSessionId), // Change this URL to match your Python server endpoint
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
    })
}