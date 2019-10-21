var UpdateTable = function () {
// 等待提交列表
    var handleRecords = function () {
        var grid = new Datatable();
        //debugger;
        grid.init({
            src: $("#update_table"),
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
                    url: "/product_management/update/data/"
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
                    {"mData": "product_name", "sTitle": "产品名称"},
                    {"mData": "pCompany_name", "sTitle": "公司名称"},
                    // {"mData": "one_year_money", "sTitle": "过去一年销售额"},
                    // {"mData": "three_year_money", "sTitle": "过去三年销售额"},
                    {"mData": "maturity_name", "sTitle": "成熟度"},
                    {"mData": "independence_name", "sTitle": "自主度"},
                    {"mData": "business_name", "sTitle": "业务领域"},
                    {"mData": "technology_name", "sTitle": "技术形态"},
                    {"mData": "uploader", "sTitle": "申请人"},
                    {"mData": "apply_type_name", "sTitle": "申请类型"},
                    {"mData":null,"sTitle":"操作", "sClass": "center",
                        "fnCreatedCell": function (nTd, sData, oData, iRow, iCol) {
                            var element = $(nTd).empty();
                            var modify = $('<a href="/product_management/edit_product/'+oData["id"]+'/" class="btn btn-xs">修改</a>');
                            var invalid = $('<a href="javascript:;" class="btn btn-xs btn-warning">停用</a>');
                            var delete_p = $('<a href="javascript:;" class="btn btn-xs btn-danger">删除</a>');
                            element.append(modify);
                            element.append(invalid);
                            element.append(delete_p);

                            invalid.on('click',function () {
                                var id = oData["id"];
                                var con = confirm("确定停用吗?");
                                if (con) {
                                    $.get("/product_management/update/invalid/" + id + "/", function (data) {
                                        if (data.success) {
                                            $.growlService("取消提交！", {type: "success"});
                                            location.href = "/product_management/page_new_product/";
                                        } else {
                                            $.growlService(data.error_messag, {type: "danger"});
                                        }
                                    })
                                }
                            });
                            delete_p.on('click',function () {
                                var id = oData["id"];
                                var con = confirm("确定删除吗?");
                                if (con) {
                                    $.get("/product_management/update/delete/" + id + "/", function (data) {
                                        if (data.success) {
                                            $.growlService("提交成功！", {type: "success"});
                                            location.href = "/product_management/page_new_product/";
                                        } else {
                                            $.growlService(data.error_messag, {type: "danger"});
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
            grid.setUrl("/product_management/update/data/");
            grid.submitFilter();
        });

        // handle filter cancel button click
        tableWrapper.on('click', '.filter-cancel', function (e) {
            e.preventDefault();
            $('.select').val('').trigger('change'); //select2 置空
            $('.dateFilter').val('');
            grid.resetFilter();
        });

        //全选按钮
        $(".checkall").click(function () {
            $("#update_table tr input[type='checkbox']").each(function () {
                var check = $(this).parent("span").hasClass("checked");
                if (!check) {
                    $(this).prop("checked", true).uniform('refresh');
                } else {
                    $(this).prop("checked", false).uniform('refresh');
                }
                $(this).parents("tr").toggleClass("selected")
            });
        });

        //多选停用按钮
        $("#invalid_many").on('click', function () {
            var checkedBox = $("input[type='checkbox']:checked");
            if (checkedBox.length < 1) {
                alert("请至少选择一项！");
                return
            } else {
                var con = confirm("确定提交吗?");
                if (con) {
                    // 选中全部通过
                    for (var i=0; i < checkedBox.length; i++) {
                        var data = $("#update_table").DataTable().row(i).data();
                        $.get("/product_management/update/invalid/" + data["id"] + "/", function (data) {
                        })
                    }
                    $.growlService("提交成功！", {type: "success"});
                    window.location.reload(true);
                }
            }
        });
        //多选删除按钮
        $("#delete_many").on('click', function () {
            var checkedBox = $("input[type='checkbox']:checked");
            if (checkedBox.length < 1) {
                alert("请至少选择一项");
                return
            } else {
                // 选中全部不通过
                var con = confirm("确定取消吗?");
                if (con) {
                    for (var i=0; i < checkedBox.length; i++) {
                        var data = $("#update_table").DataTable().row(i).data();
                        $.get("/product_management/update/delete/" + data["id"] + "/", function (data) {
                        })
                    }
                    $.growlService("取消提交", {type: "danger"});
                    window.location.reload(true);
                }
            }
        });
    };


    return {

        //main function to initiate the module
        init: function () {
            handleRecords();
        }

    };

}();
