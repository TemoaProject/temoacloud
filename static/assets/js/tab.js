$(".nav-tabs")

    .on("click", "a", function (e)
    {
        e.preventDefault();
        if (!$(this).hasClass('add-contact')) {
            $(this).tab('show');
        }
    })

    .on("click", "span", function ()
    {
        var anchor = $(this).siblings('a');
        $(anchor.attr('href')).remove();
        $(this).parent().parent().children('li').first().children('a').click();
        $(this).parent().remove();
        //$(".nav-tabs li").children('a').first().click();
    });
