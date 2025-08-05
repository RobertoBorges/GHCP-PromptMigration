require(["/Scripts/app/Course.binding.js", "/Scripts/app/Course.validate.js", 'utils', 'typeahead'], function (appViewModel, formValidator, utils, type) {
    var id = getParameterByName('id');
    //first we need to subscribe
    diPSClient.Subscribe('CourseReturned' + id, function (data) {
        var model = data.course;
        appViewModel.add(model);
        formValidator.initViewModel(appViewModel);
        formValidator.initValidator();
    });
    //then we need to publish
    diPSClient.Publish('Courses.GetCourse', { Id: id });
});