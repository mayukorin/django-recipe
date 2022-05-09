function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

let csrftoken = getCookie('csrftoken');

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
   $('.favorite-button').on('click', '.favorite-make-button', function(event) {
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
            $(`#recipe-${recipe_id}-favorite-button`).html(
                `<button type="button"  class="btn btn-danger m-2 favorite-destroy-button" value=${recipe_id}>
                    お気に入り解除
                </button>`
            );
        })
    })

    $('.favorite-button').on('click', '.favorite-destroy-button', function(event) {
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
            let base_url = $(location).attr('origin');
            console.log(base_url);
            if (template_name == "recipe_favorite_list") {
                console.log(data);
                let now_page_favorite_recipe_cnt = $('.recipe-img').length;
                if (now_page_favorite_recipe_cnt == 1 || now_page_favorite_recipe_cnt == data.favorite_recipe_cnt)  {
                    console.log("recipe-ok");
                    location.href = base_url + '/recipe/recipes/favorite';
                }
                else {
                    console.log("not 0");
                    $(`#recipe-${recipe_id}-article`).remove();
                }
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
