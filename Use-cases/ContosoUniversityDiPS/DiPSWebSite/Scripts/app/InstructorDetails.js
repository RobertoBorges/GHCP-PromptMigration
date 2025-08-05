require(["/Scripts/app/Instructor.binding.js", 'utils'], function (appViewModel, utils) {
    var id = getParameterByName('id');
    //first we need to subscribe
    diPSClient.Subscribe('InstructorReturned' + id, function (data) {
        var model = data.Instructor;
        appViewModel.add(model);
    });
    //then we need to publish
    diPSClient.Publish('Instructors.GetInstructor', { Id: id });
});