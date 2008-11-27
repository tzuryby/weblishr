var editMode = /\/edit\//.test(document.location.pathname);
var addMode = !editMode;

// wait for the DOM to be loaded 
jQuery(document).ready(function() { 
    // Make the form Ajax-Submit
    jQuery('#form').submit(function() { 
        jQuery('#content').val(jQuery.wymeditors(0).html());
        // submit the form 
        document.forms[0].submit();
        return false;
    });    
    
    // Load data
    if (editMode){
        new_path = (document.location.pathname).replace('/edit/', '/ajax/');
        jQuery.getJSON(new_path, function(data){
            for (item in data){
                jQuery('#' + item).val(data[item]);
                item === 'content' && jQuery('#content').wymeditor({ logoHtml: '', html: data[item]});
            }
        jQuery("#url").attr("disabled", "disabled");
    });
        
    }
    // Load WYMEditor
    else if (addMode){
        jQuery('#content').wymeditor({                           
            logoHtml: '', 
            html: window.client_params.init_wym_editor
            });
        
        //Bind blur event so: title -> [filter] -> url       
        jQuery("#title").blur(function () {
            jQuery('#url').val(jQuery(this).val().replace(/\W/g, '-').toLowerCase())
        });        
    }
});
