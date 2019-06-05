
var checkboxes = {
  color: false,
  color_conf: false,
  class: false
};
var sliders = {
  class_detection_confidence: 0.15,
  color_confidence: 0.5
};
var color = {};
var name = "";
var c_page = 1;
search_handler = self => {
  name = self.value;  
  if (event.key == "Enter") search();
};
class_confidence_slider_handler = self => {
  sliders.class_detection_confidence = self.value;
};
color_confidence_slider_handler = self => {
  sliders.color_confidence = self.value;
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

color_checkbox_handler = (self)=>{
  checkboxes.color = self.checked
}

color_confidence_checkbox_handler = (self)=>{
  checkboxes.color_conf = self.checked
}

class_checkbox_handler = (self)=>{
  checkboxes.class = self.checked
}
