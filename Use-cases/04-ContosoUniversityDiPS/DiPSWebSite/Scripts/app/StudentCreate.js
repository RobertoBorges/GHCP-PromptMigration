require(["/Scripts/app/Student.binding.js", "/Scripts/app/Student.validate.js", 'utils', 'typeahead'], function (appViewModel, formValidator, utils, type) {
    var drew = false;
    var lastResult = [];
    var id = '00000000-0000-0000-0000-000000000000';
    //first we need to subscribe
    diPSClient.Subscribe('StudentReturned' + id, function (data) {
        var model = data.Student;
        appViewModel.add(model);
        formValidator.initViewModel(appViewModel);
        formValidator.initValidator();
    });
    //get the Student
    diPSClient.Publish('Students.GetStudent', { Id: id });
});