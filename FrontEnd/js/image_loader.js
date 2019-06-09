search = () => {
  next_elem.style.visibility = "visible";
  let url = "https://xcoa.av.it.pt/labi2019-p2-g2/list?type=detected";
  let b_color = color;
  b_color["tol"] = 0.9;
  if (checkboxes.color_conf) b_color["tol"] = sliders.color_confidence;
  else b_color["tol"] = 0.9;
  if (name != "") url += "&name=" + name;
  if (checkboxes.class) url += "&thr=" + sliders.class_detection_confidence;
  if (checkboxes.color) url += "&color=" + JSON.stringify(b_color);
  url += "&page=" + c_page + "&per_page=24";
  //console.log(url);
  fetch(url)
    .then(res => res.json())
    .then(res => {
      if (name != "") return res[name];
      else return res;
    })
    .then(res => {
      last_page = res.length != 24
      if (last_page) next_elem.style.visibility = "hidden";
      let total_height = 320 + (res.length - 1) * 320 / 3
      total_height = total_height - total_height % 320
      gallery_div.style.height = total_height + "px"

      gallery_div.innerHTML = "";
      for (let i of res) {
        let class_name = name == "" ? i.class : name;
        class_name = capitalize(class_name);
        let to_add = "";
        if (i.image != i.original)
          to_add =
            '<div class="gridy-1 gridyhe-1">' +
            '    <div class="gridimg" style="background-image:' +
            " url(https://xcoa.av.it.pt/labi2019-p2-g2/images/" +
            i.image +
            ')">&nbsp;</div>' +
            '    <div class="gridinfo"><br><br>' +
            '      <h4 class="h4">Class: ' +
            class_name +
            "</h4>" +
            '      <h4 class="h4">Confidence: ' +
            i.confidence +
            "</h4>" +
            '      <a href="' +
            "image_inspect.html?id=" +
            i.original +
            '" class="grid-btn grid-more"><span>More</span> <i class="fa fa-plus"></i></a>' +
            "    </div>" +
            "  </div>";
        gallery_div.innerHTML += to_add;
      }
    })
    .catch(e => console.log(e));
};

capitalize = str => str.charAt(0).toUpperCase() + str.substring(1);
