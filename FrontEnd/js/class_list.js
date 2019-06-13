let url = "https://xcoa.av.it.pt/labi2019-p2-g2/list?type=names";

fetch(url)
  .then(res => res.json())
  .then(res => {
    for (let i of res) {
      fetch(
        "https://xcoa.av.it.pt/labi2019-p2-g2/list?type=detected&per_page=3&name=" +
          i
      )
        .then(res => res.json())
        .then(res => {
          let tmp_name = Object.keys(res)[0];
          res = res[Object.keys(res)[0]];
          let master_to_add = "";
          master_to_add += '<h4 class="class_list_item_text"><a href="https://xcoa.av.it.pt/labi2019-p2-g2/search_images.html?name=' + tmp_name + '" >'+
          capitalize(tmp_name) +
            '</a></h4><div class="gridywrap" style="height:320px">';
          for (let i of res) {
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
                capitalize(tmp_name) +
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
            master_to_add += to_add;
          }
          master_to_add +=
            res.length <= 1
              ? '<div class="gridy-1 gridyhe-1">' +
                '    <div class="gridimg" style="background-image:' +
                ' url()">&nbsp;</div></div>'
              : "";
          master_to_add +=
            res.length <= 2
              ? '<div class="gridy-1 gridyhe-1">' +
                '    <div class="gridimg" style="background-image:' +
                ' url()">&nbsp;</div></div>'
              : "";
          master_to_add += "</div>";
          classes_div.innerHTML += master_to_add;
        })
        .catch(e => console.log(e));
    }
  });
