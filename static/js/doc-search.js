$(document).ready(function() {

    $('input[class=search-bar]').tooltip({
        placement: "top",
        trigger: "hover"
    });

    $('input[class=search-bar]').keypress(function(e){
      if ( e.which == 13  ) return false;
    });

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
            $(_filter2).appendTo('.search-box');
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
            $(_filter3).appendTo('.search-box');
          }
        });
      }
      else
      {
        if($('.filter3box'))
        { $('.filter3box').remove();  }
      }
    });

    $( ".search-bar" ).autocomplete({
		     source: function(request, response) {
		      $.ajax({
		          url: "/fms/document/search/",
		          data: { q: $(".search-bar").val(), filter1: $(".filter1").val(), filter2: $(".filter2").val(), filter3: $(".filter3").val() },
		          dataType: "json",
		          type: "GET",
		          success: function(data){
                docs = data;
                if(docs.length != 0)
                {
                  response($.map(data, function(doc) {
                    return { 
                      label: doc.name,
                      value: doc.name,
                      id: doc.id,
                      doc_no: doc.doc_no,
                      address: doc.address,
                      cat_name: doc.cat.name,
                      subcat1_name: doc.subcat1.name,
                      subcat2_name: doc.subcat2.name,
                      _status: doc._status,
                      rack_name: doc.rack.name,
                      rack_type: doc.rack.type,
                      rack_image: doc.rack.image
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
          
          var _status = (ui.item._status == true) ? '<span style="color:green;"><b>YES<b></span>' : '<span style="color:red;"><b>No</b></span>';
          var _subcat1 = (ui.item.subcat1_name != undefined) ? ui.item.subcat1_name:"--";
          var _subcat2 = (ui.item.subcat2_name != undefined) ? ui.item.subcat2_name:"--";
          var _rack_name = (ui.item.rack_name != undefined) ? ui.item.rack_name:"--";
          var _rack_type = (ui.item.rack_type != undefined) ? ui.item.rack_type:"--";
          var p_ele = '<div class="doc-data">'+
                            '<legend class="item-legend">'+ ui.item.value +'</legend>'+
                            '<table class="entry-table table table-striped table-bordered table-condensed">'+
                            '<tr><td><h4>DOCUMENT DATA</h4></td></tr>'+
                            '<tr>'+
                            '<td>'+
                            '<div class="doc-table">'+
                            '<table class="table table-striped table-bordered table-condensed">'+
                              '<tr><td>Name: </td><td>'+ui.item.value+'</td></tr>'+
                              '<tr><td>Address: </td><td>'+ ui.item.address +'</td></tr>'+
                              '<tr><td>Category: </td><td>'+ ui.item.cat_name +'</td></tr>'+
                              '<tr><td>SubCategory-1: </td><td>'+ _subcat1 +'</td></tr>'+
                              '<tr><td>SubCategory-2: </td><td>'+ _subcat2 +'</td></tr>'+
                              '<tr><td>Rack: </td><td>'+ _rack_name +'</td></tr>'+
                              '<tr><td>Rack type: </td><td>'+ _rack_type +'</td></tr>'+
                              '<tr><td>Availability: </td><td>'+ _status +'</td></tr>'+
                          '</table>'+
                          '</div></td></tr>'+
                          '<tr><td><h4>LOCATION MAP</h4></td></tr>'+
                          '<tr><td><img class="location-map" src="/'+ ui.item.rack_image +'" alt="Document Location Image"/></td></tr></table>'+
                        '</div><br>';                 
        $('#main').html(p_ele);
        $(this).val('');
		  }
   });
});
