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
    // makeRequest2(dataUrl, getVisionAPIInfo);
    recognizeIngredient(dataUrl)
  }
  // reader.onload = recognizeIngredient(reader)
}

function ingredientDetectionByLabel(dataUrl) {

  var defer = new $.Deferred();
  var end = dataUrl.indexOf(",")
  var request =  "{'requests': [{'image': {'content': '" + dataUrl.slice(end + 1) + "'},'features': [{'type': 'LABEL_DETECTION','maxResults': 100,}]}]}";
  var ingredients_pk_and_names = new Map();
  $.ajax({
    url: "/recipe/ingredients/vision_api_info/",
    method: "POST",
    dataType: "json",
    data: {
        'search_param': request,
    },
  }).done(function(result) {
    console.log(result);
    if (result.responses[0].labelAnnotations != null) {
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
        }
      }).done(function(result) {
        console.log("label detection finised");
        console.log(result);
        ingredients_pk_and_names = result;
        console.log(ingredients_pk_and_names);
        defer.resolve(ingredients_pk_and_names);
      })
    } 
  }).fail(function() {
    defer.reject('failed to load info');
  });
  return defer.promise();
  /*
  var end = dataUrl.indexOf(",")
  var request =  "{'requests': [{'image': {'content': '" + dataUrl.slice(end + 1) + "'},'features': [{'type': 'LABEL_DETECTION','maxResults': 100,}]}]}";
  var ingredients_pk_and_names = new Map();
  $.ajax({
    url: "/recipe/ingredients/vision_api_info/",
    method: "POST",
    dataType: "json",
    data: {
        'search_param': request,
    },
  }).done(function(result) {
    console.log(result);
    if (result.responses[0].labelAnnotations != null) {
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
        }
      }).done(function(result) {
        console.log("label detection finised");
        console.log(result);
        ingredients_pk_and_names = result;
        console.log(ingredients_pk_and_names);
        return ingredients_pk_and_names;
      })
    } 
  }).fail(function(result) {
    console.log('failed to load info');
  });
  */

}

function recognizeIngredient(dataUrl) {
  

  // var ingredients_pk_and_name_by_label_detection = ingredientDetectionByLabel(dataUrl);
  var ingredients_pk_and_name_by_label_detection = new Map();
  /*
  ingredientDetectionByLabel(dataUrl).then((result) => {
    ingredients_pk_and_name_by_label_detection = result;
    ingredientDetectionByText(dataUrl).then((result) => {
      console.log(ingredients_pk_and_name_by_label_detection);
      console.log(result);
      result = new Map();
      Object.assign(ingredients_pk_and_name_by_label_detection, result);
      showResult22(ingredients_pk_and_name_by_label_detection);
    });
  });
  */
  ingredientDetectionByLabel(dataUrl).then((result) => {
    ingredients_pk_and_name_by_label_detection = result;
    return ingredientDetectionByText(dataUrl);
  }).then((result) => {
    result = new Map();
    Object.assign(ingredients_pk_and_name_by_label_detection, result);
    showResult(ingredients_pk_and_name_by_label_detection);
  })
  // console.log(ingredients_pk_and_name_by_label_detection);
  // console.log(ingredients_pk_and_name_by_label_detection);
  // Object.assign(ingredients_pk_and_name_by_label_detection, ingredients_pk_and_name_by_text_detection);
  // showResult22(ingredients_pk_and_name_by_label_detection);
}




function ingredientDetectionByText(dataUrl) {
  var defer = new $.Deferred();
  var end = dataUrl.indexOf(",");
  var request =  "{'requests': [{'image': {'content': '" + dataUrl.slice(end + 1) + "'},'features': [{'type': 'DOCUMENT_TEXT_DETECTION','maxResults': 100,}]}]}";
  var ingredients_pk_and_names = new Map();
  $.ajax({
    url: "/recipe/ingredients/vision_api_info/",
    method: "POST",
    dataType: "json",
    data: {
        'search_param': request,
    },
  }).done(function(result) {
    console.log(result);
    if (result.responses[0].textAnnotations != null) {
      console.log(result.responses[0].fullTextAnnotation.text);
      var japanese_name_array = result.responses[0].fullTextAnnotation.text.split(/\n/);
      // var japanese_name_array = result.responses[0].textAnnotations.map((object) => object.description);
      // japanese_name_array.shift();
      console.log(japanese_name_array);
      $.ajax({
        url: "/recipe/ingredients/hiragana_api_info/",
        method: "GET",
        dataType: "json",
        data: {
            'japanese_names': japanese_name_array,
        },
      }).done(function(hiragana_array) {
          $.ajax({
            url: "/recipe/ingredients/search_by_hiragana_name/",
            method: "GET",
            dataType: "json",
            data: {
              "ingredient_hiragana_names": hiragana_array
            }
          }).done(function(result) {
            ingredients_pk_and_names = result;
            console.log(ingredients_pk_and_names);
            defer.resolve(ingredients_pk_and_names);
          })
        })
      }
  });
  return defer.promise();
}


function makeRequest(dataUrl, callback) {

  var end = dataUrl.indexOf(",")
  var request =  "{'requests': [{'image': {'content': '" + dataUrl.slice(end + 1) + "'},'features': [{'type': 'OBJECT_LOCALIZATION','maxResults': 100,}]}]}"
  callback(request)

}

function makeRequest2(dataUrl, callback) {
  var end = dataUrl.indexOf(",")
  var request =  "{'requests': [{'image': {'content': '" + dataUrl.slice(end + 1) + "'},'features': [{'type': 'DOCUMENT_TEXT_DETECTION','maxResults': 100,}]}]}"
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
    showResult2(result);
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

function showResult2(result) {
  console.log(result);
  console.log("hos")
  var japanese_name_array = result.responses[0].textAnnotations.map((object) => object.description);
  japanese_name_array.shift();
  console.log(japanese_name_array);
  $.ajax({
    url: "/recipe/ingredients/hiragana_api_info/",
    method: "GET",
    dataType: "json",
    data: {
        'japanese_names': japanese_name_array,
    },
  }).done(function(hiragana_array) {
      $.ajax({
        url: "/recipe/ingredients/search_by_hiragana_name/",
        method: "GET",
        dataType: "json",
        data: {
          "ingredient_hiragana_names": hiragana_array
        }
      }).done(function(data) {
        console.log(data);
      })
  });
}

function showResult(ingredients_pk_and_names) {
  if (ingredients_pk_and_names.length == 0) {
    var alert_message = `<div class="alert alert-danger" role="alert">
                      食材が一つも識別されませんでした
                      </div>`;
    $('.no_food').append($(alert_message));
  } else {
    $('#recognition_to_search_button').removeClass("hidden");
    $.each(ingredients_pk_and_names, function(index, pk_and_name) {
      var check_form = `
      <div class='custom-control custom-checkbox food_check'>
      <input type="checkbox" class='custom-control-input' name='ingredients' id='custom-check-${index}' value=${pk_and_name["pk"]} checked>
      <label class='custom-control-label' for='custom-check-${index}'>${pk_and_name["name"]}</label>
      </div>`;
      $('#checkboxes').append($(check_form));
    });
  }
}


function showResult22(result) {
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
