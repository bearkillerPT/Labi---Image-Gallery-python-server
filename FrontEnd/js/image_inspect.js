var canvas = document.getElementById("viewport"),
  context = canvas.getContext("2d");

fetch("https://xcoa.av.it.pt/labi2019-p2-g2/get?id=" + getUrlVars().id)
  .then(res => res.json())
  .then(res => {
    let base_image = new Image();
    base_image.src =
      "https://xcoa.av.it.pt/labi2019-p2-g2/images/" + getUrlVars().id;
    base_image.onload = function() {
      context.canvas.width = $(window).width();
      context.canvas.height = 500;
      let scale = canvas.height / base_image.height;
      let top_left_x = ($(window).width() - base_image.width * scale) / 2;
      context.drawImage(
        base_image,
        top_left_x,
        0,
        base_image.width * scale,
        base_image.height * scale
      );
      for (let i of res) {
        context.beginPath();
        context.font = "20px Arial";
        context.fillStyle = "red";
        context.fillText(
          i.class,
          top_left_x + i.box.x * scale + 5,
          +20 + i.box.y * scale
        );
        context.lineWidth = "1";
        context.strokeStyle = "blue";
        context.rect(
          top_left_x + i.box.x * scale,
          i.box.y * scale,
          i.box.x1 * scale - i.box.x * scale,
          i.box.y1 * scale - i.box.y * scale
        );
        context.stroke();
      }
    };
  })
  .catch(e => console.log(e));

/*Obtem os parametro passados no url*/
/*função copiada do stack overflow*/
function getUrlVars() {
  var vars = {};
  var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(
    m,
    key,
    value
  ) {
    vars[key] = value;
  });
  return vars;
}
