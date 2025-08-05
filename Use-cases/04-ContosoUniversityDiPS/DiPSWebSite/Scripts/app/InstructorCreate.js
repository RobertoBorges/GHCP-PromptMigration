require(["/Scripts/app/Instructor.binding.js", "/Scripts/app/Instructor.validate.js", 'utils', 'typeahead'], function (appViewModel, formValidator, utils, type) {


    var drew = false;
    var lastResult = [];
    var id = '00000000-0000-0000-0000-000000000000';
    //first we need to subscribe
    diPSClient.Subscribe('InstructorReturned' + id, function (data) {
        var model = data.Instructor;
        appViewModel.add(model);
        formValidator.initViewModel(appViewModel);
        formValidator.initValidator();
    });
    //get the Instructor
    diPSClient.Publish('Instructors.GetInstructor', { Id: id });

});