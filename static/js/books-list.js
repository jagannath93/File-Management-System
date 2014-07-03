$(document).ready(function() {
    $(".cat-filter").change(function(){

      $(this).popover({ title: 'Loading Data.....  Please Wait', html:true});
      var data = { cat: $(this).val() };
      $.get('/fms/book-list/', data, function(res){
        $('.cat-filter').popover('hide');

        var books = res.bdata;
        if(books.length == 0)
        { $('#main').html('<span><b>No Books Found.</b></span>'); }  
        else
        {
          var ele = '';
          for(var i=0; i<books.length; i++)
          {
            var book = books[i];
            var _address = book.address;
            var _status = (book.status == true) ? '<span style="color:green;"><b>YES<b></span>' : '<span style="color:red;"><b>No</b></span>';
            var _isbn = (book.isbn != 'None') ? book.isbn:"--";
            var _publisher = book.publisher ? book.publisher:"--";
            var _author = book.author ? book.author:"--";
            ele += '<div class="book-data">'+
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
          }
          $('#main').html(ele);
        } 
      });
    });
  });
