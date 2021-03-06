$(document).ready(function() {
    // チェックボックスのクリックを無効化します。
    $('.image_box .disabled_checkbox').click(function() {
      return false;
    });
      
    // 画像がクリックされた時の処理です。
    $('.progressive').on('click', function() {
      console.log("ok");
      if (!$(this).children('img').is('.checked')) {
        // チェックが入っていない画像をクリックした場合、チェックを入れます。
        console.log("check");
        $(this).children('img').addClass('checked');
        $(this).siblings('input').prop('checked',true);
      } else {
        // チェックが入っている画像をクリックした場合、チェックを外します。
        $(this).children('img').removeClass('checked');
        $(this).siblings('input').prop('checked',false);
      }
    });
    $('.progressive').on('reset', function() {
        //リセット時、checkクラスをoffにする
        $(this).children('img').removeClass('checked');
        $(this).siblings('input').prop('checked',false);
    });
    $('#clear').click(function(){
      $('.progressive').children('img').removeClass('checked');
      $('input[type="checkbox"]').prop('checked',false);
    });
    $('.recipe-click-area').click(function() {
      window.location.href = $(this).data('link');
    });
});

$(window).on('load',function(){
    $('input[type="checkbox"]').prop('checked',false);

});


d1 = document.getElementById("recipe_result");
d2 = document.getElementById("select-myrecipe");
d3 = document.getElementById("myrecipe_result");
d4 = document.getElementById("select-myrecipe-delete");

  
function clickBtn1() {
    // 選択に変える
    d1.style.display = "none";
    d2.style.display = "block";
}

function clickBtn2() {
    // 戻す
    d2.style.display = "none";
    d1.style.display = "block";
}

function clickBtn3() {
    // 選択に変える
    d3.style.display = "none";
    d4.style.display = "block";
}

function clickBtn4() {
    // 戻す
    d4.style.display = "none";
    d3.style.display = "block";
}



