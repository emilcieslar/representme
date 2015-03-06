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

});