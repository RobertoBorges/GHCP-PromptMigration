define(['jquery', 'knockout', 'underscore', 'moment'], function ($, ko, _, moment) {
    if ($("#refresh").val() == 'yes') { location.reload(); } else { $('#refresh').val('yes'); }
        
    var modelStudent = [
    ];

    ko.bindingHandlers.datetimepicker = {
        init: function (element, valueAccessor, allBindingsAccessor) {

            var options = {
                pickTime: false,
                defaultDate: StudentAppViewModel.dateSelected()
            };

            $(element).parent().datetimepicker(options);

            ko.utils.registerEventHandler($(element).parent(), "change.dp", function (event) {
                var value = valueAccessor();
                if (ko.isObservable(value)) {
                    var thedate = $(element).parent().data("DateTimePicker").getDate();
                    value(moment(thedate).toDate());
                }
            });
        },
        update: function (element, valueAccessor) {
            var widget = $(element).parent().data("DateTimePicker");
            //when the view model is updated, update the widget
            var thedate = new Date(ko.utils.unwrapObservable(valueAccessor()));
            widget.setDate(thedate);
        }
    };

    var StudentAppViewModel = {
        Students: ko.observableArray(
            modelStudent
        ),

        add : function (element) {
            var that = this;

            
            var date = element.Student ? element.Student.EnrollmentDate : element.EnrollmentDate;
            that.dateSelected = ko.observable(date);
            that.Students.push(element);
        },

        remove: function () {
            var self = this;
            diPSClient.Publish('Students.Delete', { Id: this.Id });
            StudentAppViewModel.Students.remove(self);
        },

        rootElement: "",

        dateSelected: ko.observable()


    };

    $(document).ready(function () {
        //if a root element is defined, then use it
        if(StudentAppViewModel.rootElement)
            ko.applyBindings(StudentAppViewModel ); 
        else
            ko.applyBindings(StudentAppViewModel,document.getElementById(StudentAppViewModel.rootElement)); 
    });
    return StudentAppViewModel;

});
