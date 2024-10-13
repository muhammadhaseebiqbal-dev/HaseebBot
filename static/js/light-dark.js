const sun_icon = document.querySelector('.light-dark-mode')
let mode_status = false;

sun_icon.addEventListener("click", () => {
    if (!mode_status) {
        document.documentElement.style.setProperty('--_drawer_bg', '#ebebeb');
        document.documentElement.style.setProperty('--_chatarea_bg', '#fff');
        document.documentElement.style.setProperty('--_drawerChildBg', '#000000');
        document.documentElement.style.setProperty('--_drawerChildtxtcolor', '#fff');
        document.documentElement.style.setProperty('--_textarea_txtcolor', '#000000');
        mode_status = true
    }
    else
    {
        document.documentElement.style.setProperty('--_drawer_bg', '#272727');
        document.documentElement.style.setProperty('--_chatarea_bg', '#514f4f');
        document.documentElement.style.setProperty('--_drawerChildBg', '#fff');
        document.documentElement.style.setProperty('--_drawerChildtxtcolor', '#000000');
        document.documentElement.style.setProperty('--_textarea_txtcolor', '#fff');
        mode_status = false
    }
});
