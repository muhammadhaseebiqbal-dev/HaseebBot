let CHATS = document.getElementById("CHATS").innerHTML;
let imagediv_status = false

// sound effects
const send_msg_effect = new Audio()

// Session Identifier
const CurrentSessionId = Session_Idetifier(10)
console.log(CurrentSessionId);

$(document).ready(function () {
    $("#dataForm").submit(function (event) {
        event.preventDefault();

        document.getElementById('session_id').innerHTML = CurrentSessionId
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

        $("#CHATS").append(` <div class="msg sent">${$("#dataInput").val()}</div>`);
        
        if (isImage($("#dataInput").val())) {
            $("#CHATS").append(`<div class="AiImage" style="display:flex;justify-content:center;align-items:center;"><a href="" download blank><img src="../static/images/thinking.gif" style = "width:40px;height:40px"></a></div>`)
            imagediv_status = true
        }
        scrollToBottom()
        send_msg_effect.src = '../static/soundeffects/message-sent.mp3'
        send_msg_effect.play()

        textarea.style.height = 35 + "px"

        document.getElementById('dataInput').value = ""
        document.getElementsByClassName('initial_prompt_container')[0].style.display = "none"

        $.ajax({
            type: "POST",
            url: "/textModel", // Change this URL to match your Python server endpoint
            data: JSON.stringify(formData), // Convert data to JSON string
            contentType: "application/json",
            dataType: "json",
            encode: true,
        })
            .done(function (response) {
                if (response.jpeg) {
                    let base64Image
                    base64Image = response.jpeg;
                    document.getElementsByClassName('initial_prompt_container')[0].style.display = "none"
                    if (imagediv_status) {
                        imageplaceholder = document.querySelectorAll('.AiImage a img')  
                        imageplaceholder[imageplaceholder.length - 1].style.width = "100%"
                        imageplaceholder[imageplaceholder.length - 1].style.height = "310px"
                        imageplaceholder[imageplaceholder.length - 1].src = `data:image/jpeg;base64,${base64Image}`
                        imageplaceholder[imageplaceholder.length - 1].href = `data:image/jpeg;base64,${base64Image}`
                        imagediv_status = false
                    }
                    else{    
                        $("#CHATS").append(`<div class="AiImage"><a href="data:image/jpeg;base64,${base64Image}" download blank><img src="data:image/jpeg;base64,${base64Image}"></a></div>`)
                        imageplaceholder = document.querySelectorAll('.AiImage a img')  
                        imageplaceholder[imageplaceholder.length - 1].style.width = "100%"
                        imageplaceholder[imageplaceholder.length - 1].style.height = "310px"
                        imagediv_status = false
                    }
                    document.getElementById('submit').innerHTML = `<i class="fa-solid fa-arrow-up fa-xl" style="color: #fff;"></i>`
                    scrollToBottom()

                } 
                else {
                    if (response.promptid == CurrentSessionId) {
                        if (response.snippet_Validation == "empty") {
                            var data = response.message
                            data = data.replace(/\*\*(.*?)\*\*/g, "<br><strong>$1</strong>\n<br>");
                            formatedData = data.replace("*", "");
                            console.log("1",formatedData);

                            
                            $("#CHATS").append(` <div class="msg rcvd" background="#18222d"><div class="msg_tools"><div class="copy_text"><i class="fa-solid fa-copy"></i></div></div><p><code>${formatedData}</code></p></div>`);
                            send_msg_effect.src = '../static/soundeffects/message-sent.mp3'
                            
                            document.getElementById('submit').innerHTML = `<i class="fa-solid fa-arrow-up fa-xl" style="color: #fff;"></i>`
                            send_msg_effect.play()
                            scrollToBottom()
                            Copied()

                        } else {
                            var data = response.message
                            formatedData = (data.replace(/\*\*(.*?)\*\*/g, "<br><strong><h3>$1</h3></strong>\n<br>")).split("```");
                            console.log("2",formatedData);
                            
                            $("#CHATS").append(`
                                               <div class="msg rcvd"><div class="msg_tools"><span>Output</span><div class="copy_text"><i class="fa-solid fa-copy"></i></div></div><pre style="width:100%;overflow-x:auto;box-sizing:border-box;color:magenta;"><code class="language-java " style:"padding:7px;">${formatedData}</code></pre></div>
                                       `);
                            $("#CHATS").append(` <div class="msg rcvd" background="#18222d" style="padding:13px;"><div class="msg_tools"><div class="copy_text"><i class="fa-solid fa-copy"></i></div></div><p><code>${formatedData[2]}</code></p></div>`);

                            document.getElementById('dataInput').value = ""
                            send_msg_effect.src = '../static/soundeffects/message-sent.mp3'
                            send_msg_effect.play()

                            document.getElementById('submit').innerHTML = `<i class="fa-solid fa-arrow-up fa-xl" style="color: #fff;"></i>`
                            hljs.highlightAll();
                            scrollToBottom()
                            Copied()

                        }

                    }
                    else {
                        console.error("Logical Error on Client Side");
                    }

                }
            })
            .fail(function (error) {
                console.error(error);
            });

    });
});



