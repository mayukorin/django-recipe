'use strict';

$(document).ready(function() {
    console.log("ok");
    $('#uploader').change(function(evt) {
        let file = evt.target.files;
        let reader = new FileReader();
        let dataUrl = "";
        try {
            reader.readAsDataURL(file[0]);
            reader.onload = function() {
                dataUrl = reader.result;
                $('#showPic').html("<img src='" + dataUrl + "'>");
                clear();
                removeHidden('#progress-info');

                recognizeIngredient(dataUrl);

                removeHidden(".ImageArea");
                removeHidden(".resultArea");
            }
        } catch (e) {
            console.log(e);
        }

    })
});

function clear() {
    $('#checkboxes').text("");
    $('.no_food').text("");
    addHidden('#recognition_to_search_button');
    removeHidden('#progress-info');
    changeProgressBarStatus('0');
    addHidden('#label-vision-api');
    $('#recognition_title').text("識別中．．．");
}

function removeHidden(selectorName) {
    $(selectorName).removeClass('hidden');
}

function addHidden(selectorName) {
    $(selectorName).addClass('hidden');
}

function changeProgressBarStatus(ratio) {
    $('#progress-info').css('width', `${ratio}%`);
    $('#progress-info').text(`${ratio}%`);
}

function recognizeIngredient(dataUrl) {

    ingredientDetectionByLabel(dataUrl).then((result) => {
        let ingredients_pk_and_name_by_label_detection = result;
        ingredientDetectionByText(dataUrl).then((ingredients_pk_and_name_by_text_detection) => {
            let all_ingredients_pk_and_names = new Map();
            ingredients_pk_and_name_by_label_detection.concat(ingredients_pk_and_name_by_text_detection).forEach(function(ingredient_pk_and_name) {
                all_ingredients_pk_and_names.set(ingredient_pk_and_name["pk"], ingredient_pk_and_name["name"]);
            });
            showResult(Array.from(all_ingredients_pk_and_names));
        });
    });
}

function ingredientDetectionByLabel(dataUrl) {

    let defer = new $.Deferred();
    let end = dataUrl.indexOf(",")
    let request = "{'requests': [{'image': {'content': '" + dataUrl.slice(end + 1) + "'},'features': [{'type': 'LABEL_DETECTION','maxResults': 100,}]}]}";
    $.ajax({
        url: "/recipe/ingredients/vision_api_info/",
        method: "POST",
        dataType: "json",
        data: {
            'search_param': request,
        },
    }).done(function(result) {
        console.log(result);
        changeProgressBarStatus('20');
        if (result.responses[0].labelAnnotations != null) {

            let object_english_name_list_detected = result.responses[0].labelAnnotations.map((object) => object.description);
            object_english_name_list_detected = Array.from(new Set(object_english_name_list_detected));
            console.log(object_english_name_list_detected);

            $.ajax({
                url: "/recipe/ingredients/search_by_english_name/",
                method: "GET",
                dataType: "json",
                data: {
                    'object_english_name_list_detected': object_english_name_list_detected,
                }
            }).done(function(ingredient_pk_and_name_list) {
                console.log(ingredient_pk_and_name_list);
                changeProgressBarStatus('40');
                defer.resolve(ingredient_pk_and_name_list);
            })
        } else {
            changeProgressBarStatus('40');
            defer.resolve([]);
        }
    }).fail(function() {
        defer.reject('failed to load info');
    });
    return defer.promise();
}

function ingredientDetectionByText(dataUrl) {
    let defer = new $.Deferred();
    let end = dataUrl.indexOf(",");
    let request = "{'requests': [{'image': {'content': '" + dataUrl.slice(end + 1) + "'},'features': [{'type': 'DOCUMENT_TEXT_DETECTION','maxResults': 100,}]}]}";
    $.ajax({
        url: "/recipe/ingredients/vision_api_info/",
        method: "POST",
        dataType: "json",
        data: {
            'search_param': request,
        },
    }).done(function(result) {
        changeProgressBarStatus('60');
        if (result.responses[0].textAnnotations != null) {

            console.log(result.responses[0].fullTextAnnotation.text);
            let text_list_detected = result.responses[0].fullTextAnnotation.text.split(/\n/);
            console.log(text_list_detected);

            $.ajax({
                url: "/recipe/ingredients/conversion_to_hiragana/",
                method: "GET",
                dataType: "json",
                data: {
                    'text_list_detected': text_list_detected,
                },
            }).done(function(hiragana_text_detected_list) {
                changeProgressBarStatus('80');
                console.log(hiragana_text_detected_list);
                $.ajax({
                    url: "/recipe/ingredients/search_by_hiragana_name/",
                    method: "POST",
                    dataType: "json",
                    data: {
                        "hiragana_text_detected_list": hiragana_text_detected_list
                    }
                }).done(function(ingredient_pk_and_name_list) {
                    addHidden('#hiragana-conversion');
                    removeHidden('#hiragana-search');
                    console.log(ingredient_pk_and_name_list);
                    changeProgressBarStatus('100');
                    defer.resolve(ingredient_pk_and_name_list);
                })
            })
        } else {
            changeProgressBarStatus('100');
            defer.resolve([]);
        }
    });
    return defer.promise();
}

function showResult(ingredients_pk_and_names) {
    $('#recognition_title').text('識別結果');
    if (ingredients_pk_and_names.length == 0) {
        let alert_message = `<div class="alert alert-danger" role="alert">
                      食材が一つも識別されませんでした
                      </div>`;
        $('.no_food').append($(alert_message));
    } else {
        removeHidden('#recognition_to_search_button');
        let index = 0;
        for (let [pk, name] of ingredients_pk_and_names) {
            let check_form = `
      <div class='custom-control custom-checkbox food_check'>
      <input type="checkbox" class='custom-control-input' name='ingredients' id='custom-check-${index}' value=${pk} checked>
      <label class='custom-control-label' for='custom-check-${index}'>${name}</label>
      </div>`;
            $('#checkboxes').append($(check_form));
            index += 1;
        }
    }
}