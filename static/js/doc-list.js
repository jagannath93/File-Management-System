$(document).ready(function() {
    $(".filter1").on("change", function(){
      if(!($(this).val() == ''))
      {
        var cat_data = {cat: $(this).val()};
        $.get('/fms/get_sc1/', cat_data, function(res){
          if(res.length)
          {
            var _filter2 = '<td class="filter2box"><select class="filter2">'+
                            '<option value="">SubCategory-1</option>';
            for(var i=0; i<res.length; i++)
            {
              _filter2 += '<option value="'+res[i].code+'">'+res[i].name+'</option>';
            }  
            _filter2 += '</select></td>';

            if($('.filter2box'))
            { $('.filter2box').remove(); }
            if($('.filter3box'))
            { $('.filter3box').remove(); }
            $(_filter2).appendTo('.filter-box');
          }
        });
      }
      else
      {
        if($('.filter2box'))
        { $('.filter2box').remove();  }
        if($('.filter3box'))
        { $('.filter3box').remove();  }
      }
    });

    $(document).on("change", ".filter2", function(){
      if(!($(this).val() == ''))
      {
        var cat_data = {cat: $('.filter1').val(), subcat1: $(this).val()};
        $.get('/fms/get_sc2/', cat_data, function(res){
          if(res.length)
          {
            var _filter3 = '<td class="filter3box"><select class="filter3">'+
                            '<option value="">SubCategory-2</option>';
            for(var i=0; i<res.length; i++)
            {
              _filter3 += '<option value="'+res[i].code+'">'+res[i].name+'</option>';
            }  
            _filter3 += '</select></td>';

            if($('.filter3box'))
            { $('.filter3box').remove(); }
            $(_filter3).appendTo('.filter-box');
          }
        });
      }
      else
      {
        if($('.filter3box'))
        { $('.filter3box').remove();  }
      }
    });

    /* ON BUTTON CLICK */
    $('.get_list_btn').click(function(){
      var filter_data = { filter1: $(".filter1").val(), filter2: $(".filter2").val(), filter3: $(".filter3").val() };
      $.get('/fms/document/list/', filter_data, function(res){
         var ele = '';
         for(var i=0; i<res.length; i++)
         {
           ele += '<div class="doc-data">'+
                              '<legend>'+ res[i].name +'</legend>'+
                              '<table class="entry-table table table-striped table-bordered table-condensed">'+
                              '<tr>'+
                              '<td>'+
                              '<div class="doc-table">'+
                              '<table class="table table-striped table-bordered table-condensed">'+
                                '<tr><td>Name: </td><td>'+ res[i].name +'</td></tr>'+
                                '<tr><td>Address: </td><td>'+ res[i].address +'</td></tr>'+
                                '<tr><td>Category: </td><td>'+ res[i].cat.name +'</td></tr>'+
                                '<tr><td>SubCategory-1: </td><td>'+ res[i].subcat1.name +'</td></tr>'+
                                '<tr><td>SubCategory-2: </td><td>'+ res[i].subcat2.name +'</td></tr>'+
                                '<tr><td>Rack: </td><td>'+ res[i].rack.rack_name +'</td></tr>'+
                                '<tr><td>Rack type: </td><td>'+ res[i].rack.type +'</td></tr>'+
                                '<tr><td>Availability: </td><td>'+ res[i]._status +'</td></tr>'+
                            '</table>'+
                            '</div></td></tr></table>'+
                          '</div><br>';                 

         }
         $('#main').html(ele);
      })    
    }); 
  });
