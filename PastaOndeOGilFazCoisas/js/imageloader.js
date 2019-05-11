var div = document.getElementById("nice")
funcaodogil = function(type) {
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "http://127.0.0.1:8080/list?type=detected&name=" + type, false)
    xhttp.send(null)
    let res = xhttp.responseText
    res = JSON.parse(res)
    console.log(res)
    let a = ""
    for (let i = 0; i < res[type].length; i++) {
        a +=  "<div class=\"grid-item \"   <img src='http://127.0.0.1:8080/images/" + res.person[i].image + "'/>"
    }
    div.innerHTML += a
}