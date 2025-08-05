define(['jquery', 'knockout', 'underscore', 'moment'], function ($, ko, _, moment) {
    if ($("#refresh").val() == 'yes') { location.reload(); } else { $('#refresh').val('yes'); }
        
    var modelInstructor = [
    ];

    ko.bindingHandlers.datetimepicker = {
        init: function (element, valueAccessor, allBindingsAccessor) {

            var options = {
                pickTime: false,
                defaultDate: InstructorAppViewModel.dateSelected()
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

    var InstructorAppViewModel = {
        Instructors: ko.observableArray(
            modelInstructor
        ),

        add : function (element) {
            var that = this;

            
            var date = element.Instructor ? element.Instructor.HireDate : element.HireDate;
            that.dateSelected = ko.observable(date);
            that.Instructors.push(element);
        },

        remove: function () {
            var self = this;
            diPSClient.Publish('Instructors.Delete', { Id: this.Id });
            InstructorAppViewModel.Instructors.remove(self);
        },

        rootElement: "",

        dateSelected: ko.observable()


    };

    $(document).ready(function () {
        //if a root element is defined, then use it
        if(InstructorAppViewModel.rootElement)
            ko.applyBindings(InstructorAppViewModel ); 
        else
            ko.applyBindings(InstructorAppViewModel,document.getElementById(InstructorAppViewModel.rootElement)); 
    });
    return InstructorAppViewModel;

});
