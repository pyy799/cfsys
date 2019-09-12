var TableExample = function () {

    var handleRecords = function () {
        var grid = new Datatable();
        //debugger;

        grid.init({
            src: $("#serviceTable"),
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
                //"sDom": "<'row-fluid inboxHeader'<'span6'<'dt_actions'>l><'span6'f>r>t<'row-fluid inboxFooter'<'span6'i><'span6'p>>", //待补充
                "pageLength": 50,//每页显示10条数据
                "bAutoWidth": false,//宽度是否自动，感觉不好使的时候关掉试试
                "bLengthChange": false,
                "bFilter": false,
                "ordering": true,
                "deferRender": false,
                // "serverSide":true,
                // "bProcessing": true, //开启读取服务器数据时显示正在加载中……特别是大数据量的时候，开启此功能比较好
                ajax: {
                    url: "/contract/contract_detail/service/data/" + $('#contractId').val() + "/"
                },
                //"bServerSide": true, //开启服务器模式，使用服务器端处理配置datatable。注意：sAjaxSource参数也必须被给予为了给datatable源代码来获取所需的数据对于每个画。 这个翻译有点别扭。开启此模式后，你对datatables的每个操作 每页显示多少条记录、下一页、上一页、排序（表头）、搜索，这些都会传给服务器相应的值。 
                //"sAjaxSource": "{{rootUrl}}", //给服务器发请求的url
                "aoColumns": [ //这个属性下的设置会应用到所有列，按顺序没有是空,bVisible是否可见
                    {"mData": "id", "sTitle": "ID", "bVisible": false, 'show': 'no'},
                    {"mData": "service_type_name", "sTitle": "服务类型"},
                    {"mData": "charge_type_name", "sTitle": "计费模式"},
                    {"mData": "prestore_amount", "sTitle": "预存总量"},
                    {"mData": "prestore_money", "sTitle": "预存总价"},
                    {"mData": "arranged_amount", "sTitle": "月保底量(G)"},
                    {"mData": "arranged_money", "sTitle": "月保底价格(元)"},
                    {"mData": "concurrence_amount", "sTitle": "并发总量(人)"},
                    {"mData": "concurrence_money", "sTitle": "并发总价(元)"},
                    {"mData": "over_type_name", "sTitle": "超出计费方式"},
                    {"mData": "over_price", "sTitle": "超出单价"},
                    {"mData": "over_unit", "sTitle": "超出单位"},
                    {"mData": "over_ladder", "sTitle": "超出阶梯"}
                ],
                "fnRowCallback": function (nRow, aData, iDisplayIndex) {// 当创建了行，但还未绘制到屏幕上的时候调用，通常用于改变行的class风格

                },
                "fnInitComplete": function (oSettings, json) { //表格初始化完成后调用 在这里和服务器分页没关系可以忽略

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
