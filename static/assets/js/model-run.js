/* function populateFileList(str, project_id, account_id) {
     var url = '/project/files/get-file-list/' + project_id;
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

            $("#"+str+"datafilename").html(options);

            if( $("#"+str+"datafilename").val() != 0){
                showDownloadButtonWithHelp(true, str, $("#"+str+"datafilename").val());
            }
        }
    });
}*/


/* function initDropZone(str){
    // Dropzone class:
    var myDropzone = new Dropzone("div#"+str+"dropArea", {
        url: "/fileupload",
        params: {
        mode: str
    }
    });

    myDropzone.on('sending', function(file, xhr, formData){

            if (str == "input"){
                formData.append('isOverwrite', $("#isInputOverwrite").is(':checked') ? 1 : 0 );
            }
            else if (str == "output")
            {
                formData.append('isOverwrite', $("#isOutputOverwrite").is(':checked') ? 1 : 0 );
            }
    });


    myDropzone.on("success", function(fileList, response)
    {

        var options = '<option value="0">--Select data File--</option>';
        var mode = response.mode
        $.each(response.data, function(index, obj) {
            options += fileList.name == obj ? "<option selected='selected' value=" + obj + ">" + obj + "</option>" :
                "<option value=" + obj + ">" + obj + "</option>";
        });

        //$("#"+str+"datafilename").html(options);

        //Update output in all cases
        if (mode == "output"){
          $("#outputdatafilename").html(options);
          console.log(options)
        }
        else if (mode == "input") {
          $("#inputdatafilename").html(options);
        }

        showDownloadButtonWithHelp(true, str, fileList.name);

        outputBlank(false);

        myDropzone.removeAllFiles();

    });

   }*/

function initJs(mode, project_id, account_id, scenario_uid)
{
    //populateFileList('input', project_id, account_id);
    //populateFileList('output', project_id, account_id);
    //initDropZone('input');
    //initDropZone('output');

    initForm(project_id, scenario_uid);

    $("input[name='runoption']").click(function() {

       //alert("clicked");

        selected_val =  $(this).val() ;
        //alert(selected_val)

        if( selected_val == "Single-Run")
        {
            $(".UncertaintyAnalysisOptions, .MGAConfiguration").addClass("hidden");
            //alert("hide")
        }
        else if (selected_val == "Uncertainty-Analysis")
        {
            $(".UncertaintyAnalysisOptions, .MGAConfiguration").removeClass("hidden");
            //alert("show")
        }



   });



}





function outputBlank(isBlank)
{

    if(isBlank)
    {
        $("input[name='createspreadsheetoption']").prop("disabled", true);
        $("input[name='createspreadsheetoption'][value='']").prop("checked",true);
        $("input[name='createtextfileoption']").prop("disabled", true);
        $("input[name='createtextfileoption'][value='yes']").prop("checked",true);
    }
    else
    {
        $("input[name='createspreadsheetoption']").prop("disabled", false);
        $("input[name='createspreadsheetoption'][value='yes']").prop("checked",true);
        $("input[name='createtextfileoption']").prop("disabled", false);
        $("input[name='createtextfileoption'][value='yes']").prop("checked",true);
    }


}

function initForm(project_id, scenario_uid) {


    outputBlank(false);
    showDownloadButtonWithHelp(false, 'output');
    showDownloadButtonWithHelp(false, 'input');

   /* $("#outputdatafilename").change(function(){

        if($(this).val() == 0 )
        {
            outputBlank(true);
            showDownloadButtonWithHelp(false, 'output', '');
        }
        else
        {
            if ($("#inputdatafilename").val() == 0){
                outputBlank(true);
            }
            else {
                outputBlank(false);
            }
            showDownloadButtonWithHelp(true, 'output', $(this).val());
        }

    });


    $("#inputdatafilename").change(function(){

        if($(this).val() == 0 )
        {
            outputBlank(true);
            showDownloadButtonWithHelp(false, 'input', '');
        }
        else
        {
            if ($("#outputdatafilename").val() != 0) {
                outputBlank(false);
            }
            else {
                outputBlank(true);
            }
            showDownloadButtonWithHelp(true, 'input', $(this).val() );
        }

    });*/

    $("#chkneosserver").change(function(){
        var options = '';
        if(this.checked) {
            var solvers = [{"key":"cplex", "value": "Cplex"}, {"key":"gurobi", "value": "Gurobi"}, {"key":"ipopt", "value": "Ipopt"}]
            solvers.forEach((element, index, array) => {
                options += "<option value=" + element.key + ">" + element.value + "</option>";
            });
            $("#solver").html(options);
        } else {
            options += "<option value=" + 'cbc' + ">" + 'Coin-OR Cbc' + "</option>";
            $("#solver").html(options);
        }

    });



    var url = '/project/model-run/index/' + project_id + '/' + scenario_uid;



    //$("#db-input-file-error").hide();
    $("#input-file-error").hide();
    $("#output-file-error").hide();
    $("#scenarioname-error").hide();
    $("#solver-error").hide();


    $("#model-run-form").submit(function(e) {

    // function submitForm(e) {

        e.preventDefault();

        str = '<pre name="output_pre"></pre>';
        $("#outputarea").html(str)

        var isErrors;

        var fileInput = $("#inputdatafilename").val();
        if (fileInput == '--Select data File--' || fileInput == '')
        {
            $("#input-file-error").show();
            isErrors = true;
        }
        else
        {
            $("#input-file-error").hide();
        }

        var fileOutput = $("#outputdatafilename").val();
        if (fileOutput == '--Select data File--' || fileOutput == '')
        {
            $("#output-file-error").show();
            isErrors = true;
        }

        else
        {
            $("#output-file-error").hide();
        }


        scenarioname = $("input[name='scenarioname']").val();
        if( scenarioname == '')
        {
            $("#scenarioname-error").show();
            isErrors = true;
        }
        else
        {
            $("#scenarioname-error").hide();
        }

        solver = $("input[name='solver']").val();
        if( solver == '')
        {
            $("#solver-error").show();
            isErrors = true;
        }
        else
        {
            $("#solver-error").hide();
        }

        if(isErrors) {
        return false;
        }

        $(".spinner").removeClass("invisible");
        $("#download-butto  n").removeClass("btn-yellow").attr("href", "#");

        xmlhttp = new XMLHttpRequest();
        xmlhttp.open("POST", url, true);
        xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xmlhttp.onreadystatechange = function(){
            if(xmlhttp.readyState == 4) {
                str = xmlhttp.responseText;
                //str = str.replace("\n", "<br/>");
                lindex = str.lastIndexOf("*");

                zip = ''
                if ( lindex > 0 ) {
                    zip = str.substring(lindex);
                    str = str.substring(0,lindex);
                }
                str = '<pre name="output_pre">' + str + '</pre>';
                var html = str
                var first_line = (html.split('\n')[0].match(/^\s+/));
                if (first_line != null) {
                    var blankLen = (first_line[0]).length;
                    $("#outputarea").html($.trim(html.replace(eval("/^ {" + blankLen + "}/gm"), "")));
                }
                else {
                    var blankLen = 0;
                    $("#outputarea").html($.trim(html.replace(eval("/^ {" + blankLen + "}/gm"), "")));
                }



                if (zip != "") {
                    start_index = zip.lastIndexOf('{')+1;
                    end_index = zip.lastIndexOf('}');
                    zippath = zip.substring(start_index, end_index);
                    if(zippath != "")
                        $("#download-button").addClass("btn-yellow").attr("href", settings.RESULT_URL + zippath);
                }

                $(".spinner").addClass("invisible");
                // $("#inputdatafilename").trigger("change");
                // $("#outputdatafilename").trigger("change");

            } else if (xmlhttp.readyState > 2){
                str = xmlhttp.responseText;
                //str = str.replace("\n", "<br/>");
                str = '<pre name="output_pre">' + str + '</pre>';

                var html = str
                var first_line = (html.split('\n')[0].match(/^\s+/));
                if (first_line != null) {
                    var blankLen = (first_line[0]).length;
                    $("#outputarea").html($.trim(html.replace(eval("/^ {" + blankLen + "}/gm"), "")));
                }
                else {
                    var blankLen = 0;
                    $("#outputarea").html($.trim(html.replace(eval("/^ {" + blankLen + "}/gm"), "")));
                }
            }


        }

        xmlhttp.send($('form#model-run-form').serialize());
        xmlhttp.responseType = "text/html";

});
}


function showDownloadButtonWithHelp(isShow, mode, datafilename)
{
    if(isShow)
    {
        $("#download-"+mode+"-db").removeClass('hidden');
        $("#download-"+mode+"-button-help").removeClass('hidden');

        $("#download-"+mode+"-db").attr("href", settings.RESULT_URL + "uploaded/files/" + datafilename );

    }
    else
    {
        $("#download-"+mode+"-db").addClass('hidden');
        $("#download-"+mode+"-button-help").addClass('hidden');
    }
}
