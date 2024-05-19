// Session identifier & id
function Session_Idetifier(length) {
    const libNum = "1234567890"
    const libChar = "QWERTYUIOPASDFGHJKLZXCVBNM"
    let result = ''
    for (let i = 0; i < (length-4); i++) {
        result += Math.floor(Math.random()*libNum.length)
    }
    for (let j = 0; j < 4; j++) {
        result += libChar[Math.floor(Math.random()*libNum.length)]
    }
    a = result.split('')
    for (let k = 0; k < result.length; k++) {
        a[k] = result[Math.floor(Math.random()*a.length)]
    }  
    return a.join('')
}