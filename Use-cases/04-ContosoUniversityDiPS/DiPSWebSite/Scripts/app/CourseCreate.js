require(["/Scripts/app/Course.binding.js", "/Scripts/app/Course.validate.js", 'utils', 'typeahead'], function (appViewModel, formValidator, utils, type) {
    //first we need to subscribe
    diPSClient.Subscribe('CourseReturned' + '00000000-0000-0000-0000-000000000000', function (data) {
        var model = data.course;
        appViewModel.add(model);
        formValidator.initViewModel(appViewModel);
        formValidator.initValidator();
    });
    //then we need to publish
    diPSClient.Publish('Courses.GetCourse', { Id: '00000000-0000-0000-0000-000000000000' });
});