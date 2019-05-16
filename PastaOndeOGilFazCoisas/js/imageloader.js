var name = ""
var listOfClasses;
var color = "";
var checkBoxStatus;

getList = function() {
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "http://127.0.0.1:8080/list?type=names", false);
    xhttp.send(null);
    var res = xhttp.responseText;
    listOfClasses = JSON.parse(res)
};

getImagesByName = function(self) {
    if (event.key !== 'Enter' && self.opc !== "start") return;
    if (self.value != "")
        name = self.value;
    if (!(listOfClasses.includes(name)) && name !== "") return;
    var request;
    if (checkBoxStatus) {
        request = "http://127.0.0.1:8080/list?type=detected&name=" + name + "&color=" + color + "&page=1&per_page=10";
    } else {
        request = "http://127.0.0.1:8080/list?type=detected&name=" + name + "&page=1&per_page=10";
    }
    var div = document.getElementById("grid");
    console.log(request);
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", request, false);
    xhttp.send(null);
    var res = xhttp.responseText;
    res = JSON.parse(res);
    var imageArray = "";
    if (name !== "") {
        for (var i = 0; i < res[name].length; i++) {
            imageArray += "<div class=\"grid-item " + name + "\"><img src='http://127.0.0.1:8080/images/" + res[name][i].image + "' width=\"" + Math.round($(window).width() / 4.2) + "\"/></div>";
        }
    } else {
        for (var i = 0; i < res.length; i++) {
            imageArray += "<div class=\"grid-item \"><img src='http://127.0.0.1:8080/images/" + res[i].image + "' width=\"" + Math.round($(window).width() / 4.2) + "\"/></div>";
        }
    }

    div.innerHTML = imageArray;
    setTimeout(filter, 400);
};

filter = function() {
    var msnry = new Masonry('.grid', {
        columnWidth: Math.round($(window).width() / 4),
        itemSelector: '.grid-item'
    });
};

defColor = function(colorArr) {
    var nameAfter = document.getElementById("filter").value;
    if (!checkBoxStatus) {
        document.getElementById("parent").style.background = "#b5bfb8";
        alert("Please check the checkbox before selecting a color!")
    }
    if (name != nameAfter && nameAfter != "")
        name = nameAfter;
    color = "{\"R\": " + colorArr[0] + ", \"G\": " + colorArr[1] + ", \"B\" :" + colorArr[2] + ", \"tol\" : 0.15}";
    if (checkBoxStatus) {
        getImagesByName({ value: "", opc: "start" });
    }
};

colorSearch = function() {
    checkBoxStatus = document.getElementById("checkbox").checked;
    if (!checkBoxStatus) {
        document.getElementById("parent").style.background = "#b5bfb8";
    }
};

window.onload = function() {
    document.getElementById("checkbox").checked = false;
    getList();
    getImagesByName({ value: "", opc: "start" });
    autocomplete(document.getElementById("filter"), listOfClasses)
};


//Função importada do site w3schools para autocomplete com lista user defined, minificada para melhor gestao de codigo

function autocomplete(e, t) {
    var n;

    function i(e) { if (!e) return !1;! function(e) { for (var t = 0; t < e.length; t++) e[t].classList.remove("autocomplete-active") }(e), n >= e.length && (n = 0), n < 0 && (n = e.length - 1), e[n].classList.add("autocomplete-active") }

    function a(t) { for (var n = document.getElementsByClassName("autocomplete-items"), i = 0; i < n.length; i++) t != n[i] && t != e && n[i].parentNode.removeChild(n[i]) }
    e.addEventListener("input", function(i) { var o, l, s, r = this.value; if (a(), !r) return !1; for (n = -1, (o = document.createElement("DIV")).setAttribute("id", this.id + "autocomplete-list"), o.setAttribute("class", "autocomplete-items"), this.parentNode.appendChild(o), s = 0; s < t.length; s++) t[s].substr(0, r.length).toUpperCase() == r.toUpperCase() && ((l = document.createElement("DIV")).innerHTML = "<strong>" + t[s].substr(0, r.length) + "</strong>", l.innerHTML += t[s].substr(r.length), l.innerHTML += "<input type='hidden' value='" + t[s] + "'>", l.addEventListener("click", function(t) { e.value = this.getElementsByTagName("input")[0].value, a() }), o.appendChild(l)) }), e.addEventListener("keydown", function(e) {
        var t = document.getElementById(this.id + "autocomplete-list");
        t && (t = t.getElementsByTagName("div")), 40 == e.keyCode ? (n++, i(t)) : 38 == e.keyCode ? (n--, i(t)) : 13 == e.keyCode && (e.preventDefault(), n > -1 && t && t[n].click())
    }), document.addEventListener("click", function(e) { a(e.target) })
};
//fim da funcção importada