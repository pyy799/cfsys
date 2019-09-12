/***
Wrapper/Helper Class for datagrid based on jQuery Datatable Plugin
***/
var Datatable = function() {
    var tableOptions; // main options
    var dataTable; // datatable object
    var table; // actual table jquery object
    var tableContainer; // actual table container object
    var tableWrapper; // actual table wrapper jquery object
    var tableInitialized = false;
    var ajaxParams = {}; // set filter mode
    var filterParams = {};
    var the;

    var countSelectedRecords = function() {
        var selected = $('tbody > tr > td:nth-child(1) input[type="checkbox"]:checked', table).size();
    };

    return {
        //main function to initiate the module
        init: function(options) {
            //debugger;    
            if (!$().dataTable) {
                return;
            }

            the = this;

            // default settings
            options = $.extend(true, {
                src: "", // actual table  
                filterApplyAction: "filter",
                filterCancelAction: "filter_cancel",
                resetGroupActionInputOnSuccess: true,
                loadingMessage: 'Loading...',
                dataTable: {
                   // "dom": "<'row'<'col-md-4 col-sm-12'<'table-group-actions pull-right'>>r><'table-scrollable't><'row'<'col-md-8 col-sm-12'pli><'col-md-4 col-sm-12'>>", // datatable layout
                    "dom":"<'row'<'col-md-12 col-sm-12'<'table-group-actions'>>r><'row'<'col-md-6 col-sm-12'f>r><'table-scrollable't><'row'<'col-md-3 col-sm-12'i><'col-md-4 col-sm-12'l><'col-md-5 col-sm-12'p>>",
                    "oLanguage": {//下面是一些汉语翻译
                        "sSearch": "搜索",
                        "sLengthMenu": "每页显示 _MENU_ 条记录",
                        "sZeroRecords": "没有检索到数据",
                        "sInfo": "显示 _START_ 至 _END_ 条 共 _TOTAL_ 条",
                        "sInfoFiltered": "(筛选自 _MAX_ 条数据)",
                        "sInfoEmtpy": "没有数据",
                       // "sProcessing": "正在加载数据...",
                       // "sProcessing": "<img src='../global/img/loading-spinner-grey.gif' />",//这里是给服务器发请求后到等待时间显示的 加载gif
                        "oPaginate":
                        {
                            "sFirst": "首页",
                            "sPrevious": "前一页",
                            "sNext": "后一页",
                            "sLast": "末页"
                        }
                    },

                    "orderCellsTop": true,
                    "columnDefs": [{ // define columns sorting options(by default all columns are sortable extept the first checkbox column)
                        'orderable': false,
                        'targets': [0]
                    }],
                    // set the initial value
                    "pageLength": 1,   
                    "sPaginationType": "bootstrap_full_number", // pagination type(bootstrap, bootstrap_full_number or bootstrap_extended)
                    "autoWidth": false, // disable fixed width and enable fluid table
                    "processing": false, // enable/disable display message box on record load
                    "serverSide": false // enable/disable server side ajax loading

                }
            }, options);

            tableOptions = options;

            // create table's jquery object
            table = $(options.src);
            tableContainer = table.parents(".table-container");
            columns = options.dataTable.aoColumns;
            // apply the special class that used to restyle the default datatable
            var tmp = $.fn.dataTableExt.oStdClasses;

            $.fn.dataTableExt.oStdClasses.sWrapper = $.fn.dataTableExt.oStdClasses.sWrapper + " dataTables_extended_wrapper";
            $.fn.dataTableExt.oStdClasses.sFilterInput = "form-control input-small input-sm input-inline";
            $.fn.dataTableExt.oStdClasses.sLengthSelect = "form-control input-xsmall input-sm input-inline";

            // initialize a datatable
            dataTable = table.DataTable(options.dataTable);

            // revert back to default
            $.fn.dataTableExt.oStdClasses.sWrapper = tmp.sWrapper;
            $.fn.dataTableExt.oStdClasses.sFilterInput = tmp.sFilterInput;
            $.fn.dataTableExt.oStdClasses.sLengthSelect = tmp.sLengthSelect;

            // get table wrapper
            tableWrapper = table.parents('.dataTables_wrapper');

            // build table group actions panel
            if ($('.table-actions-wrapper', tableContainer).size() === 1) {
                $('.table-group-actions', tableWrapper).html($('.table-actions-wrapper', tableContainer).html()); // place the panel inside the wrapper
                $('.table-actions-wrapper', tableContainer).remove(); // remove the template container
            }
             // handle group checkboxes check/uncheck
            $('.group-checkable', table).change(function() {
                var set = $('tbody > tr > td:nth-child(1) input[type="checkbox"]', table);
                var checked = $(this).is(":checked");
                $(set).each(function() {
                    $(this).attr("checked", checked);
                });
                $.uniform.update(set);
                countSelectedRecords();
            });

            // handle row's checkbox click
            table.on('change', 'tbody > tr > td:nth-child(1) input[type="checkbox"]', function() {
                countSelectedRecords();
            });
        },
        setFilterParam: function(name, value){
            filterParams[name] = value;
        },
        setAjaxData:function(){
            // get all typeable inputs
            $('textarea.form-filter, select.form-filter, input.form-filter:not([type="radio"],[type="checkbox"])', tableWrapper).each(function() { 
               // the.setAjaxParam($(this).attr("name"), $(this).val());
                the.setFilterParam($(this).attr("name"), $(this).val());
            });

            // get all checkboxes
            $('input.form-filter[type="checkbox"]:checked', tableWrapper).each(function() {
                the.addAjaxParam($(this).attr("name"), $(this).val());
            });

            // get all radio buttons
            $('input.form-filter[type="radio"]:checked', tableWrapper).each(function() {
               // the.setAjaxParam($(this).attr("name"), $(this).val());
                the.setFilterParam($(this).attr("name"), $(this).val());
            });
            the.setAjaxParam("filter", filterParams);
            
        },
        submitFilter: function() {
            the.setAjaxParam("action", tableOptions.filterApplyAction);
            the.setAjaxData();
            return ajaxParams;
            

 //           dataTable.ajax.reload();
        },

        resetFilter: function() {
            $('textarea.form-filter, select.form-filter, input.form-filter', tableWrapper).each(function() {
                $(this).val("");
            });
            $('input.form-filter[type="checkbox"]', tableWrapper).each(function() {
                $(this).attr("checked", false);
            });
            the.clearAjaxParams();
            the.addAjaxParam("action", tableOptions.filterCancelAction);
            dataTable.ajax.reload();
        },

        getSelectedRowsCount: function() {
            return $('tbody > tr > td:nth-child(1) input[type="checkbox"]:checked', table).size();
        },

        getSelectedRows: function() {
            var rows = [];
            $('tbody > tr > td:nth-child(1) input[type="checkbox"]:checked', table).each(function() {
                rows.push($(this).val());
            });

            return rows;
        },
        
        setAjaxParam: function(name, value) {
            ajaxParams[name] = value;
        },

        addAjaxParam: function(name, value) {
            if (!ajaxParams[name]) {
                ajaxParams[name] = [];
            }

            skip = false;
            for (var i = 0; i < (ajaxParams[name]).length; i++) { // check for duplicates
                if (ajaxParams[name][i] === value) {
                    skip = true;
                }
            }

            if (skip === false) {
                ajaxParams[name].push(value);
            }
        },

        clearAjaxParams: function(name, value) {
            ajaxParams = {};
        },

        getDataTable: function() {
            return dataTable;
        },

        getTableWrapper: function() {
            return tableWrapper;
        },

        gettableContainer: function() {
            return tableContainer;
        },

        getTable: function() {
            return table;
        },
        setUrl:function(urlParam) {
            //set new url
            dataTable.ajax.url(urlParam);
        },
        getColumns: function(){
            return columns
        }
    };

};
