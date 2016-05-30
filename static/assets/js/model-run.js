function populateFileList(str){
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

   public function initDropZone(str){
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
}
