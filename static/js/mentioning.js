mentionImgAi = setInterval(() => {
    if ((document.getElementById('dataInput').value) === '@') {
        document.getElementById('dataInput').value = '@ImgAi '
    }

}, 100);