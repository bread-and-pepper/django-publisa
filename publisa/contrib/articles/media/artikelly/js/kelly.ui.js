$(document).ready(function(){
    $('select#id_inline_content_type').change(function(){
        if($(this).val()){
            var url = $('.response').attr("rel").replace('0', $(this).val());
            $('.response').load(url, function(){
                activateInline();
            });
        } else {
            $('.response').empty();
        }
    });

    if($('.thumb').length > 0){
        $('.thumb').fancybox();
    }
});

function dismissAddAnotherPopup(win){
    win.close();
    var value = $('#id_inline_content_type :selected').val();
    var url = $('.response').attr("rel").replace('0', value);
    $('.response').load(url, function(){
        activateInline();
    });
}

function activateInline(){
    $('.response').find('*[rel]').each(function(index){
        $(this).parent().click(function(){
            var rel = $(this).find('img').attr("rel").split("-");
            var class_selected = $('#id_inline_content_class :selected').text();
            var inline = '@[inline type='+rel[0]+' id='+rel[1]+' class='+class_selected+']';
            var dest = $('#id_inline_content_dest :selected').val();

            $('#'+ dest).val(inline + '\n\n' + $('#'+ dest).val());
            $('#'+ dest).focus();

            $('a[title=Preview]').trigger('mouseup');
        });
    });
}
