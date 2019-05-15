var listOfClasses
getList = function() {
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "http://127.0.0.1:8080/list?type=names", false)
    xhttp.send(null)
    var res = xhttp.responseText
    listOfClasses = JSON.parse(res)
}

getImagesByName = function(self) {
    if (event.key !== 'Enter' && self.opc != "start") return
    let name = self.value
    if (!(listOfClasses.includes(name)) && name != "") return
    let request
    if (name == "")
        request = "http://127.0.0.1:8080/list?type=detected&page=1&per_page=16"
    else
        request = "http://127.0.0.1:8080/list?type=detected&name=" + name + "&page=1&per_page=16"
    var div = document.getElementById("grid")
    console.log(request)
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", request, false)
    xhttp.send(null)
    var res = xhttp.responseText
    res = JSON.parse(res)
    var imageArray = ""
    if (name = "") {
        for (var i = 0; i < res[name].length; i++) {
            imageArray += "<div class=\"grid-item " + name + "\"><img src='http://127.0.0.1:8080/images/" + res[name][i].image + "' width=\"" + Math.round($(window).width() / 4.2) + "\"/></div>"
        }
    } else {
        for (let classes of Object.keys(res)) {
            {
                for (var i = 0; i < res[classes].length; i++) {
                    imageArray += "<div class=\"grid-item " + classes + "\"><img src='http://127.0.0.1:8080/images/" + res[classes][i].image + "' width=\"" + Math.round($(window).width() / 4.2) + "\"/></div>"
                }
            }
        }
    }
    div.innerHTML = imageArray
    setTimeout(filter, 200)
}

filter = function() {
    var msnry = new Masonry('.grid', {
        columnWidth: Math.round($(window).width() / 4),
        itemSelector: '.grid-item'
    });
}

window.onload = function() {
    getList();
    getImagesByName({ value: "", opc: "start" });
    autocomplete(document.getElementById("filter"), listOfClasses)
}

//Função importada do site w3schools para autocomplete com lista user defined, minificada para melhor gestao de codigo

function autocomplete(e, t) {
    var n;

    function i(e) { if (!e) return !1;! function(e) { for (var t = 0; t < e.length; t++) e[t].classList.remove("autocomplete-active") }(e), n >= e.length && (n = 0), n < 0 && (n = e.length - 1), e[n].classList.add("autocomplete-active") }

    function a(t) { for (var n = document.getElementsByClassName("autocomplete-items"), i = 0; i < n.length; i++) t != n[i] && t != e && n[i].parentNode.removeChild(n[i]) }
    e.addEventListener("input", function(i) { var o, l, s, r = this.value; if (a(), !r) return !1; for (n = -1, (o = document.createElement("DIV")).setAttribute("id", this.id + "autocomplete-list"), o.setAttribute("class", "autocomplete-items"), this.parentNode.appendChild(o), s = 0; s < t.length; s++) t[s].substr(0, r.length).toUpperCase() == r.toUpperCase() && ((l = document.createElement("DIV")).innerHTML = "<strong>" + t[s].substr(0, r.length) + "</strong>", l.innerHTML += t[s].substr(r.length), l.innerHTML += "<input type='hidden' value='" + t[s] + "'>", l.addEventListener("click", function(t) { e.value = this.getElementsByTagName("input")[0].value, a() }), o.appendChild(l)) }), e.addEventListener("keydown", function(e) {
        var t = document.getElementById(this.id + "autocomplete-list");
        t && (t = t.getElementsByTagName("div")), 40 == e.keyCode ? (n++, i(t)) : 38 == e.keyCode ? (n--, i(t)) : 13 == e.keyCode && (e.preventDefault(), n > -1 && t && t[n].click())
    }), document.addEventListener("click", function(e) { a(e.target) })
}
//fim da funcção importada