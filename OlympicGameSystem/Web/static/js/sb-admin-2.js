$(function() {

    $('#side-menu').metisMenu();

});

//Loads the correct sidebar on window load,
//collapses the sidebar on window resize.
// Sets the min-height of #page-wrapper to window size
$(function() {
    $(window).bind("load resize", function() {
        topOffset = 50;
        width = (this.window.innerWidth > 0) ? this.window.innerWidth : this.screen.width;
        if (width < 768) {
            $('div.navbar-collapse').addClass('collapse');
            topOffset = 100; // 2-row-menu
        } else {
            $('div.navbar-collapse').removeClass('collapse');
        }

        height = ((this.window.innerHeight > 0) ? this.window.innerHeight : this.screen.height) - 1;
        height = height - topOffset;
        if (height < 1) height = 1;
        if (height > topOffset) {
            $("#page-wrapper").css("min-height", (height) + "px");
        }
    });

    var url = window.location;
    var element = $('ul.nav a').filter(function() {
        return this.href == url || url.href.indexOf(this.href) == 0;
    }).addClass('active').parent().parent().addClass('in').parent();
    if (element.is('li')) {
        element.addClass('active');
    }
});
$(document).ready(function()
{
    $("#mydropdown").change(function()
    {
        target = $(this).val();
        if(target != 'none')
        {
            $(".table").hide();
            $("#" + target).show();
        }
        return false;
    });
});
$(document).ready(function()
{
    $("#category_select").change(function()
    {
        target = $(this).val();
        if(target == 'tian')
        {
            $(".J" ).hide();
            $(".A").hide();
            $(".T" ).show();
        }
        else if (target == "jing")
        {
            $(".T").hide();
            $(".A").hide();
            $(".J" ).show();
        }
        else
        {
            $(".T").hide();
            $(".J").hide();
            $(".A").show();
            
        }
        return false;
    });
});
$(document).ready(function()
{
    $("#event_select").change(function()
    {
        target = $(this).val();
        $(".c_athlete").hide();
        $("." + target).show();
        return false;
    });
});

$(document).ready(function()
{
    $("#select_major_judge").change(function()
    {
        target = $(this).val();
        $(".alljudge").show();
        $("#" + target).hide();
        return false;
    });
});

$(document).ready(function() {
    $(".clickable-row").click(function() {
        window.document.location = $(this).data("href");
    });
});


