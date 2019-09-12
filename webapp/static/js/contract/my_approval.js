var MyApprovalTable = function () {

    var handleRecords = function () {
        var grid = new Datatable();
        //debugger;

        grid.init({
            src: $("#my_approval"),
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
                "ordering": true,
                // "bProcessing": true, //开启读取服务器数据时显示正在加载中……特别是大数据量的时候，开启此功能比较好
                ajax: {
                    url: "/contract/contract_approval/my_approval/data/"
                },
                //"bServerSide": true, //开启服务器模式，使用服务器端处理配置datatable。注意：sAjaxSource参数也必须被给予为了给datatable源代码来获取所需的数据对于每个画。 这个翻译有点别扭。开启此模式后，你对datatables的每个操作 每页显示多少条记录、下一页、上一页、排序（表头）、搜索，这些都会传给服务器相应的值。
                //"sAjaxSource": "{{rootUrl}}", //给服务器发请求的url
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
                    {"mData": "salesman", "sTitle": "销售"},
                    {"mData": null, "sTitle": "服务日期", "sClass": "center",
                        "fnCreatedCell": function (nTd, sData, oData, iRow, iCol) {
                            var element = $(nTd).empty();
                            var timerange = [oData["contract_start_date"], oData["contract_end_date"]].join(" - ");
                            element.append(timerange);
                        }
                    },
                    {"mData": "total_money", "sTitle": "合同总价"},
                    {"mData": "approval_status_name", "sTitle": "审批状态"},
                    {"mData": null, "sTitle": "审批", "sClass": "center",
                        "fnCreatedCell": function (nTd, sData, oData, iRow, iCol) {
                            var element = $(nTd).empty();
                            var agree = $('<a href="javascript:;" class="btn btn-xs btn-info">通过</a>');
                            var disagree = $('<a href="" class="btn btn-xs btn-danger"  data-toggle="modal" data-target="#approval_note_dialog">不通过</a>');
                            element.append(agree);
                            element.append(disagree);

                            agree.on('click',function () {
                                var id = oData["id"];
                                var con = confirm("确定审批通过吗?");
                                if (con) {
                                    $.get("agree/" + id + "/", function (data) {
                                        if (data.success) {
                                            $.growlService("审批成功！", {type: "success"});
                                            location.href = "/contract/contract_approval/";
                                        } else {
                                            $.growlService("审批失败！", {type: "danger"});
                                        }
                                    })
                                }
                            });
                            disagree.on('click',function () {
                                var id = oData["id"];
                                $("#approval_note_form").ajaxForm({
                                    type: "post",
                                    url: "/contract/contract_approval/disagree/"+id+"/",    //提交到的url
                                    success: function (data) {
                                        if (data.success) {
                                            location.href = "/contract/contract_approval/"
                                        }
                                    }
                                });
                            })
                        }
                    }
                ],
                "fnRowCallback": function (nRow, aData, iDisplayIndex) {// 当创建了行，但还未绘制到屏幕上的时候调用，通常用于改变行的class风格

                },
                "fnInitComplete": function (oSettings, json) { //表格初始化完成后调用 在这里和服务器分页没关系可以忽略
                    var a=json['recordsFiltered'];
                    if(a)
                        $('#approvaling').html(a);
                }
            }
        });

        var tableWrapper = grid.getTableWrapper();
        // handle filter submit button click
        tableWrapper.on('click', '.filter-submit', function (e) {
            e.preventDefault();
            //only set no reaload
            grid.setUrl("/contract/contract_approval/my_approval/data/");
            grid.submitFilter();
        });

        // handle filter cancel button click
        tableWrapper.on('click', '.filter-cancel', function (e) {
            e.preventDefault();
            $('.select').val('').trigger('change'); //select2 置空
            $('.dateFilter').val('');
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
