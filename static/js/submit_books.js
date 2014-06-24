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
                    id: user.id
                  }
                }));
		          } 
		        });
         },
		      selectFirst:true,
		      minLength:2,
		      select: function(event,ui) {
            $('#main').html('');
            var data = { issue_id: ui.item.id };
            $.get("/fms/get_book_issued_data/", data, function(res){
              console.log(res);
              
              var p_ele = '<div class="issue-data">'+
                            '<legend>Person Details</legend>'+
                            '<table class="table table-striped table-bordered table-condensed">'+
                              '<tr><td>Name: </td><td>'+res.pdata.person_name+'</td></tr>'+
                              '<tr><td>Email: </td><td>'+res.pdata.person_email+'</td></tr>'+
                              '<tr><td>Mobile No.: </td><td>'+res.pdata.person_mobile_no+'</td></tr>'+
                              '<tr><td>Issued Date: </td><td>'+res.pdata.issue_date+'</td></tr>'+
                              '<tr><td>Return Date: </td><td>'+res.pdata.return_date+'</td></tr>'+
                          '</table>'+
                        '</div><br>';                 
             $('#main').append(p_ele);
        
             var b_ele = '<div class="issued-books">'+
                          '<legend>Issued Books</legend>'+
                          '<form class="submit-form" action="#">'+
                          '<input type="hidden" name="issue_id" value="'+ res.pdata.issue_id +'"/>'+
                          '<table class="table table-striped table-bordered table-condensed">'+
                          '<tr><th>Name</th><th>ISBN No.</th><th>Author</th><th>Publisher</th><th>Status</th></tr>';
 
             
             var _bdata = res.bdata;
             if(_bdata.length == 0) {
               b_ele += '<tr><td colspan="5">No Issued Books Found</td></tr>';
             }
             for(var i=0; i<_bdata.length; i++)
             {
                b_ele += '<tr>'+
                  '<td>'+_bdata[i].name+'</td>'+
                  '<td>'+_bdata[i].isbn_number+'</td>'+
                  '<td>'+_bdata[i].author+'</td>'+
                  '<td>'+_bdata[i].publisher+'</td>'+
                  '<td><input type="checkbox" class="checkbox" name="book_'+_bdata[i].id+'"/></td>'+
                  '</tr>';
             }
             
             b_ele += '</table></form></div>';
             $('#main').append(b_ele);

             if(_bdata.length > 0) {
               var btn_ele = 
                '<div style="clear:both;"></div>'+
                '<div class="btn_box">'+
                  '<table class="table3">'+
                    '<tr>'+
                      '<td>'+
                        '<div id="btn1">'+
                          '<button class="submit-btn btn btn-primary"> Submit </button>'+
                        '</div>'+
                      '</td>'+
                      '<td>'+
                        '<div id="btn3">'+
                          '<buttoncontext class="btn"> Cancel </button>'+
                        '</div>'+
                      '</td>'+
                    '</tr>'+
                  '</table>'+
                '</div>';

               $('#main').append(btn_ele);
             }
             $(this).val('');

            });
		      }
		});

    $(document).on('click', '.submit-btn', function(){
      var sdata = $('.submit-form').serialize();
      $.get('/fms/submit-books/', sdata, function(res){
         console.log('submitted!');
         if(res=='ok')
          window.location.href = '/fms/submit-books/?page_msg=submission saved successfully';
      });
   });
});
