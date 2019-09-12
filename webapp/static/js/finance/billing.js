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
                "ordering": true,
                // "bProcessing": true, //开启读取服务器数据时显示正在加载中……特别是大数据量的时候，开启此功能比较好
                ajax: {
                    url: "/finance/finance_billing/data/"
                },
                //"bServerSide": true, //开启服务器模式，使用服务器端处理配置datatable。注意：sAjaxSource参数也必须被给予为了给datatable源代码来获取所需的数据对于每个画。 这个翻译有点别扭。开启此模式后，你对datatables的每个操作 每页显示多少条记录、下一页、上一页、排序（表头）、搜索，这些都会传给服务器相应的值。
                //"sAjaxSource": "{{rootUrl}}", //给服务器发请求的url
                "aoColumns": [ //这个属性下的设置会应用到所有列，按顺序没有是空,bVisible是否可见
                    {
                        "mData": null,
                        // "sTitle": '<input id="checkall" name="" type="checkbox" value="">',
                        "fnCreatedCell": function (nTd, sData, oData, iRow, iCol) {
                            var element = $(nTd).empty();
                            element.append("<input type='checkbox' name='checkList' />");
                        }
                    },
                    {"mData": "id", "sTitle": "ID", "bVisible": false},
                    {"mData": "contract_number", "sTitle": "合同编号"},
                    {"mData": "customer_name", "sTitle": "客户名称"},
                    {"mData": "month", "sTitle": "月份"},
                    {"mData": "salesman_name", "sTitle": "销售"},
                    {"mData": "total_money", "sTitle": "总费用"},
                    {"mData": "status", "sTitle": "状态"},
                    {"mData": null, "sTitle": "预览", "sClass": "center",
                        "fnCreatedCell": function (nTd, sData, oData, iRow, iCol) {
                            var element = $(nTd).empty();
                            var detail = $('<a href="/finance/finance_billing_detail/'+oData["id"]+'">账单预览</a>');
                            element.append(detail);
                        }
                    },
                    {"mData": null, "sTitle": "操作", "sClass": "center",
                        "fnCreatedCell": function (nTd, sData, oData, iRow, iCol) {
                            var element = $(nTd).empty();
                            var send = $('<a href="javascript:;" class="btn btn-xs btn-info"><i class="fa fa-envelope"></i> 发邮件</a>');
                            var remove = $('<a href="javascript:;" class="btn btn-xs btn-danger"><i class="fa fa-times"></i> 删除</a>');
                            element.append(send);
                            element.append(remove);

                            send.on('click', function () {
                                var id = oData["id"];
                                $.get("/finance/bill_send/" + id + "/", function (data) {
                                    if (data.success) {
                                        $.growlService("邮件发送成功！", {type: "success"});
                                        grid.getDataTable().ajax.reload();
                                    } else {
                                        $.growlService("邮件发送失败！", {type: "danger"})
                                    }
                                })
                            });

                            remove.on('click', function () {
                                var con = confirm("确定删除？");
                                if (con) {
                                    $.get("/finance/bill_remove/" + oData["id"] + "/", function (data) {
                                        if (data.success) {
                                            $.growlService("删除成功", {type: "success"});
                                            grid.getDataTable().ajax.reload();
                                        } else {
                                            $.growlService("删除失败", {type: "danger"})
                                        }
                                    })
                                }
                            });
                        }
                    }
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
            //only set no reaload
            grid.setUrl("/finance/finance_billing/data/");
            grid.submitFilter();
        });

        // handle filter cancel button click
        tableWrapper.on('click', '.filter-cancel', function (e) {
            e.preventDefault();
            $('.select').val('').trigger('change'); //select2 置空
            $('.date').val('');
            grid.resetFilter();
        });

        //点击复选框,选中行
        $("#example").on('change', 'tr input[name="checkList"]', function () {
            var $tr = $(this).parents('tr');
            var check = $(this).prop("checked");
            if (!check) {
                $(this).prop("checked", true).uniform('refresh');
            } else {
                $(this).prop("checked", false).uniform('refresh');
            }
            //$tr.toggleClass('selected');
        });

        //单击行，选中复选框
        $("#example").on('click', 'tr', function (e) {
            var check_box = $(this).find("input[type='checkbox']");
            if (check_box.attr("id") == "checkall") {
                return
            }

            var check = $(this).find("input[type='checkbox']").prop("checked");
            if (!check) {
                $(this).find("input[type='checkbox']").prop("checked", true).uniform('refresh');
            } else {
                $(this).find("input[type='checkbox']").prop("checked", false).uniform('refresh');
            }
            $(this).parents("tr").toggleClass("selected");
        });

        // 全选按钮
        $(".checkall").click(function () {
            $("#example tr input[type='checkbox']").each(function () {
                var check = $(this).parent("span").hasClass("checked");
                if (!check) {
                    $(this).prop("checked", true).uniform('refresh');
                } else {
                    $(this).prop("checked", false).uniform('refresh');
                }
                $(this).parents("tr").toggleClass("selected");
            });
        });

        // 全部取消按钮
        $(".clearall").click(function() {
             $("#example tr input[type='checkbox']").each(function() {
                 $(this).prop("checked", false).uniform('refresh');
             });
        });

        // 多选发送邮件按钮
        $("#btnSendAll").on('click', function () {
            var ott = $("#example").DataTable().rows(".selected");
            if (ott[0].length < 1) {
                alert("请至少选择一行发送账单！");
                return
            }
            var bids = "";
            $.each(ott.data(), function (key, val) {
                bids += val["id"] + "_";
            });
            $.get("/finance/bill_send/" + bids + "/", function (data) {
                if (data.success) {
                    $.growlService("发送账单成功！", {type: "success"});
                    grid.getDataTable().ajax.reload();
                }
                else {
                    $.growlService("发送账单失败！", {type: "danger"});
                }
            });
        });
        // 多选删除按钮
        $("#btnRemoveAll").on('click', function () {
            var ott = $("#example").DataTable().rows(".selected");
            if (ott[0].length < 1) {
                alert("请至少选择一行账单删除！");
                return
            }
            var bids = "";
            $.each(ott.data(), function (key, val) {
                bids += val["id"] + "_";
            });
            $.get("/finance/bill_remove/" + bids + "/", function (data) {
                if (data.success) {
                    $.growlService("删除账单成功！", {type: "success"});
                    grid.getDataTable().ajax.reload();
                }
                else {
                    $.growlService("删除账单失败！", {type: "danger"});
                }
            });
        })
    };

    var handleDatePickers = function () {

        if (jQuery().datepicker) {
            $('.date-picker').datepicker({
                rtl: Metronic.isRTL(),
                orientation: "left",
                autoclose: true,
                format: "yyyy-mm-dd"
            });
            //$('body').removeClass("modal-open"); // fix bug when inline picker is used in modal
        }

        /* Workaround to restrict daterange past date select: http://stackoverflow.com/questions/11933173/how-to-restrict-the-selectable-date-ranges-in-bootstrap-datepicker */
    };


    return {

        //main function to initiate the module
        init: function () {
            handleRecords();
            handleDatePickers();
        }

    };

}();
