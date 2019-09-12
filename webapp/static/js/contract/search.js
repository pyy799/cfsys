var TableExample = function () {

    var handleRecords = function () {
        var grid = new Datatable();
        //debugger;

        grid.init({
            src: $("#example"),
            onSuccess: function (grid) {
                // execute some code after table records loaded
            },
            onError: function (grid) {
                // execute some code on network or other general error
            },
            onDataLoad: function (grid) {
                // execute some code on ajax data load
            },
            dataTable: {
                "sPaginationType": "simple_numbers", //分页风格，full_number会把所有页码显示出来（大概是，自己尝试）
                "pageLength": 10,//每页显示10条数据
                "bAutoWidth": false,//宽度是否自动，感觉不好使的时候关掉试试
                "bLengthChange": false,
                "serverSide": true,
                "bFilter": false,
                "bSort":true,
                "ordering": true,
                ajax: {
                    url: "/contract/contract_search/data/"
                },
                "aoColumns": [ //这个属性下的设置会应用到所有列，按顺序没有是空,bVisible是否可见
                    {"mData": "id", "sTitle": "ID", "bVisible": false},
                    {"mData": "contract_number", "sTitle": "合同编号", "sClass": "center",
                        "fnCreatedCell": function (nTd, sData, oData, iRow, iCol) {
                            var element = $(nTd).empty();
                            var detail = $('<a href="/contract/contract_detail/'+oData["id"]+'">'+oData["contract_number"]+'</a>');
                            element.append(detail);
                        }
                    },
                    {"mData": "customer", "sTitle": "客户名称"},
                    {"mData": "deal_path_name", "sTitle": "签单渠道"},
                    {"mData": "deal_type_name", "sTitle": "签单类型"},
                    {"mData": "sign_type_name", "sTitle": "合同类型"},
                    {"mData": "contract_related", "sTitle": "关联合同号"},
                    {"mData": null, "sTitle": "服务日期", "sClass": "center",
                        "fnCreatedCell": function (nTd, sData, oData, iRow, iCol) {
                            var element = $(nTd).empty();
                            var timerange = [oData["contract_start_date"], oData["contract_end_date"]].join(" - ");
                            element.append(timerange);
                        }
                    },
                    {"mData": "service_type_name", "sTitle": "服务类型"},
                    {"mData": "prestore", "sTitle": "预存费用"},
                    {"mData": "function_money", "sTitle": "功能模块总价"},
                    {"mData": "total_service_money", "sTitle": "服务总价"},
                    {"mData": "service_rank_money", "sTitle": "售后总价"},
                    {"mData": "total_money", "sTitle": "合同总价"},
                    {"mData": "contact_person", "sTitle": "客户联系人"},
                    {"mData": "contact_tel", "sTitle": "联系电话"},
                    {"mData": "contact_email", "sTitle": "联系邮箱"},
                    {"mData": "customer_service", "sTitle": "客服"},
                    {"mData": "salesman", "sTitle": "销售"},
                    {"mData": "salesman_depart", "sTitle": "销售部门"}
                ],
                "fnRowCallback": function (nRow, aData, iDisplayIndex) {// 当创建了行，但还未绘制到屏幕上的时候调用，通常用于改变行的class风格

                },
                "fnInitComplete": function (oSettings, json) { //表格初始化完成后调用 在这里和服务器分页没关系可以忽略

                }

            }
        });

        var tableWrapper = grid.getTableWrapper();
        // handle filter submit button click
        tableWrapper.on('click', '.filter-submit', function (e) {
            e.preventDefault();
            var fil_params = [];
            $('.getFilter').each(function(index, val){
                if ($(this).val()){
                    fil_params.push(''+$(this).data("key")+'='+$(this).val()+'')
                }
            });
            grid.setUrl("/contract/contract_search/data/?"+fil_params.join('&'));
            grid.submitFilter();
        });

        // handle filter cancel button click
         tableWrapper.on('click', '.filter-cancel', function (e) {
            e.preventDefault();
            $('.select').val('').trigger('change'); //select2 置空
            $('.date').val('');
            grid.resetFilter();
        });

    };

    return {

        //main function to initiate the module
        init: function () {
            handleRecords();
        }

    };

}();
