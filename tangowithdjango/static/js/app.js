$(document).ready(function() {

    // Reset or set actions on resize
    $(window).resize(function() {

        // Remove style from menu, .login-form, #login-shade
        $('.header .menu, .login-form, #login-shade').removeAttr('style');

        // Set height each time user resizes the window
        $('.msp-wrap .vote').height($('.msp-wrap').height()-$('.msp-wrap h6').outerHeight());

        // Set height for #login-shade at load of document
        $('#login-shade').height($(window).height());

    });

    // Show and hide menu
    $('.header .menu-icon').click(function() {
        $('.header .menu').toggle();
    });

    // Show and hide log in form
    $('.login-link').click(function() {
        $('.login-form').toggle();
        $('#login-shade').toggle();
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
        text = $.trim($('#comment_form textarea').val());

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

            // Increase commends number
            $('#comments_number').text(parseInt($('#comments_number').text())+1);

            // Clear the text in the commend text field
            $('#comment_form textarea').val('');

        } else {
            alert("Empty comment.");
        }

    /*$.get('/rango/add_comment/', {text: text}, function(data){
               $('#like_count').html(data);
               $('#likes').hide();
    });*/

    });

    // Set height for #login-shade at load of document (will be re-set on resize)
    $('#login-shade').height($(window).height());

    // Check whether we have to display login form
    var hashValue = location.hash;
    if(hashValue == "#login") {
        $('.login-form').fadeIn();
        $('#login-shade').fadeIn();
    }

    // Whenever user clicks on #login-shade, it closes the login
    $('#login-shade').click(function() {
        $(this).hide();
        $('.login-form').hide();
    });

});