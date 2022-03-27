function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            console.log(csrftoken);
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});



$(document).ready(function() {
   $(document).on('click', '.favorite-make-button', function(event) {
        let recipe_id = $(this).val();
        event.preventDefault();
        $.ajax({
            url: "/recipe/make_favorite/",
            method: "POST",
            dataType: "json",
            data: {
                'recipe_id': recipe_id,
            },
        }).done(function(data) {
            recipe_id = data["recipe_id"]
            $(`#recipe-${recipe_id}-favorite-button`).html(
                `<button type="button"  class="btn btn-danger m-2 favorite-destroy-button" value=${recipe_id}>
                    お気に入り解除
                </button>`
            );
        })
    })

    $(document).on('click', '.favorite-destroy-button', function(event) {
        let recipe_id = $(this).val();
        event.preventDefault();
        let template_name = $(this).data('template');
        $.ajax({
            url: "/recipe/destroy_favorite/",
            method: "POST",
            dataType: "json",
            data: {
                'recipe_id': recipe_id,
            },
        }).done(function(data) {
            
            recipe_id = data["recipe_id"]
            if (template_name == "favorite_recipe") {
                $(`#recipe-${recipe_id}-article`).html("");
                let recipe_cnt = $('.recipe-img').length;
                if (recipe_cnt == 0) $(`#favorite_recipe`).html(`<h1>お気に入りレシピがありません</h1>`);
            } else {
                $(`#recipe-${recipe_id}-favorite-button`).html(
                    `<button type="button"  class="btn btn-success m-2 favorite-make-button" value=${recipe_id}>
                        お気に入り登録
                    </button>`
                );
            }
        })
    
    })

})
