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
        $('.login-form').fadeToggle();
        $('#login-shade').fadeToggle();
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

    // Add or update a user vote in the database
    ////////////////////////////////////////////
    $('.user_vote').click(function() {

        // Get law-id
        var lawid = $(this).parent().attr('data-lawid');

        // Get whether user voted for or against
        var user_for = false;
        if($(this).hasClass('approve')) {
            user_for = true;
        }

        $.get('/representME/user_vote/', {law_id: lawid, vote: user_for}, function(data){
            // If we were successful during the process of adding user vote to database
            if(data == "True") {
                // Update the HTML accordingly
                // Here we have to update the number of votes
                if(user_for) {
                    // Update number of votes
                    var number = parseInt($('.user_vote.approve').text()) + 1;
                    $('.user_vote.approve').text(number);
                    // Update your-vote
                    $('.your-vote').addClass('yes');
                } else {
                    // Update number of votes
                    var number = parseInt($('.user_vote.against').text()) + 1;
                    $('.user_vote.against').text(number);
                    // Update your-vote
                    $('.your-vote').addClass('no');
                }

                // Display numbers
                $('.user_vote').addClass('number');
            }
        });

    });

    // Edit a comment
    ////////////////////////////////
    $('.edit-comment').click(function() {

        // Get the comment text
        var text = $(this).parent().parent().find('p').text();
        // Place the text to the textarea
        $('#comment_form textarea').val(text);
        // Change data-editid to the id of the comment
        // TODO: Don't forget to empty data-editid after adding a comment
        $('#comment_form').attr('data-editid','something');

    });


    // Add a comment to the database
    ////////////////////////////////
    $('input[name=send-comment]').click(function(e) {
        // Stop from default behaviour (sending a form using POST request)
        e.preventDefault();

        var text;
        text = $.trim($('#comment_form textarea').val());

        var law_id;
        law_id = $('#comment_form').attr('data-lawid');

        // If the comment is not empty
        if(text.length != 0) {

            // Post comment to the view and wait for the answer
            $.get('/representME/add_comment/', {text: text, law_id: law_id}, function(data){
                // If we were successful during the process of adding user vote to database
                if(data != "False") {

                    // If we're adding first comment
                    if($(".no-comments").length != 0) {
                        $(".no-comments").remove();
                    }

                    // Add the comment to the wrapper
                    $('#comments-wrapper').prepend('<div data-userid="" class="latest-law" style="display: none"><h3>Emil Cieslar &nbsp;&nbsp;<span>' + data + '</span> &nbsp;&nbsp;<span>Edit</span></h3><p>' + text + '</p></div><!-- .latest-law -->');
                    // After the HTML is added, display it nicely
                    $('#comments-wrapper .latest-law').fadeIn('slow');

                    // Increase commends number
                    $('#comments_number').text(parseInt($('#comments_number').text())+1);

                    // Clear the text in the commend text field
                    $('#comment_form textarea').val('');

                }
            });



        } else {
            alert("Empty comment.");
        }



    });

    // Set height for #login-shade at load of document (will be re-set on resize)
    $('#login-shade').height($(window).height());

    // Simple function to display login
    var displayLogin = function() {
        $('.login-form').fadeIn();
        $('#login-shade').fadeIn();
    }

    // Check whether we have to display login form
    // We will reuse this function in onhashchange as well
    var displayLogIn = function() {

        var hashValue = location.hash;
        if (hashValue == "#login") {
            displayLogin();
        } else if (hashValue == "#login-invalid") {
            displayLogin();
            $('.login-invalid').show();
        } else if (hashValue == "#login-disabled") {
            displayLogin();
            $('.login-disabled').show();
        }

    }

    // Check for displaying at document ready
    displayLogIn();

    $(window).on('hashchange', function() {
        displayLogIn();
    });


    // Whenever user clicks on #login-shade, it closes the login
    $('#login-shade').click(function() {
        $(this).fadeOut();
        $('.login-form').fadeOut();
    });

});