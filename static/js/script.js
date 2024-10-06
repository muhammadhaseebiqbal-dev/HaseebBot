let CHATS = document.getElementById("CHATS").innerHTML;
function generateRandomString(length) {
    const characters = "0123456789"; // String containing digits
    let result = "";
    for (let i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * characters.length));
    }
    return result;
}
const send_msg_effect = new Audio()

// Session Identifier
const CurrentSessionId = Session_Idetifier(10)
console.log(CurrentSessionId);

$(document).ready(function () {
    $("#dataForm").submit(function (event) {
        event.preventDefault();
        var prompt_id_js = generateRandomString(5);
        console.log("rand:" + prompt_id_js);
        document.getElementById('session_id').innerHTML = "Session : " + prompt_id_js
 if (Boolean((document.getElementById('dataInput').value).match('@')) === false) {
           document.getElementById('submit').innerHTML = `<i class="fa-solid fa-spinner fa-spin-pulse" style="color: #fff;"></i>`
           var formData = {
               query: $("#dataInput").val(),
               SessionId: CurrentSessionId
           };
           $.getJSON("https://api.ipify.org?format=json",
               function (data) {
                   // Displayin IP address on screen
                   $("#User_ip").html(data.ip);
               })
           $("#CHATS").append(`
                 <div class="msg sent">${$("#dataInput").val()}</div>
               `);
           send_msg_effect.src = '../static/soundeffects/message-sent.mp3'
           send_msg_effect.play()
           textarea.style.height = 35 + "px"
           document.getElementById('dataInput').value = ""
           document.getElementsByClassName('initial_prompt_container')[0].style.display = "none"
           
           $.ajax({
               type: "POST",
               url: "/server", // Change this URL to match your Python server endpoint
               data: JSON.stringify(formData), // Convert data to JSON string
               contentType: "application/json",
               dataType: "json",
               encode: true,
           })
               .done(function (response) {
                   console.log(response.prompt_id);
                   document.getElementById('submit').innerHTML = `<i class="fa-solid fa-arrow-up fa-xl" style="color: #fff;"></i>`
                   if (response.promptid == CurrentSessionId) {
                       if (response.snippet_Validation == "empty") {
                           var frmt = response.message
                           frmt = frmt.replace(/\*\*(.*?)\*\*/g, "<br><strong>$1</strong>\n<br>");
                           frmt2 = frmt.replace("*", "");
                           $("#CHATS").append(` <div class="msg rcvd" background="#18222d"><div class="msg_tools"><div class="copy_text"><i class="fa-solid fa-copy"></i></div></div><p><code>${frmt2}</code></p></div>`);
                           send_msg_effect.src = '../static/soundeffects/message-sent.mp3'
                           send_msg_effect.play()
                           scrollToBottom()
                           Copied()
   
                       } else {
                           var frmt = response.message
                           formating_pase = (frmt.replace(/\*\*(.*?)\*\*/g, "<br><strong><h3>$1</h3></strong>\n<br>")).split("```");
                           $("#CHATS").append(`
                                           <div class="msg rcvd"><div class="msg_tools"><span>Output</span><div class="copy_text"><i class="fa-solid fa-copy"></i></div></div><pre style="width:100%;overflow-x:auto;box-sizing:border-box;color:magenta;"><code class="language-java " style:"padding:7px;">${formating_pase[1]}</code></pre></div>
                                   `);
                           $("#CHATS").append(` <div class="msg rcvd" background="#18222d" style="padiing:13px;"><div class="msg_tools"><div class="copy_text"><i class="fa-solid fa-copy"></i></div></div><p><code>${formating_pase[2]}</code></p></div>`);

                           document.getElementById('dataInput').value = ""
                           send_msg_effect.src = '../static/soundeffects/message-sent.mp3'
                           send_msg_effect.play()
                           hljs.highlightAll();
                           scrollToBottom()
                           Copied()
   
                       }
                       console.log(response);
                       // Handle response from server
   
                   }
                   else {
                       console.log(response.prompt_id);
                   }
               })
               .fail(function (error) {
                   console.error(error);
               });
            } 
    else {
     document.getElementById('submit').innerHTML = `<i class="fa-solid fa-spinner fa-spin-pulse" style="color: #fff;"></i>`
    var formData = {
        query: $("#dataInput").val(),
        SessionId: CurrentSessionId
    };
    $.ajax({
        type: "POST",
        url: "/genimg",
        data: JSON.stringify(formData),
        contentType: "application/json",
        dataType: "json",
        encode: true,
    })
    .done(function (response) {
        let warning
        let base64Image
        if (response.jpeg) {
            base64Image = response.jpeg;
            document.getElementsByClassName('initial_prompt_container')[0].style.display = "none"
            $("#CHATS").append(`<div class="AiImage"><a href="data:image/jpeg;base64,${base64Image}" download blank><img src="data:image/jpeg;base64,${base64Image}"></a></div>`)
            // document.getElementById('CHATS') += `<div class="AiImage"><img src="data:image/jpeg;base64,${base64Image}"></div>`
            document.getElementById('submit').innerHTML = `<i class="fa-solid fa-arrow-up fa-xl" style="color: #fff;"></i>`
            document.getElementById('dataInput').value = "@ImgAi :"
            scrollToBottom()
        } else {
            const warningBox = document.querySelector('.warning')
            warning = response.warning
            warningBox.textContent = warning
            warningBox.classList.add('warn-anim')
            document.getElementById('dataInput').value = "@ImgAi "

        }

    })
    .fail(function (error) {
        
    })
 }
    });
});
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


const textarea = document.querySelector('textarea')
textarea.addEventListener('input', autoResize, false);

function autoResize() {
    this.style.height = 'auto';
    this.style.height = this.scrollHeight + 'px';
}
// initial prompt logic that insert specific value in textare
const init_prompt = document.querySelectorAll('.initialprompt')
var init_prompt_values = {
    "0": "Who is you Developer or Programmer. Give me Some Details. also use emojis to greet your programmer.",
    "1": "Create A TimeTable For Me to complete 14 chatpter in a week also add some Resting hours.",
    "2": "Can you summerize Article: \n \"https://www.techtarget.com/whatis/definition/ChatGPT\"",
    "3": "Tell me Some Teen Jokes",
    "4": "Give Me Proper Diet Plan For a Week \n Age: 18 years Old \n Height: 5ft. 6inch. \n Weight: 120kg \n Purpose: To loose weight up to 50kg",
    "5": "Create a flappy bird Logic : \n lang: \"javascript\" ",
}
init_prompt.forEach(function (ini_propmt_elem, i) {
    ini_propmt_elem.addEventListener("click", () => {
        textarea.value = init_prompt_values[i]
    })
})