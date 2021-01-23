/*function populateFileList(mode, project_uid, account_id){
    var url = '/project/files/get-file-list/' + project_uid;
    $.ajax({
        url: url,
        dataType: 'json',
        method: 'get',
        success: function(result) {


            var options = '<option value="0">--Select data File--</option>';
            file_list = JSON.parse(result);

            $.each(file_list, function(index, obj) {

                options += '<option value="' + obj.fields.uid + '">' + obj.fields.name + '</option>';
            });

            $("#datafilename").html(options);
            $("#db-plot-datafilename").html(options);
        }
    });
}*/

function addTab(tabcontent)
{

    var id = $("#graphviz-tabs").children().length + 1; //think about it ;)


    var tabId = 'result_' + id;

    $("#graphviz-tabs").append('<li><a class="nav-link" href="#result_' + id + '">Output ' + id +'</a><span>x</span></li>');

    $('#graphviz-content')
    .append('<div class="tab-pane" id="' + tabId + '"> ' + tabcontent + '</div>');

    $('#graphviz-tabs li:nth-child(' + id + ') a').click();

}

function displayNetworkDiagram(mode_folder, image_filename, result_url) {

    //file is inside result/ folder but due to static django we have to say url /static :(  ..enjoy :)
    var imgPath = result_url + mode_folder + "/" + image_filename + "?" + new Date().getTime();

    var tabcontent = '<iframe class="result-frame" src="' + imgPath + '" width="1600" height="800" alt="Output"></iframe> ';

    addTab(tabcontent);





    //$('#networkDiagram').html('<iframe class="result-frame" src="' + imgPath + '" width="800" alt="Output"></iframe> ');
}


function initForm(mode, project_uid, scenario_uid, result_url, data_file_name) {

    $('#commodity-technology-value').hide();
    $('#commodity-label').hide();
    $("#commodity-value-error").hide();
    $(".date-range").hide();


    $("#commodity-file-error").hide();
    $("#input-file-error").hide();
    $("#scenario-name-error").hide();
    $("#date-range-error").hide();

    var url = '/project/input-data/run-input/' + project_uid + '/' + scenario_uid;



    $("#input-form").submit(function(e) {


        e.preventDefault();

        $("#commodity-value-error").hide();

        /*var fileInput = $("#datafilename option:selected").text();
        if (fileInput == '--Select data File--' || fileInput == '')
        {
            $("#input-file-error").show();
            return false;
        }
        else
        {
            $("#input-file-error").hide();
        }*/


        type = $('#commodity-technology-type').val();

        if(type != 'none')
        {
           filename = $("#commodity-technology-type").val();

            if(filename == '')
            {
                //alert("Select model first");
                $("#commodity-value-error").show();
                return;
            }
        }

        $(".spinner").removeClass("invisible");


        $.post( url, $('form#input-form').serialize(), function(data) {

            //alert(data.filename + data.mode);
            $(".spinner").addClass("invisible");

            if(data.error)
            {
            PNotify.error({
                        text: data.error,
                    });
                return;
            }
            if(data.success) {
            PNotify.success({text:data.success})}


            displayNetworkDiagram(data.mode, data.filename, result_url );

            //Make download button ready
            $("#download-button").addClass("btn-yellow").attr("href", result_url + data.zip_path);

        },
       'json' // I expect a JSON response
    );
});
}

function showHideCommodityTechnology(mode, project_uid, data_file_name){

    $('#commodity-technology-type').change(function(){

        type = $('#commodity-technology-type').val();

        if(type == 'none')
        {
            $('#commodity-technology-value').hide();
            $('#commodity-label').hide();
        }
        else
        {

            filename = $("#datafilename").val();

            if(filename == 0)
            {
                $("#commodity-file-error").show();
                return;
            }

            $('#commodity-technology-value').show();
            $('#commodity-label').html("Select "+type+" value");
            $('#commodity-label').show();


            getCTList(mode, type, filename, project_uid);
        }
    });
}

function getCTList(mode, type, filename, project_uid){
    var url = '/project/files/get-ct-list/' + project_uid;


    $.ajax({
        url: url,
        dataType: 'json',
        data: {
            mode: mode,
            filename: filename,
            type: type
        },
        success: function(result) {
            if(result.error)
            {
                alert(result.error)
                return;
            }


            var options = '<option value="0">--Select '+ type +' value--</option>';
            $.each(result.data, function(index, obj) {
                options += "<option value=" + obj + ">" + obj + "</option>";
            });


            $("#commodity-technology-value").html(options);

        }
    });
}

function showDownloadButtonWithHelp()
{
    $("#download-db").removeClass('hidden');
    $("#download-button-help").removeClass('hidden');
}

function initJs(mode, project_uid, account_id, scenario_uid, result_url, data_file_name)
{
    initForm(mode, project_uid, scenario_uid, result_url, data_file_name);

   /* populateFileList(mode, project_uid, account_id);*/

    showHideCommodityTechnology(mode, project_uid, data_file_name);

    /*$('#datafilename').change(function(){

        $('#commodity-technology-value').hide();
        $('#commodity-label').hide();

        $("#commodity-technology-type").val("none");
        $('#commodity-technology-value').html("");

        $("#commodity-file-error").hide();
        $("#input-file-error").hide();

    });*/

}

$(document).ready(function(){
    $('[data-rel="popover"]').popover();
});




