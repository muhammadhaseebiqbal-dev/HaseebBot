const drawer = document.getElementById("DRAWER");
const drawer_btn = document.getElementById("SVG_DRAWER");
const close_btn = document.getElementById("CLOSE");
const reloadchats_btn = document.getElementById("RELOADCHATS");
var drawer_status = "disabled";
drawer_btn.addEventListener("click", () => {
    navigator.vibrate("50")
    drawer.style.translate = "99%";
    drawer_status = "enabled"
});
close_btn.addEventListener("click", () => {
    if (drawer_status == "enabled") {
        navigator.vibrate("50")
        drawer.style.translate = "0%";
        console.log("ok");
    }
})
reloadchats_btn.addEventListener("click", () => {
    location.reload()
})