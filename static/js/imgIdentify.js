const similar_word = [
    "pic",    
    "pics",
    "pict",
    "pictu",
    "pictur",
    "picture",
    "pictures",
    "img",
    "imge",
    "jpg",
    "png",
    "jfif",
    "jpeg",
    "image",
    "images",
    "illustration",
    "illust",
    "abstract art"
]

function isImage(query) {
    x = query.toLowerCase().split(/\s+/);
    for(let word of similar_word){
        if (x.includes(word)) {
            return true;   
        }
    }
    return false;
}
