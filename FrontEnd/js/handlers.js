var checkboxes = {
  color: false,
  color_conf: false,
  class: false
};
var sliders = {
  class_detection_confidence: 0.15,
  color_confidence: 0.9
};
var color = {};
var name = "";
var c_page = 1;
var last_page = false;
next_handler = self => {
  if (c_page == 1) prev_elem.style.visibility = "visible";
  if (last_page) next_elem.style.visibility = "hidden";
  c_page++;
  search();
};
prev_handler = self => {
  if (c_page == 2) prev_elem.style.visibility = "hidden";
  if (last_page) next_elem.style.visibility = "visible";
  c_page--;
  search();
};
search_handler = self => {
  name = self.value.toLowerCase();
  if (event.key == "Enter") search();
};
class_confidence_slider_handler = self => {
  sliders.class_detection_confidence = self.value;
};
color_confidence_slider_handler = self => {
  sliders.color_confidence = 1 - self.value;
};
search_button_handler = self => {
  search();
};
picker_handler = _color => {
  color["R"] = _color._rgba[0];
  color["G"] = _color._rgba[1];
  color["B"] = _color._rgba[2];
  if (checkboxes.color) search();
};

color_checkbox_handler = self => {
  checkboxes.color = self.checked;
};

color_confidence_checkbox_handler = self => {
  checkboxes.color_conf = self.checked;
};

class_checkbox_handler = self => {
  checkboxes.class = self.checked;
};
window.onload = () => {
  t_name = getUrlVars().name;
  if (t_name == null) {
    name = "";
  } else {
    name = t_name;
    name_input.value = name;
    name_input.focus();
    name_input.blur();
    search();
  }
};
function getUrlVars() {
  var vars = {};
  var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(
    m,
    key,
    value
  ) {
    vars[key] = value;
  });
  console.log(vars)
  vars.name = vars.name.replace("%20", " ");
  console.log(vars)
  return vars;
}
