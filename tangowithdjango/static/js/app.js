$(document).ready(function() {

    // Reset or set actions on resize
    $(window).resize(function() {

        // Remove style from menu and .login-form
        $('.header .menu, .login-form').removeAttr('style');

        // Set height each time user resizes the window
        $('.msp-wrap .vote').height($('.msp-wrap').height()-$('.msp-wrap h6').outerHeight());

    });

    // Show and hide menu
    $('.header .menu-icon').click(function() {
        $('.header .menu').toggle();
    });

    // Show and hide log in form
    $('.login-link').click(function() {
        $('.login-form').toggle();
    })

    // Set height for .msp-wrap .vote (it's absolutely positioned
    $('.msp-wrap .vote').height($('.msp-wrap').height()-$('.msp-wrap h6').height());

    // Make a tr in a laws list a link
    $('.laws-table tr').click(function() {
        if($(this).data('href') !== undefined)
        {
            document.location = $(this).data('href');
        }
    });

    // Add a comment to the database
    $('input[name=send-comment]').click(function(e) {
        // Stop from default behaviour (sending a form using POST request)
        e.preventDefault();

        var text;
        text = $.trim($(this).parent().find('textarea').val());

        // If the comment is not empty
        if(text.length != 0) {

            // If we're adding first comment
            if($(".no-comments").length != 0) {
                $(".no-comments").remove();
            }

            // Add the comment to the wrapper
            $('#comments-wrapper').prepend('<div class="latest-law" style="display: none"><h3>Emil Cieslar &nbsp;&nbsp;<span>Datum a cas</span></h3><p>' + text + '</p></div><!-- .latest-law -->');
            // After the HTML is added, display it nicely
            $('#comments-wrapper .latest-law').fadeIn('slow');

        } else {
            alert("Empty comment.");
        }

    /*$.get('/rango/add_comment/', {text: text}, function(data){
               $('#like_count').html(data);
               $('#likes').hide();
    });*/

    });

});