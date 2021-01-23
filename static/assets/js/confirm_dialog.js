//FIXME
// 1. implement loader
// 2. show message with animate and then hide dialog
// 3. take action like remove whole row of action link/button

function init_confirm_dialog(){

    $('#confirm-delete').on('click', '.btn-ok', function(e) {

    var $modalDiv = $(e.delegateTarget);

    $modalDiv.addClass('loading');

    var url = $(this).data('href');
    var token = $("[name=csrfmiddlewaretoken]").val();

    $.post( url, {'csrfmiddlewaretoken': token}, function(data) {

            //alert(data.filename + data.mode);
            //$(".spinner").addClass("invisible");


            if(data.error)
            {
                $("#confirm-modal-message").text(data.error);

                return;
            }

            $("#confirm-modal-message").text(data.message);
            //FIXME remove column of table

            $modalDiv.modal('hide').removeClass('loading');
            location.reload();

        },'json' // I expect a JSON response
    );


    });

    // Bind to modal opening to set necessary data properties to be used to make request
    $('#confirm-delete').on('show.bs.modal', function(e) {
//      var data = $(e.relatedTarget).data();
//      $('.title', this).text(data.recordTitle);
//      $('.btn-ok', this).data('id', data.recordId);

      $(this).find('.btn-ok').attr('data-href', $(e.relatedTarget).data('href'));

    });

}