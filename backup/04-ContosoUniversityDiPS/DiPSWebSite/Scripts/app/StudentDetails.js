require(["/Scripts/app/Student.binding.js", 'utils'], function (appViewModel, utils) {
    var id = getParameterByName('id');
    //first we need to subscribe
    diPSClient.Subscribe('StudentReturned' + id, function (data) {
        var model = data.Student;
        appViewModel.add(model);
    });
    //then we need to publish
    diPSClient.Publish('Students.GetStudent', { Id: id });
});