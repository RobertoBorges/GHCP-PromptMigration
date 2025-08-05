require(["/Scripts/app/Department.binding.js", "/Scripts/app/Department.validate.js", 'utils', 'typeahead'], function (appViewModel, formValidator, utils, type) {
    var drew = false;
    var lastResult = [];
    var id = getParameterByName('id');
    //first we need to subscribe
    diPSClient.Subscribe('DepartmentReturned' + id, function (data) {
        var model = data.Department;
        appViewModel.add(model);
        formValidator.initViewModel(appViewModel);
        formValidator.initValidator();

        //the autocomplete
        $('.autocomplete').on('keyup', function (event) {
            //launch the search
            var query = $(this).val();
            if (query.length > 1) {
                //send the query
                diPSClient.Publish('Instructors.SearchInstructor', { query: query, id: id });
                if (!drew) {
                    //Create list for results
                    $(this).after('<ul id="res"></ul>');
                    drew = true;
                    $("#res").on("click", "li", function () {
                        //set the value on the hidden field
                        $(this).parent().parent().children('.autocomplete').val($(this).text());
                        $(this).parent().parent().children(':hidden:first').val($(this).attr('iId')).change();
                        //clear results
                        $("#res").empty();
                    });
                }
            } else if (drew) {
                $("#res").empty();
            }
        });
    });

    diPSClient.Subscribe('InstructorSearch' + id, function (data) {
        //compare the results, if are the same, do not redraw
        if (data.length == lastResult.length) {
            var equal = true;
            for (r in data) {
                if (data[r].Id != lastResult[r].Id) {
                    $("#res").empty();
                    equal = false;
                    break;
                }
            }
            if (equal)
                return; //all are the same
        }
        else
            $("#res").empty();
        //draw the results
        for (term in data) {
            $("#res").append("<li iId='" + data[term].Id + "'>" + data[term].Name + "</li>");
        }
        lastResult = data;
    });

    //get the department
    diPSClient.Publish('Departments.GetDepartment', { Id: id });

});