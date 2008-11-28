var editMode = /\/edit\//.test(document.location.pathname);
var addMode = !editMode;

// wait for the DOM to be loaded 
$(document).ready(function() { 
    // Make the form Ajax-Submit
    $('#form').submit(function() { 
        $('#content').val($.wymeditors(0).html());
        //$('#key_name').val($('#url').val());
        // submit the form 
        document.forms[0].submit();
        return false;
    });    
    
    // Load data
    if (editMode){
        new_path = (document.location.pathname).replace('/edit/', '/ajax/');
        $.getJSON(new_path, function(data){
            for (item in data){
                $('#' + item).val(data[item]);
                item === 'content' && $('#content').wymeditor({ logoHtml: '', html: data[item]});
            }
        $('#delete').attr('href', document.location.pathname.replace('/edit/', '/delete/'));
    });
        
    }
    // Load WYMEditor
    else if (addMode){
        $('#content').wymeditor({                           
            logoHtml: '', 
            html: window.client_params.init_wym_editor
            });
        
        //Bind blur event so: title -> [filter] -> url       
        $("#title").blur(function () {
            $('#url').val($(this).val().replace(/\W/g, '-').replace(/-+/g, '-').toLowerCase())
        });        
    }
});
