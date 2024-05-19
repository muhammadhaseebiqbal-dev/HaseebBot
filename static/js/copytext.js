function Copied() {
    const copy_icon = document.querySelectorAll('.copy_text')
    var text_to_copy_parent_elem = document.querySelectorAll('code')
    copy_icon.forEach(function (icon,i) {
        icon.addEventListener('click',()=>{
           var content = text_to_copy_parent_elem[i]
           var temp_textarea_element = document.createElement('textarea')
            temp_textarea_element.value = content.innerText
            document.body.appendChild(temp_textarea_element);
            temp_textarea_element.select()
            document.execCommand('copy')
            document.body.removeChild(temp_textarea_element)
            console.log("Copied!");
        })
    })
    
}