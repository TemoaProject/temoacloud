function populateFileList(mode){
    var url = '/dapp/loadfilelist';

    $.ajax({
        url: url,
        dataType: 'json',
        method: 'get',
        data: {
            mode: mode
        },
        success: function(result) {
            
            var options = '<option value="0">--Select data File--</option>';
            $.each(result.data, function(index, obj) {
                options += "<option value=" + obj + ">" + obj + "</option>";
            });
            
            $("#datafilename").html(options);
            
        }
    });
}



/*function ioFormSubmit() {

    fileInput = $("#file-list option:selected").text();
    if (fileInput == '--Select data File--') {
        $("#input-file-error").show();
        return false;
    } else {
        $("#input-file-error").hide();
    }
    comInput = $("#comomodity-input-text").val();
    comOutput = $("#comomodity-output-text").val();
    colorScheme = $("input[name=qcolorscheme]:checked").val();
    outputFormat = $("#output-format").text();
    displayNetworkDiagram();
    alert("hi");
    var url = '/dapp/runinput';
    $.ajax({
        url: url,
        method: "post",
        data: {datafile:fileInput,commodityoutputlimit:comInput,commodityinputlimit:comOutput,ccolorscheme:colorScheme,format:outputFormat},
        dataType: 'json',
        success: function(result) {
            alert(result);
            displayNetworkDiagram();
        }
    });

}
*/


function displayNetworkDiagram(folder, filename) {
    
    //file is inside result/ folder but due to static django we have to say url /static :(  ..enjoy :)
    var imgPath = "/static/" + folder + "/" + filename + "/simple_model.svg" ;
    $('#networkDiagram').html('<img src="' + imgPath + '" height=400 alt="Output" />');
}


function initForm() {
    
    var url = '/dapp/runinput';
    
    
    
    $("#input-form").submit(function(e) {
        
        
        e.preventDefault();
        
        
        
        var fileInput = $("#datafilename option:selected").text();
        if (fileInput == '--Select data File--' || fileInput == '') 
        {
            $("#input-file-error").show();
            return false;
        } 
        else 
        {
            $("#input-file-error").hide();
        }
        
        
        $.post( url, $('form#input-form').serialize(), function(data) {
            
            //alert(data.filename + data.mode);
            
            
            displayNetworkDiagram(data.mode, data.filename );
        },
       'json' // I expect a JSON response
    );
});


/*
    fileInput = $("#file-list option:selected").text();
    if (fileInput == '--Select data File--') {
        $("#input-file-error").show();
        return false;
    } else {
        $("#input-file-error").hide();
    }
    comInput = $("#comomodity-input-text").val();
    comOutput = $("#comomodity-output-text").val();
    colorScheme = $("input[name=qcolorscheme]:checked").val();
    outputFormat = $("#output-format").text();
    displayNetworkDiagram();
    
    //alert("hi");
    
    
    $.ajax({
        url: url,
        method: "post",
        data: {datafile:fileInput,commodityoutputlimit:comInput,commodityinputlimit:comOutput,ccolorscheme:colorScheme,format:outputFormat},
        dataType: 'json',
        success: function(result) {
            alert(result);
            displayNetworkDiagram();
        }
    });*/

}

function showHideCommodityTechnology(){
    $('#commodity-technology-type').change(function(){
    if($('#commodity-technology-type').val() == 'none'){
        $('#commodity-technology-value').hide();
        $('#commodity-label').hide();
    } else {
        $('#commodity-technology-value').show();
        $('#commodity-label').html("Select "+$('#commodity-technology-type').val()+" value");
        $('#commodity-label').show();
}
});
}



function initJs(str)
{
    initForm();
    $('#commodity-technology-value').hide();
    $('#commodity-label').hide();
    populateFileList(str);
    showHideCommodityTechnology();
    
    $("#input-file-error").hide();
    
    /*$("#input-form").submit(function(e) {
        e.preventDefault();
        ioFormSubmit();
    });*/
    
    
    // Dropzone class:
    var myDropzone = new Dropzone("div#dropArea", {
        url: "/dapp/fileupload",
        params: {
        mode: str
    }
    });

    myDropzone.on("success", function(fileList, response) 
    {
        
        var options = '<option value="0">--Select Input File--</option>';
        
        $.each(response.data, function(index, obj) {
            options += fileList.name == obj ? "<option selected='selected' value=" + obj + ">" + obj + "</option>" :
                "<option value=" + obj + ">" + obj + "</option>";
        });
        
        $("#datafilename").html(options);

        myDropzone.removeAllFiles();

    });
    
}
