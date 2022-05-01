'use strict';

$(document).ready(function() {
  console.log("ok");
  $('#uploader').change(function(evt) {
    clear();
    getImageInfo(evt);
    clear();
    $(".ImageArea").removeClass("hidden");
    $(".resultArea").removeClass("hidden");
  })
});


function clear() {
  $('#checkboxes').text("");
  $('.no_food').text("");
  $('#recognition_to_search_button').addClass("hidden");
}

function getImageInfo(evt) {
  var file = evt.target.files;
  var reader = new FileReader();
  var dataUrl = "";
  reader.readAsDataURL(file[0]);
  reader.onload = function() {
    dataUrl = reader.result;
    $('#showPic').html("<img src='" + dataUrl + "'>");
    makeRequest(dataUrl, getVisionAPIInfo);
  }
}

function makeRequest(dataUrl, callback) {

  var end = dataUrl.indexOf(",")
  var request =  "{'requests': [{'image': {'content': '" + dataUrl.slice(end + 1) + "'},'features': [{'type': 'LABEL_DETECTION','maxResults': 10,}]}]}"
  callback(request)

}

function getVisionAPIInfo(request) {


  $.ajax({
    url: "/recipe/ingredients/vision_api_info/",
    method: "POST",
    dataType: "json",
    data: {
        'search_param': request,
    },
  }).done(function(result) {
    console.log(result);
    showResult(result);
  }).fail(function(result) {
    console.log('failed to load info');
  });
  /*
  $.ajax({
    url: VisionApiUrl,
    type: 'POST',
    async: true,
    cache: false, 
    data: request,
    dataType: 'json',
    contentType: 'application/json',
  }).done(function(result) {
    console.log(result);
    showResult(result);
  }).fail(function(result) {
    console.log('failed to load info');
  });
  */
}

function showResult(result) {
  if (result.responses[0].labelAnnotations == null) {
    var alert_message = `<div class="alert alert-danger" role="alert">
                          食材が一つも識別されませんでした
                          </div>`;
    $('.no_food').append($(alert_message));
  } else {
    var english_name_array = result.responses[0].labelAnnotations.map((object) => object.description);
    console.log(english_name_array);
    var english_name_set = new Set(english_name_array);
    english_name_array = Array.from(english_name_set);
    $.ajax({
        url: "/recipe/ingredients/search_by_english_name/",
        method: "GET",
        dataType: "json",
        data: {
            'ingredient_english_names': english_name_array,
        },
    }).done(function(data) {
        console.log(data);
        if (data.length == 0) {
          var alert_message = `<div class="alert alert-danger" role="alert">
                            食材が一つも識別されませんでした
                            </div>`;
          $('.no_food').append($(alert_message));
        } else {
          $('#recognition_to_search_button').removeClass("hidden");
          $.each(data, function(index, id_and_name) {
            var check_form = `
            <div class='custom-control custom-checkbox food_check'>
            <input type="checkbox" class='custom-control-input' name='ingredients' id='custom-check-${index}' value=${id_and_name["pk"]}>
            <label class='custom-control-label' for='custom-check-${index}'>${id_and_name["name"]}</label>
            </div>`;
            $('#checkboxes').append($(check_form));
          });
        }
      });
    }
  }
/*
    english_name_set.forEach((english_name, index) => {
      console.log(english_name);
      if (data[english_name]) {
        var check_form = `
          <div class='custom-control custom-checkbox food_check'>
          <input type="checkbox" class='custom-control-input' name='categories[]' id='custom-check-${index}' value=${data[english_name][0]["id"]}>
          <label class='custom-control-label' for='custom-check-${index}'>${data[english_name][0]["japanese_name"]}</label>
          </div>`;
          $('#checkboxes').append($(check_form));
          flag = 1;
      }
    })

    if (flag==1) {
      $('#recognition_to_search_button').removeClass("hidden");
    } else {
      var alert_message = `<div class="alert alert-danger" role="alert">
                          食材が一つも識別されませんでした
                          </div>`;
      $('.no_food').append($(alert_message));
    }
  });
  */
