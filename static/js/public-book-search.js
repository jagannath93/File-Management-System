$(document).ready(function() {
    var books = new Array();

    $('input[class=search-bar]').tooltip({
        placement: "top",
        trigger: "hover"
    });

    $('input[class=search-bar]').keypress(function(e){
      if ( e.which == 13  ) return false;
    });

    $( ".search-bar" ).autocomplete({
		     source: function(request, response) {
		      $.ajax({
		          url: "/fms/public/book-search/",
		          data: { q: $(".search-bar").val(), filter1: $(".filter1").val(), filter2: $(".filter2").val() },
		          dataType: "json",
		          type: "GET",
		          success: function(data){
                books = data;
                if(books.length != 0)
                {
                  response($.map(data, function(book) {
                    return { 
                      label: book.name+": "+book.isbn,
                      value: book.name,
                      id: book.id
                    }
                  }));
                }
                else {
                  $('#main').html('<b>No Items Found.</b>');
                }
		          } 
		        });
         },
		      selectFirst:true,
		      minLength:2,
		      select: function(event,ui) {
           $.ajax({
		          url: "/fms/book-search/book-data/",
		          data: { book_id: ui.item.id },
		          dataType: "json",
		          type: "GET",
              success: function(data){

              var book = data.bdata;
              console.log(book);
              var _address = book.address;
              var _status = (book.status == true) ? '<span style="color:green;"><b>YES<b></span>' : '<span style="color:red;"><b>No</b></span>';
              var _isbn = (book.isbn != 'None') ? book.isbn:"--";
              var _publisher = book.publisher ? book.publisher:"--";
              var _author = book.author ? book.author:"--";
              
              var p_ele = '<div class="book-data">'+
                            '<legend>'+ book.name +'</legend>'+
                            '<table class="entry-table table table-striped table-bordered table-condensed">'+
                              '<tr><td>'+
                            '<div class="book-image">'+
                              '<img src="/'+ book.image +'" alt="cover-image"/>'+
                            '</div>'+
                            '</td>'+
                            '<td>'+
                            '<div class="book-table">'+
                            '<table class="table table-striped table-bordered table-condensed">'+
                              '<tr><td>Name: </td><td>'+book.name+'</td></tr>'+
                              '<tr><td>Number: </td><td>'+ book.code +'</td></tr>'+
                              '<tr><td>Category: </td><td>'+ book.categories +'</td></tr>'+
                              '<tr><td>ISBN Number: </td><td>'+ _isbn +'</td></tr>'+
                              '<tr><td>Publisher: </td><td>'+ _publisher +'</td></tr>'+
                              '<tr><td>Author: </td><td>'+ _author +'</td></tr>'+
                              '<tr><td>Address: </td><td>'+ book.code+' / '+_address +'</td></tr>'+
                              '<tr><td>Availability: </td><td>'+ _status +'</td></tr>'+
                          '</table>'+
                          '</div></td></tr></table>'+
                        '</div><br>';                 
              $('#main').html(p_ele);
           }
        });

        $(this).val('');
		  }

   });
});
