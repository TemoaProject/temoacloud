function initDropZone(){
var myDropzone = new Dropzone("div#dropArea", {
url: window.location.pathname,
params: {
'scenario_name': $("[name=scenario_name]").val(),
'csrfmiddlewaretoken': $("[name=csrfmiddlewaretoken]").val(),
},
init: function() {
  this.on('error', function(file, response) {
  PNotify.error({
  text: response.error?response.error:'Something went wrong',
});
  this.removeAllFiles();
  });
   this.on('success', function(file, response) {
   $("[name=scenario_name]").val("");
   PNotify.success({text: response.message});
   $("#dropArea").css({"pointer-events": "none", "cursor": "not-allowed"});
   this.removeAllFiles();
  });
  }
  });

  myDropzone.on('sending', function(file, xhr, formData){
            formData.append('scenario_name', $("[name=scenario_name]").val() );
    });
  }

function initJs()
{
initDropZone();
}