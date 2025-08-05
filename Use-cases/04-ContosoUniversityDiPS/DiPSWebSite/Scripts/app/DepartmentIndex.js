require(["/Scripts/app/Department.binding.js", 'moment', 'utils', 'underscore'], function (appViewModel, moment, utils, _) {

    //first we need to subscribe
    diPSClient.Subscribe('DepartmentsUpdated', function (data) {
        appViewModel.Departments.removeAll();
        _.each(data.Departments, function (item) {
            appViewModel.add(item);
        });
    });
    //then we need to publish
    diPSClient.Publish('Departments.GetDepartments', { id: '' });

});