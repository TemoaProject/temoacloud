 function populateFileList(str) {
    var url = '/dapp/loadfilelist';
    $.ajax({
        url: url,
        dataType: 'json',
        method: 'get',
        data: {
            mode: str
        },
        success: function(result) {
            
            var options = '<option value="0">--Select data File--</option>';
            $.each(result.data, function(index, obj) {
                options += "<option value=" + obj + ">" + obj + "</option>";
            });
            $("#"+str+"datafilename").html(options);
            
        }
    });
}
 
 function initDropZone(str){
    // Dropzone class:
    var myDropzone = new Dropzone("div#"+str+"dropArea", {
        url: "/dapp/fileupload",
        params: {
        mode: str
    }
    });

    myDropzone.on("success", function(fileList, response) 
    {
        
        var options = '<option value="0">--Select data File--</option>';
        
        $.each(response.data, function(index, obj) {
            options += fileList.name == obj ? "<option selected='selected' value=" + obj + ">" + obj + "</option>" :
                "<option value=" + obj + ">" + obj + "</option>";
        });
        
        $("#"+str+"datafilename").html(options);

        myDropzone.removeAllFiles();

    });

   } 

function initJs()
{ 
    populateFileList('input');
    populateFileList('output');
    initDropZone('input');
    initDropZone('output');
    $("#input-file-error").hide();
    $("#output-file-error").hide();
    initForm();
}

function initForm() { 
    
    var url = '/dapp/model';
    
    
    
    $("#model-run-form").submit(function(e) {
            
        e.preventDefault();
        
        var fileInput = $("#inputdatafilename option:selected").text();
        if (fileInput == '--Select data File--' || fileInput == '') 
        {
            $("#input-file-error").show();
            return false;
        } 
        else 
        {
            $("#input-file-error").hide();
        }

        var fileOutput = $("#outputdatafilename option:selected").text();
        if (fileOutput == '--Select data File--' || fileOutput == '') 
        {
            $("#output-file-error").show();
            return false;
        } 
        else 
        {
            $("#output-file-error").hide();
        }
        
        
        $.post( url, $('form#model-run-form').serialize(), function(data) {
            
            alert("model-run-submit");
        },
       'json' // I expect a JSON response
    );
});
}