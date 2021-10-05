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
        console.log(recipe_id);
        event.preventDefault();
        $.ajax({
            url: "/recipe/make_favorite/",
            type: "POST",
            dataType: "json",
            contentType: "application/x-www-form-urlencoded",
            data: {
                'recipe_id': recipe_id,
            },
            beforeSend: function(xhr, settings){
                if(!csrfSafeMethod(settings.type)&&!this.crossDomain){
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            success:function(data){
                console.log(data);
                recipe_id = data["recipe_id"]
                $(`#recipe-${recipe_id}`).html(
                    `<button type="button"  class="btn btn-danger m-2 favorite-destroy-button" value=${recipe_id}>
                        お気に入り解除
                    </button>`
                );
            },
            error:function(req,text){
                console.log(text);
            },
        });
   });
   $(document).on('click', '.favorite-destroy-button', function(event) {
        let recipe_id = $(this).val();
        console.log(recipe_id);
        event.preventDefault();
        $.ajax({
            url: "/recipe/destroy_favorite/",
            type: "POST",
            dataType: "json",
            contentType: "application/x-www-form-urlencoded",
            data: {
                'recipe_id': recipe_id,
            },
            beforeSend: function(xhr, settings){
                if(!csrfSafeMethod(settings.type)&&!this.crossDomain){
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            success:function(data){
                console.log(data);
                recipe_id = data["recipe_id"]
                $(`#recipe-${recipe_id}`).html(
                    `<button type="button"  class="btn btn-success m-2 favorite-make-button" value=${recipe_id}>
                        お気に入り登録
                    </button>`
                );
            },
            error:function(req,text){
                console.log(text);
            },
        });
    
    });


    $(document).on('click', '.favorite-destroy-button2', function(event) {
        let recipe_id = $(this).val();
        console.log(recipe_id);
        event.preventDefault();
        $.ajax({
            url: "/recipe/destroy_favorite/",
            type: "POST",
            dataType: "json",
            contentType: "application/x-www-form-urlencoded",
            data: {
                'recipe_id': recipe_id,
            },
            beforeSend: function(xhr, settings){
                if(!csrfSafeMethod(settings.type)&&!this.crossDomain){
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            success:function(data){
                console.log(data);
                console.log("2");
                recipe_id = data["recipe_id"]
                $(`#recipe-${recipe_id}-contain`).html("");
            },
            error:function(req,text){
                console.log(text);
            },
        });
    
    });
   

});