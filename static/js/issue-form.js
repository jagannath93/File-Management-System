$(document).ready(function() {
    $( "#person_name" ).autocomplete({
		     source: function(request, response) {
		      $.ajax({
		          url: "/fms/issued-person/search/",
		          data: { q: $("#person_name").val() },
		          dataType: "json",
		          type: "GET",
		          success: function(data){
                response($.map(data, function(user) {
                  return { 
                    label: user.group+": "+user.name,
                    value: user.name,
                    email: user.email,
                    mobile_no: user.mobile_no,
                    group: user.group,
                    issue_date: user.issue_date,
                    return_date: user.return_date,
                    id: user.id
                 }
                }));
		          } 
		        });
         },
		      selectFirst:true,
		      minLength:2,
		      select: function(event,ui) {
			      console.log(ui.item.group);
            $('#person_email').val(ui.item.email);
            $('#person_mobile_no').val(ui.item.mobile_no);
            $('#person_group').val(ui.item.group);
            $('#issue_date').val(ui.item.issue_date);
            $('#return_date').val(ui.item.return_date);
		      }
		});

    $( "#book-search" ).autocomplete({
		     source: function(request, response) {
		      $.ajax({
		          url: "/fms/books-search/",
		          data: { q: $("#book-search").val() },
		          dataType: "json",
		          type: "GET",
		          success: function(data){
                response($.map(data, function(book) {
                  if(book.status == true)
                    return { 
                      label: book.name+":   "+book.isbn+"       A",
                      value: book.name,
                      id: book.id,
                      status: book.status
                    }
                  else
                   return { 
                      label: book.name+":   "+book.isbn+"       NA",
                      value: book.name,
                      id: book.id,
                      status: book.status
                    }
                }));
		          } 
		        });
         },
		      selectFirst:true,
		      minLength:2,
		      select: function(event,ui) {

            if(ui.item.status == false) {
              alert("This book is unavailable now!");
              $(this).val(''); 
              return false;
            }

           var ele = "<tr><td><div class='book_box' id='book_box_"+ui.item.id+"'><div class='book'>"+ui.item.label+"</div></td><input type='hidden' name='books'value="+ui.item.id+" /><td><div class='cancel-btn'><img src='/static/images/cross.png'/></div></td></div></tr>";
           
           var entry = document.getElementById("book_box_"+ui.item.id);
           if(entry != undefined)
             alert("This book has already been added to the list!");
           else
           {
             $('#zero_items').hide();
			       $('#table2').append(ele);
           }
           $(this).val(''); return false;

		      }
	});
 
    $(document).on('click', '.cancel-btn', function(){
      $(this).parent().parent().remove();    
    });

    $('#btn1').click(function(){
      var form1_data = $('#form1').serialize();
      var form2_data = $('#form2').serialize();
      var data = form1_data +"&"+ form2_data;
      console.log(data);
      $.get("/fms/issue-books/", data, function(res){
        console.log("Done."); 
        window.location.href = '/fms/issue-books/';
      });
    });
  });
