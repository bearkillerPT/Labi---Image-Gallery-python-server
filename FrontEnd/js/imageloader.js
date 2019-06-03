var name = ""
var listOfClasses;
var colorinfo = [];
var checkBoxStatus;
var tol = 0.15;
var thr = 50;

getList = function() {
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "http://127.0.0.1:8080/list?type=names", false);
    xhttp.send(null);
    var res = xhttp.responseText;
    listOfClasses = JSON.parse(res)
};

foo = function(state, current) {
    var grid;
    if (state == "active") {
        getImagesByName({ value: current, opc: "start" }, "grid" + current)
    }
}

createDropdown = function() {
    var dropdown = document.getElementById("dropdowns");
    var dropdownin = "";
    var i = 1;
    for (var category of listOfClasses) {
        dropdownin += "<input class='animate' type='radio' name='question' id='q" + i + "'/><label class='animate' for='q1'>" + category + "</label><p class='response animate'><div class=\"grid\" id=\"grid" + category + "\">The images are being loaded! Please wait for the server to respond!</div>"
        i += 1;
    }
    dropdown.innerHTML += dropdownin;
}

function handleFileSelect(evt) {
    var files = evt.target.files; // FileList object

    // Loop through the FileList and render image files as thumbnails.
    for (var i = 0, f; f = files[i]; i++) {

        // Only process image files.
        if (!f.type.match('image.*')) {
            continue;
        }

        var reader = new FileReader();

        // Closure to capture the file information.
        reader.onload = (function(theFile) {
            return function(e) {
                // Render thumbnail.
                var span = document.createElement('span');
                span.innerHTML = ['<img class="thumb" src="', e.target.result,
                    '" title="', escape(theFile.name), '"/>'
                ].join('');
                document.getElementById('list').insertBefore(span, null);
            };
        })(f);

        // Read in the image file as a data URL.
        reader.readAsDataURL(f);
    }
}


getImagesByName = function(self, divname) {
    if (event.key !== 'Enter' && self.opc !== "start") return;
    if (self.value != "")
        name = self.value;
    if (!(listOfClasses.includes(name)) && name !== "") return;
    var request;
    if (checkBoxStatus && colorinfo) {
        var color = "{\"R\": " + colorinfo[0] + ", \"G\": " + colorinfo[1] + ", \"B\" :" + colorinfo[2] + ", \"tol\" : " + tol + "}"
        request = "http://127.0.0.1:8080/list?type=detected&name=" + name + "&color=" + color + "&page=1&per_page=10&thr=" + thr;
    } else {
        request = "http://127.0.0.1:8080/list?type=detected&name=" + name + "&page=1&per_page=10&thr=" + thr;
    }
    var div;
    if (divname) {
        div = document.getElementById(divname);
    } else {
        var div = document.getElementById("grid");
    }
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
    }
    if (name != nameAfter && nameAfter != "")
        name = nameAfter;
    for (var i = 0; i < colorArr.length - 1; i++) {
        colorinfo[i] = colorArr[i];
    }
    if (checkBoxStatus) {
        getImagesByName({ value: "", opc: "start" }, "gridAll");
    }
};

sliderobj = function(self) {
    if (self)
        thr = self.value * 0.01;
}

slidertol = function(self) {
    if (self)
        tol = self.value * 0.01;
}

colorSearch = function() {
    checkBoxStatus = document.getElementById("checkbox").checked;
    if (!checkBoxStatus) {
        document.getElementById("parent").style.background = "#b5bfb8";
    }
};

presetsliders = function() {
    document.getElementById("sliderobj").value = thr;
    document.getElementById("slidertol").value = tol;
}

window.onload = function() {
    getList();

};


//Função importada do site w3schools para autocomplete com lista user defined, minificada para melhor gestao de codigo

function autocomplete() {
    var e = document.getElementById("filter");
    var t = listOfClasses;
    var n;

    function i(e) { if (!e) return !1;! function(e) { for (var t = 0; t < e.length; t++) e[t].classList.remove("autocomplete-active") }(e), n >= e.length && (n = 0), n < 0 && (n = e.length - 1), e[n].classList.add("autocomplete-active") }

    function a(t) { for (var n = document.getElementsByClassName("autocomplete-items"), i = 0; i < n.length; i++) t != n[i] && t != e && n[i].parentNode.removeChild(n[i]) }
    e.addEventListener("input", function(i) { var o, l, s, r = this.value; if (a(), !r) return !1; for (n = -1, (o = document.createElement("DIV")).setAttribute("id", this.id + "autocomplete-list"), o.setAttribute("class", "autocomplete-items"), this.parentNode.appendChild(o), s = 0; s < t.length; s++) t[s].substr(0, r.length).toUpperCase() == r.toUpperCase() && ((l = document.createElement("DIV")).innerHTML = "<strong>" + t[s].substr(0, r.length) + "</strong>", l.innerHTML += t[s].substr(r.length), l.innerHTML += "<input type='hidden' value='" + t[s] + "'>", l.addEventListener("click", function(t) { e.value = this.getElementsByTagName("input")[0].value, a() }), o.appendChild(l)) }), e.addEventListener("keydown", function(e) {
        var t = document.getElementById(this.id + "autocomplete-list");
        t && (t = t.getElementsByTagName("div")), 40 == e.keyCode ? (n++, i(t)) : 38 == e.keyCode ? (n--, i(t)) : 13 == e.keyCode && (e.preventDefault(), n > -1 && t && t[n].click())
    }), document.addEventListener("click", function(e) { a(e.target) })
};
//fim da funcção importada;