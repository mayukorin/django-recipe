$(document).ready(function() {
    // チェックボックスのクリックを無効化します。
    $('.image_box .disabled_checkbox').click(function() {
      return false;
    });
      
    // 画像がクリックされた時の処理です。
    $('img.thumbnail').on('click', function() {

      if (!$(this).is('.checked')) {
        // チェックが入っていない画像をクリックした場合、チェックを入れます。
        $(this).addClass('checked');
        $(this).siblings('input').prop('checked',true);
      } else {
        // チェックが入っている画像をクリックした場合、チェックを外します。
        $(this).removeClass('checked');
        $(this).siblings('input').prop('checked',false);
      }
    });
    $('img.thumbnail').on('reset', function() {
        //リセット時、checkクラスをoffにする
        $(this).removeClass('checked');
        $(this).siblings('input').prop('checked',false);
    });
    $('#clear').click(function(){
        $('img.thumbnail').removeClass('checked');
        $('input:checkbox[name="categories[]"]').prop('checked',false);
    });
    $('.recipe-click-area').click(function() {
      window.location.href = $(this).data('link');
    });
  });
  $(window).on('load',function(){
      $('input:checkbox[name="categories[]"]').prop('checked',false);
  
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



  