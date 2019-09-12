var redraw = function(data, th){}();

var TableExample = function () {
    var handleRecords = function (th, data, is_first) {
        var base_th = [
            {
                "mData": null,
                'show': 'no',
                //"sTitle": '<input class="checkall" name="" type="checkbox" value="">',
                "fnCreatedCell": function (nTd, sData, oData, iRow, iCol) {
                    var element = $(nTd).empty();
                    element.append("<input type='checkbox' name='checkList' />");
                }
            },
            {"mData": "id", 'show': 'no', "sTitle": "ID", "bVisible": false},
            {"mData": "contract_number", "sTitle": "合同编号"},
            {"mData": "sign_type", "sTitle": "合同类型"},
            {"mData": "customer", "sTitle": "客户名称"},
            {"mData": "customer_id", "sTitle": "财务账号"},
            {"mData": "business", "sTitle": "企业类型"},
            {"mData": "account", "sTitle": "账号", "fnCreatedCell": function (nTd, sData, oData, iRow, iCol) {
                var element = $(nTd).empty();
                var show_str = sData;
                if (sData.length > 35) {
                    show_str = show_str.substring(0, 35);
                }
                element.append("<span title=" + sData + ">" + show_str + "</span>");
            }},
            {"mData": "salesman", "sTitle": "销售负责人"},
            {"mData": "depart", "sTitle": "销售部门"},
            {"mData": "customer_service", "sTitle": "客服"},
            {"mData": "service_type_name", "sTitle": "服务类型"},
            {"mData": "charge_type_name", "sTitle": "计费类型"},
            {"mData": "contract_date", "sTitle": "服务日期"},
            {"mData": "arranged_amount", "sTitle": "月保底量", "bVisible": false},
            {"mData": "arranged_money", "sTitle": "月保底费用", "bVisible": false},
            {"mData": "prestore_amount", "sTitle": "预存总量", "bVisible": false},
            {"mData": "prestore_money", "sTitle": "预存总费用", "bVisible": false},
            {"mData": "concurrence_amount", "sTitle": "并发量", "bVisible": false},
            {"mData": "concurrence_money", "sTitle": "并发费用", "bVisible": false},
            {"mData": "over_type_name", "sTitle": "超出计费方式", "bVisible": false},
            {"mData": "over_price", "sTitle": "超出单价", "bVisible": false},
            {"mData": "over_unit", "sTitle": "超出单位", "bVisible": false},
            {"mData": "over_ladder", "sTitle": "超出阶梯", "fnCreatedCell": function (nTd, sData, oData, iRow, iCol) {
                var element = $(nTd).empty();
                var show_str = sData;
                if (sData.length > 35) {
                    show_str = sData.substring(0, 35);
                }
                element.append("<span title=" + sData + ">" + show_str + "</span>");
            }, "bVisible": false},
            {"mData": "month_function_money", "sTitle": "月基础功能费", "bVisible": false}
        ];
        var grid = new Datatable();
        th = base_th.concat(th);
        //debugger;
        grid.init({
            src: $("#example"),
            onSuccess: function (grid) {
                // execute some code after table records loaded
            },
            onError: function (grid) {
                // execute some code on network or other general error  
            },
            onDataLoad: function(grid) {
                // execute some code on ajax data load
            },
            dataTable:{
                "sPaginationType": "simple_numbers",   //分页风格，full_number会把所有页码显示出来（大概是，自己尝试）
                //"sDom": "<'row-fluid inboxHeader'<'span6'<'dt_actions'>l><'span6'f>r>t<'row-fluid inboxFooter'<'span6'i><'span6'p>>", //待补充
                "pageLength": 10,//每页显示10条数据
                "bAutoWidth": false,//宽度是否自动，感觉不好使的时候关掉试试
                "bLengthChange": false,
                "bFilter": false,
                "ordering":true,
                "deferRender": false,
                "serverSide":false,
                data: data,
                // "bProcessing": true, //开启读取服务器数据时显示正在加载中……特别是大数据量的时候，开启此功能比较好
                // ajax: {
                //    url: "/finance/common/info/data/"
                // },
                //"bServerSide": true, //开启服务器模式，使用服务器端处理配置datatable。注意：sAjaxSource参数也必须被给予为了给datatable源代码来获取所需的数据对于每个画。 这个翻译有点别扭。开启此模式后，你对datatables的每个操作 每页显示多少条记录、下一页、上一页、排序（表头）、搜索，这些都会传给服务器相应的值。
                //"sAjaxSource": "{{rootUrl}}", //给服务器发请求的url
                "aoColumns": th,
                "fnRowCallback": function(nRow, aData, iDisplayIndex) {// 当创建了行，但还未绘制到屏幕上的时候调用，通常用于改变行的class风格 
                    
                },
                "fnInitComplete": function(oSettings, json) { //表格初始化完成后调用 在这里和服务器分页没关系可以忽略
                    
                }
            }
        });
        // tablecell 显示与隐藏
        tableTellShow = function(){
            var columns = grid.getColumns();
            var html = '';
            $.each(columns, function(key, val){
                if (val.show != 'no'){
                    if (key > 1 && key <= 13) {
                        html += "<div class='col-sm-3'><label class='checkbox-inline'>";
                        html += "<input type='checkbox' data-column=" + key + " class='tableCell' checked>" + val.sTitle + "";
                        html += "</div>";
                    }
                    else if (key > 13 && key <= 24) {
                        html += "<div class='col-sm-3'><label class='checkbox-inline'>";
                        html += "<input type='checkbox' data-column=" + key + " class='tableCell'>" + val.sTitle + "";
                        html += "</div>";
                    }
                    else if (val.sTitle.indexOf("使用量") != -1 && html.indexOf("使用量") == -1) {
                        html += "<div class='col-sm-3'><label class='checkbox-inline'>";
                        html += "<input type='checkbox' data-column=" + key + " class='tableCell' checked>使用量";
                        html += "</div>";
                    }
                    else if (val.sTitle.indexOf("收费") != -1 && html.indexOf("收费") == -1) {
                        html += "<div class='col-sm-3'><label class='checkbox-inline'>";
                        html += "<input type='checkbox' data-column=" + key + " class='tableCell' checked>收费";
                        html += "</div>";
                    }
                    else if (val.sTitle.indexOf("开票") != -1 && html.indexOf("开票") == -1) {
                        html += "<div class='col-sm-3'><label class='checkbox-inline'>";
                        html += "<input type='checkbox' data-column=" + key + " class='tableCell' checked>开票";
                        html += "</div>";
                    }
                    else if (val.sTitle.indexOf("回款") != -1 && html.indexOf("回款") == -1) {
                        html += "<div class='col-sm-3'><label class='checkbox-inline'>";
                        html += "<input type='checkbox' data-column=" + key + " class='tableCell' checked>回款";
                        html += "</div>";
                    }
                }
            });

            $(".showOrNot").empty();
            $(".showOrNot").append(html);
            $(".takeAll").on("click", function(){
                $("#container .showOrNot input[type=checkbox]").each(function(key, val){
                    if ($(val).prop("checked")){}
                    else { $(val).prop("checked", true).trigger("change"); }
                })
            });
            $(".clearAll").on("click", function(){
                $("#container .showOrNot input[type=checkbox]").each(function(key, val){
                    if (!$(val).prop("checked")){}
                    else { $(val).prop("checked", false).trigger("change"); }
                })
            });
            $(".antiSelect").on("click", function(){
                $("#container .showOrNot input[type=checkbox]").each(function(key, val){
                    if ($(val).prop("checked")) {
                        $(val).prop("checked", false).trigger("change");
                    }
                    else {
                        $(val).prop("checked", true).trigger("change");
                    }
                })
            });
        };
        tableTellShow();

        // 控制checkbox改变的时候datatable中格的显示/隐藏
        $('.tableCell').on('change', function (e) {
            e.preventDefault();
            // 获得checkbox改变的列
            var k = $(this).attr('data-column');
            if (k > 24) {
                // 所有使用量、收费、开票、回款列
                $.each(columns, function (key, val) {
                    if (key >= k && (key - k) % 4 == 0) {
                        var column = grid.getDataTable().column(key);
                        column.visible(!column.visible());
                    }
                })
            }
            else {
                // 其他列
                var column = grid.getDataTable().column(k);
                column.visible(!column.visible());
            }
        });

        var tableWrapper = grid.getTableWrapper();
        // handle filter submit button click
        tableWrapper.on('click', '.filter-submit', function (e) {
            e.preventDefault();
            // only set no reload
            var fil_params = [];
            var fil_params_dict = {};
            $('.date').each(function (index, val) {
                if ($(this).val()) {
                    fil_params_dict[$(this).data('key')] = $(this).val();
                }
            });
            for (var k in fil_params_dict) {
                if (fil_params_dict.hasOwnProperty(k)) {
                    fil_params.push('' + k + '=' + fil_params_dict[k]);
                }
            }

            var params = grid.submitFilter();

            $.ajax({
                type: 'post',
                url: "/finance/finance_detail/data/?" + fil_params.join('&') + "",
                data: {"action": 'filter', "filter": JSON.stringify(params["filter"])},
                success: function (data) {
                    grid.getDataTable().destroy();
                    $("#example").empty();
                    var html = $("#wraper").html();
                    $("#container").prepend(html);

                    TableExample.init(data.data.th, data.data.data, true);

                    $("#container .select").select2({"width": "145px"});
                    $("#container .dateFilter").datepicker({autoclose: true, format: "yyyy-mm-dd"});
                    $("#container .monthFilter").datepicker({autoclose: true, format: "yyyy-mm"});

                    $("#container input[type=text]").each(function () {
                        var name = $(this).attr("name");
                        var key = $(this).data("key");

                        if (!name) {
                            $(this).val(fil_params_dict[key]);
                        } else {
                            $(this).val(params['filter'][name]);
                        }
                    })
                }
            })
        });

        // handle filter cancel button click
        tableWrapper.on('click', '.filter-cancel', function (e) {
            e.preventDefault();
            $('.select').val('').trigger('change');
            $('.dateFilter').val('');
            $('.monthFilter').val('');
            grid.resetFilter();
        });

        if (!is_first) {
            //点击复选框,选中行
            $("#example").on('change', 'tr input[name="checkList"]', function () {
                var $tr = $(this).parents('tr');
                var check = $(this).prop("checked");
                if (!check) {
                    $(this).prop("checked", true).uniform('refresh');
                } else {
                    $(this).prop("checked", false).uniform('refresh');
                }
                $tr.toggleClass('selected');
            });
            //单击行，选中复选框
            $("#example").delegate('tr', 'click', function (e) {
                e.preventDefault();
                if ($(this).hasClass('selected')) {
                    $(this).removeClass("selected")
                } else {
                    $(this).addClass('selected');
                }

                var check_box = $(this).find("input[type='checkbox']");
                if (check_box.attr("class") == "checkall") {
                    return
                }
                var check = $(this).find("input[type='checkbox']").prop("checked");
                if (!check) {
                    $(this).find("input[type='checkbox']").prop("checked", true).uniform('refresh');
                } else {
                    $(this).find("input[type='checkbox']").prop("checked", false).uniform('refresh');
                }
            });
        }

        //全选按钮
        $(".checkall").click(function () {
            $("#example tr input[type='checkbox']").each(function () {
                var check = $(this).parent("span").hasClass("checked");
                if (!check) {
                    $(this).prop("checked", true).uniform('refresh');
                } else {
                    $(this).prop("checked", false).uniform('refresh');
                }
                $(this).parents("tr").toggleClass("selected")
            });
        });

        //取消选择
        $(".clearall").click(function () {
            $("#example tr input[type='checkbox']").each(function () {
                $(this).prop("checked", false).uniform('refresh');
            });
        });

        //导出按钮
        $(".btnExport").on('click', function () {
            var ott = $("#example").DataTable().rows(".selected");
            if (ott[0].length < 1) {
                alert("请至少选择一行进行导出!!!");
                return
            }
            var default_tr_th = $("#example").DataTable().table().header().innerHTML;
            var default_tr_td = '';
            $.each(ott.nodes(), function (key, val) {
                default_tr_td += ('<tr>' + val.innerHTML + '</tr>');
            });
            $("#example").excelexportjs({
                containerid: "example",
                datatype: 'table',
                default_tr_th: default_tr_th,
                default_tr_td: default_tr_td
            });
        });

        return grid;
    };

    var handleDatePickers = function () {
        if (jQuery().datepicker) {
            $('.date-picker').datepicker({
                rtl: Metronic.isRTL(),
                orientation: "left",
                autoclose: true,
                format:"yyyy-mm-dd"
            });
            //$('body').removeClass("modal-open"); // fix bug when inline picker is used in modal
        }

        /* Workaround to restrict daterange past date select: http://stackoverflow.com/questions/11933173/how-to-restrict-the-selectable-date-ranges-in-bootstrap-datepicker */
    };


    return {
        //main function to initiate the module
        init: function (th, data, is_first) {
            var grid = handleRecords(th, data, is_first);
            handleDatePickers();
            return grid
        }

    };

}();
