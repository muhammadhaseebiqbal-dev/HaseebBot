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