var require = {
    baseUrl: '/Scripts',
    paths: {
        jquery: 'jquery-1.9.1',
        bootstrap: 'bootstrap',
        knockout: 'knockout-3.2.0',
        underscore: 'underscore',
        bootstrapValidator: 'bootstrapValidator',
        utils: 'Utils',
        moment: 'moment',
        bootstrapDateTimePicker: 'bootstrap-datetimepicker',
        bsPagination: "bs_pagination/jquery.bs_pagination.min",
        bsPaginationLocation: "bs_pagination/en.min",
        juiFilter: "jui_filter/jquery.jui_filter_rules.min",
        juiFilterLocation: "jui_filter/en.min",
        jqUi: "jquery_ui/jquery-ui.min",
        jqBsGrid: "bs_grid/jquery.bs_grid.min",
        jqBsGridLocation: "bs_grid/en.min",
        growl: "growl/jquery.growl",
        gremlins: "gremlins.min",
        spinjs: "spinjs",
        typeahead: "bootstrap.typeahead"
    },
    shim: {
        bootstrap: ["jquery"],
	    typeahead: ['bootstrap'],
	    bootstrapValidator:["bootstrap"],
	    jqBsGrid: ["jquery", "jqBsGridLocation"],
        bsPagination: ["jquery", "bsPaginationLocation"],
        juiFilter: ["jquery", "juiFilterLocation"]

    }
};
