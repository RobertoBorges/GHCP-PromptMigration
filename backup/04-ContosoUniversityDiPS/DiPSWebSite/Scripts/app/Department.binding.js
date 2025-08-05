define(['jquery', 'knockout', 'underscore', 'moment'], function ($, ko, _, moment) {
    if ($("#refresh").val() == 'yes') { location.reload(); } else { $('#refresh').val('yes'); }
        
    var modelDepartment = [
    ];

    ko.bindingHandlers.datetimepicker = {
        init: function (element, valueAccessor, allBindingsAccessor) {

            var options = {
                pickTime: false,
                defaultDate: DepartmentAppViewModel.dateSelected()
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

    var DepartmentAppViewModel = {
        Departments: ko.observableArray(
            modelDepartment
        ),

        add : function (element) {
            var that = this;

            var date = element.StartDate != undefined ? element.StartDate : element.Department.StartDate;
            that.dateSelected = ko.observable(date);
            
            that.Departments.push(element);
        },

        remove: function () {
            var self = this;
            diPSClient.Publish('Departments.Delete', { Id: this.Id });
            DepartmentAppViewModel.Departments.remove(self);
        },

        rootElement: "",

        dateSelected: ko.observable()


    };

    $(document).ready(function () {
        //if a root element is defined, then use it
        if(DepartmentAppViewModel.rootElement)
            ko.applyBindings(DepartmentAppViewModel ); 
        else
            ko.applyBindings(DepartmentAppViewModel,document.getElementById(DepartmentAppViewModel.rootElement)); 
    });
    return DepartmentAppViewModel;

});
