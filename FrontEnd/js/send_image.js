send_image = self => {
  let data = new FormData();
  data.append("image", self.files[0]);
  fetch("https://xcoa.av.it.pt/labi2019-p2-g2/put", {
    method: "POST",
    body: data
  })
    .then(res => res.json())
    .then(res => {
      if (res[0] == "Any class detected") alert("Any class detected");
      else window.open("image_inspect.html?id=" + res[1][0].original,"_self");
    })
    .catch(e => console.log(e));
};
