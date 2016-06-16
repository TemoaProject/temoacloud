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
   
    initForm();
    
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

function initForm() { 
    
    var url = '/dapp/model';
    
    $("#input-file-error").hide();
    $("#output-file-error").hide();
    $("#scenarioname-error").hide();
    $("#solver-error").hide();
    
    
    $("#model-run-form").submit(function(e) {
            
        e.preventDefault();
        
        var isErrors;
        
        var fileInput = $("#inputdatafilename option:selected").text();
        if (fileInput == '--Select data File--' || fileInput == '') 
        {
            $("#input-file-error").show();
            isErrors = true;
        } 
        else 
        {
            $("#input-file-error").hide();
        }

        var fileOutput = $("#outputdatafilename option:selected").text();
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
        
        if(isErrors)
            return false;
        
        
        $.post( url, $('form#model-run-form').serialize(), function(data) {
            
            alert("model-run-submit");
            alert(data.message);
        },
       'json' // I expect a JSON response
    );
});
}
