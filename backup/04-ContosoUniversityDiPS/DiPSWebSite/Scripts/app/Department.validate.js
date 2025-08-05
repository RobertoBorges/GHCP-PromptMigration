define(['jquery', 'bootstrapValidator', 'moment', 'bootstrapDateTimePicker'], function ($) {
    var initValidator = function () {


        $(".department_form").bootstrapValidator({
            // To use feedback icons, ensure that you use Bootstrap v3.1.0 or later
            feedbackIcons: {
                valid: 'glyphicon glyphicon-ok',
                invalid: 'glyphicon glyphicon-remove',
                validating: 'glyphicon glyphicon-refresh'
            },
            fields: {

                Id: {
                    message: 'The Id is not valid',
                    validators: {
                        numeric: {

                        },
                        notEmpty: {

                        }
                    }
                },

                Name: {
                    message: 'The Name is not valid',
                    validators: {
                        notEmpty: {
                            max: 50
                        }
                    }
                },

                Budget: {
                    message: 'The Budget is not valid',
                    validators: {
                        numeric: {

                        },
                        notEmpty: {

                        }
                    }
                },

                StartDate: {
                    message: 'The StartDate is not valid',
                    validators: {
                        date: {

                        },
                        notEmpty: {

                        }
                    }
                },

                InstructorID: {
                    message: 'The InstructorID is not valid',
                    validators: {

                    }
                },


            }
        }).on('success.form.bv', function (e) {
            e.preventDefault();

            viewModel.Departments()[0].Department.StartDate = viewModel.dateSelected();

            //do the push
            diPSClient.Publish('Departments.Save', viewModel.Departments()[0]);

            //redirect to index
            window.location = '/department/index.html';

        });
    };

    var initViewModel = function (model) {
        viewModel = model;
    };



    var formValidator = {
        initViewModel: initViewModel,
        initValidator: initValidator
    };


    return formValidator;
});
