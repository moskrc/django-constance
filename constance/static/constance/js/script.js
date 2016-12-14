django.jQuery(document).ready(function(){

    var $ = django.jQuery;

    var options = {
        mode: 'code',
        search: false,
    }

    var json_editors = [];

    $('.json').each(function(){
        var id = $(this).attr('id');
        var data = $(this).text();
        var container = $('<div class="json-editor-area">').insertAfter($(this)).css('width','100%').css('height','300px');
        var editor = new JSONEditor(container[0], options);
        editor.set($.parseJSON(data));
        editor.elem = $(this);
        $(this).hide();
        json_editors.push(editor);
    });


    $('form').on('submit', function () {
        for (var e in json_editors) {
            var editor = json_editors[e];
            editor.elem.text(JSON.stringify(editor.get()));
        }
    })

});


