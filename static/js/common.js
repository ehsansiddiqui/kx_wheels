$(function() {
    $("a[href] img[src]").each(function(){
        if( this.protocol === "http:")
            this.protocol = "https:"
    });
    $("a.select_vehicle").live("click", function() {
        var that = this;
        $.ajax({
            url: $(this).attr("href"),
            success: function(data) {
                $(that).parent().parent().html("<li>"+data+"</li>");
            }
        });
        return false;
    });
});

check_status = '';
function countChar(val) {                       // to count the number of characters in search field //
    check_statuss = '';
    check_statuss = check_status;
    var len = val.value.length;
    if(len > 3){
        if(check_statuss == 'Fail'){
            return false;
        }
        else{
            $( "#searchbtn" ).trigger( "click" );
            len = 0;
        }
    }
    };

function getfocus() {
    $("#search_value").focus();
}

  $('#search_value').click(function(){                    // to show search popUP when we click in search bar box//
     $('#search_value').prop( "disabled", true );

     $('#loginScreen').fadeIn();
     $("body").find('#searchresult').focus();
    $('#cover').show();
  });
  $('#search_value').click(function(){
    setTimeout(function(){
    $('.login-area').addClass( "loginscreen" );
    }, 100);
  });


   $('#search_logo').click(function(){                    // to show search popUP when we click in search bar box//
     $('#search_value').prop( "disabled", true );
     $('#loginScreen').fadeIn();
     $("body").find('#searchresult').focus();
    $('#cover').show();
  });
  $('#search_logo').click(function(){
    setTimeout(function(){
    $('.login-area').addClass( "loginscreen" );
    }, 100);
  });


  $('#cancel').click(function(){
     $('#search_value').prop( "disabled", false );
     $('#loginScreen').hide();
     $('#searchresult').val('');
     $('#cover').hide();
     $('#hide_popup').empty();
     $('#hide_popup1').empty();
  });


  $('form input').on('keyup', function(e) {          // to check either enter is press or not when we go for search //
   if(e.keyCode == 08 ){
    if(this.value.length <=3){
        check_status = 'true';
    }
    if(this.value.length == 2){
         $('#hide_popup').empty();
         $('#hide_popup1').empty();
    }
   }
    if(this.value.length <= 3 && this.value.length > 0){
        if(e.which == 13) {
        e.preventDefault();
        $( "#searchbtn" ).trigger( "click" );
    }
    }

});

$('body').keyup(function(e) {                     // to disappear search result on ESC key press //
     if (e.keyCode == 27) {
        $('#hide_popup').empty();
        $('#hide_popup1').empty();
    }
     $('.close').click(function() {                     // to disappear search result on ESC key press //
     $('#hide_popup').empty();
     $('#hide_popup1').empty();
    });
});

// function to send ajax and show data response //

     $('#searchbtn').click(function(){
           if($("#searchresult").val().length === 0)
           {
                alert('Please enter value to search!');
                return false;
           }
           $('#hide_popup').empty();
           $('#hide_popup1').empty();
           $("#hide_popup").append(" <div class='popuptext' id='myPopup'><a id = 'close' ><img src='/static/img/close.png' class='close' /></a><div><h1> Wheels: </h1><ul class='sub-menu' id='search_list'> </ul><h1> Tires: </h1> <ul class='sub-menu' id='search_list1'> </ul> <h1> Brands: </h1> <ul class='sub-menu' id='brands'> </ul></div> " );

           $('#hide_popup').removeClass('hide');
           var val = $("#searchresult").val();
           var token = $('#token').val();
           var data= {"val":val , "csrfmiddlewaretoken": token};
           $.ajax({
               type:"POST",
               url:$("#quick_searchh").attr('action'),
               data:data,
               success:function(response) {
                    $("#myPopup").find('ul').empty();
                    $('#hide_popup1').empty();
                    $('#sucesdata').removeClass('hide');
                    if(response.status == 'Fail'){
                        $("#hide_popup1").append(" <div class='popuptextt' id='myPopup1'><a id = 'close' ></a><p class='product-found'> No Product Found. </p></div> " );
                        $('#hide_popup1').removeClass('hide');
                        var popup = document.getElementById("myPopup1");
                        popup.classList.toggle("show");
//                        alert('No record found');
                         check_status = response.status;
                        return false;
                    }
                    else{
                    check_status = 'True';
                    var check_array = [];
                    $('#hide_popup').removeClass('hide');
                     var w_count= 0;
                     var wheel_count= 0;
                     var tire_count = 0;
                     var t_count = 0;
                    for(var i=0; i<(response.length-1); i=i+9){
                    var brand_name = response[i+4];
                    var a = check_array.indexOf(brand_name);
                     if(a < 0 ){
                        check_array[i] = brand_name;
                     }
                    var rajax = response[i+7];
                    var check = rajax.split('/');
                    if($.trim(check[1]) == 'wheels'){
                        $("#search_list").append("<li><a href= 'http://127.0.0.1:8000/kx/wheel/" + $.trim(response[i+6])+ "/"+ $.trim(response[i+3])+"/'><img src = '"+ response[i+2]+ " '/> <p>" + response[i+1]+"</p><span><p>from:</p> $" +response[i + 8] + "</span></a></li> ");
                        wheel_count = wheel_count + 1;
                        if(check_array[i] != null && w_count < 4){
                        w_count = w_count + 1;
                        $("#brands").append("<li><a id='brand_value' href= 'http://127.0.0.1:8000/kx/wheel/"+$.trim(response[i+6])+"/'><img src='"+response[i+5]+  "'/><p>"+ check_array[i]+ "</p></a></li>");
                        }
                    }
                    else{
                        $("#search_list1").append("<li><a href= 'http://127.0.0.1:8000/kx/tire/" + $.trim(response[i+6])+ "/"+ $.trim(response[i+3])+"/'><img src = '"+ response[i+2]+ " '/> <p>" + response[i+1]+"</p><span><p>from:</p> $" +response[i + 8] + "</span></a></li> ");
                        tire_count = tire_count + 1;
                        if(check_array[i] != null && t_count < 4){
                        t_count = t_count + 1;
                        $("#brands").append("<li><a id='brand_value' href= 'http://127.0.0.1:8000/kx/tire/"+$.trim(response[i+6])+"/'><img src='"+response[i+5]+  "'/><p>"+ check_array[i]+ "</p> </a></li> ");
                        }
                    }
                    }
                    if(tire_count == 0){
                         $("#search_list1").append("<p class='product-found'> No Product Found. </p>");
                    }
                    if(wheel_count == 0){
                         $("#search_list").append("<p class='product-found'> No Product Found. </p>");
                    }
                      var popup = document.getElementById("myPopup");
                    popup.classList.toggle("show");
               }
            }
            });
     });
