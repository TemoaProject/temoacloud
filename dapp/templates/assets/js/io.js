function populateFileList(modeType){
var url = '/dapp/loadfilelist';
    $.ajax({
        url: url,
        dataType: 'json',
        method: 'post',
        data: {
            mode: modeType
        },
        success: function(result) {
            var options = '<option value="0">--Select data File--</option>';
            $.each(result.data, function(index, obj) {
                options += "<option value=" + obj + ">" + obj + "</option>";
            });
            $("#file-list").html(options);
        }
    });
}

function ioFormSubmit() {

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

function displayNetworkDiagram() {
    imgPath = "/result/input/a/o.jpg";
    $('#networkDiagram').html('<img src="' + imgPath + '" width=400 height=200 alt="Output" />');
}