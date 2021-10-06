
$(document).ready(function() {

   $(document).on('click', '.favorite-make-button', function(event) {
        let recipe_id = $(this).val();
        console.log(recipe_id);
        event.preventDefault();
        $.ajax({
            url: "/recipe/make_favorite/",
            type: "POST",
            dataType: "json",
            data: {
                'recipe_id': recipe_id,
            },
        }).done(function(data) {
            console.log(data);
            recipe_id = data["recipe_id"]
            $(`#recipe-${recipe_id}`).html(
                `<button type="button"  class="btn btn-danger m-2 favorite-destroy-button" value=${recipe_id}>
                    お気に入り解除
                </button>`
            );
        })
    })

    $(document).on('click', '.favorite-destroy-button', function(event) {
        let recipe_id = $(this).val();
        console.log(recipe_id);
        event.preventDefault();
        $.ajax({
            url: "/recipe/destroy_favorite/",
            type: "POST",
            dataType: "json",
            data: {
                'recipe_id': recipe_id,
            },
        }).done(function(data) {
            
            recipe_id = data["recipe_id"]
            $(`#recipe-${recipe_id}`).html(
                `<button type="button"  class="btn btn-success m-2 favorite-make-button" value=${recipe_id}>
                    お気に入り登録
                </button>`
            );
        })
    
    })

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
        }).done(function(data) {
            recipe_id = data["recipe_id"]
            $(`#recipe-${recipe_id}-contain`).html("");

        })
    })

})
