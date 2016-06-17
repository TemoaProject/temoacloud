function initValidate()
{
// validate signup form on keyup and submit
		$("#model-run-form").validate({
			rules: {
				inputdatafilename: "required",
				outputdatafilename: "required",
				scenarioname: "required",
				
			},
			messages: {
				inputdatafilename: "Please enter your firstname",
				outputdatafilename: "Please enter your lastname",
				scenarioname: "Please enter your Scenario name",
				
			}
		});

}
