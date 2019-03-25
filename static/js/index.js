/*网页js功能*/
$(function() {
    var treeData = [];

    //初始化获取用户名和密码
    $.ajax({
        type:"post",
        url:"/index/get_user_info",
        data:{},
        success:function(data){
            console.log(data);
            //渲染界面元素
            $("#username").html(data.data.username);

            //var canvasList = document.getElementById('treeMenu');
            //console.log(canvasList);
            //html_tmp = '<li> <span>购物网站</span> <ul>'
            //         + '<li data-options="">淘宝网</li>'
            //         + '<li data-options="">京东网</li>'
            //         + '<li data-options="">苏宁购</li>'
            //         + '</ul> </li> ';
            //console.log(html_tmp);
            //var canvas_append = document.createElement('canvas');
            //canvasList.appendChild(html_tmp);

        }
    });
    console.log("test");


    /********************************************/
    //动态树形菜单数据(js赋值)
/*
    var treeData = [{
          text : "",
          children : [{
                  text : "客户信息",
                  children : [{
                          text : "个人客户信息新增",
                          attributes : {
                              url : '<iframe width="100%" height="100%" frameborder="0"  src="jsp/queryPriceStock.jsp" style="width:100%;height:100%;margin:0px 0px;"></iframe>'
                          }
                      }, {
                          text : "个人客户信息查询",
                          attributes : {
                              url : ''
                          }
                      }
                  ]
              },{
                  text : "资金信息",
                  children : [{
                          text : "总量统计",
                          attributes : {
                              url : '<iframe width="100%" height="100%" frameborder="0"  src="jsp/queryPriceStock.jsp" style="width:100%;height:100%;margin:0px 0px;"></iframe>'
                          }
                      }, {
                          text : "总量统计2",
                          attributes : {
                              url : ''
                          }
                      }
                  ]
              }
          ]
      }
    ];
*/


    //菜单数据
    //var treeData = [{
    //        'id' : "customer_add",
    //        'text' : "客户信息新增",
    //        'attributes' : {
    //            //url:'<iframe width="100%" height="100%" frameborder="0"  src="http://www.baidu.com" style="width:100%;height:100%;margin:0px 0px;"></iframe>'
    //            'url':'<iframe width="100%" height="100%" frameborder="0"  src="/customer" style="width:100%;height:100%;margin:0px 0px;"></iframe>'
    //        },
    //    },{
    //        text : "客户信息查询"
    //    }
    //];

    //菜单数据后台获取
    function treeData_load(tree_type){
        $.ajax({
            type:"post",
            url:"/index/get_menus_info",
            data:{"Message":JSON.stringify({"tree_type":tree_type})},
            success:function(data){
                treeData = data.data;
                if(tree_type=="customer_tree"){
                    $('#customer_tree').tree('loadData', treeData);
                } else if (tree_type=="system_tree"){
                    $('#system_tree').tree('loadData', treeData);

                } else{
                    console.log("无法识别的树种类");
                }
            }
        });
    }
    
    //实例化客户信息树形菜单
    $("#customer_tree").tree({
        data : treeData_load("customer_tree"),//要加载的节点数据
        lines : true,//定义是否显示树线条
        animate : true,//定义当节点展开折叠时是否显示动画效果。
        checkbox : false,//定义是否在每个节点前边显示复选框。
        method : "post",//检索数据的 http 方法（method）。post
        cascadeCheck : true,//定义是否级联检查。
        dnd : true,//定义是否启用拖放。
        //formatter : "",//定义如何呈现节点文本。
        //loader : ,//定义如何从远程服务器加载数据。返回 false 则取消该动作。
        //loadFilter : ,//返回要显示的过滤数据。返回数据时以标准树格式返回的。
        //当用户点击一个节点时触发
        onClick : function (node) {
            console.log(node);
            treeData_load("customer_tree");
            if (node.attributes) {
                //打开链接地址(打开选项卡)
                Open(node.text, node.attributes.url);
            }
        },
    });



    //实例化资产信息树形菜单
/*
    $("#asset_tree").tree({
        data : treeData_load("资产信息"),//要加载的节点数据
        lines : true,//定义是否显示树线条
        animate : true,//定义当节点展开折叠时是否显示动画效果。
        checkbox : false,//定义是否在每个节点前边显示复选框。
        method : "post",//检索数据的 http 方法（method）。post
        cascadeCheck : true,//定义是否级联检查。
        dnd : true,//定义是否启用拖放。
        //formatter : "",//定义如何呈现节点文本。
        //loader : ,//定义如何从远程服务器加载数据。返回 false 则取消该动作。
        //loadFilter : ,//返回要显示的过滤数据。返回数据时以标准树格式返回的。
        //当用户点击一个节点时触发
        onClick : function (node) {
            console.log(node);
            if (node.attributes) {
                //打开链接地址
                Open(node.text, node.attributes.url);
            }
        },
    });
*/

    //实例化系统信息树形菜单
    $("#system_tree").tree({
        data : treeData_load("system_tree"),//要加载的节点数据
        lines : true,//定义是否显示树线条
        animate : true,//定义当节点展开折叠时是否显示动画效果。
        checkbox : false,//定义是否在每个节点前边显示复选框。
        method : "post",//检索数据的 http 方法（method）。post
        cascadeCheck : true,//定义是否级联检查。
        dnd : true,//定义是否启用拖放。
        //formatter : "",//定义如何呈现节点文本。
        //loader : ,//定义如何从远程服务器加载数据。返回 false 则取消该动作。
        //loadFilter : ,//返回要显示的过滤数据。返回数据时以标准树格式返回的。
        //当用户点击一个节点时触发
        onClick : function (node) {
            console.log(node);
            if (node.attributes) {
                //打开链接地址
                Open(node.text, node.attributes.url);
            }
        },
    });



    //js代码新增折叠慢板
    $('#menu_tree').accordion('add', {
        title: 'New Title',
        content: 'New Content',
        selected: false,
        //data-options:"fit:true,border:false,animate:true"
    });

    //在右边center区域打开菜单，新增tab
    function Open(text, url) {
        if ($("#div_tabs").tabs('exists', text)) {
            //$('#div_tabs').tabs('select', text);
            $('#div_tabs').tabs('add', {
                title : text,
                closable : true,
                collapsible: true,//是否可以折叠按钮
                content : url,//打开url
            });
        } else {
            $('#div_tabs').tabs('add', {
                title : text,
                closable : true,
                collapsible: true,//是否可以折叠按钮
                content : url,//打开url
            });
        }
    }
    
    //绑定tabs的右键菜单
    //$("#div_tabs").tabs({
    //    tools:[{
    //            iconCls:'icon-add',
    //            handler:function(){
    //                alert('点击添加')
    //            }
    //        },{
    //            iconCls:'icon-save',
    //            handler:function(){
    //                alert('点击保存')
    //            }
    //    }],
    //    onContextMenu : function (e, title) {
    //        e.preventDefault();
    //        $('#tabsMenu').menu('show', {
    //            left : e.pageX,
    //            top : e.pageY
    //        }).data("tabTitle", title);
    //    }
    //});
    
    //实例化menu的onClick事件
    $("#tabsMenu").menu({
        onClick : function (item) {
            CloseTab(this, item.name);
        }
    });
    
    //几个关闭事件的实现
    function CloseTab(menu, type) {
        var curTabTitle = $(menu).data("tabTitle");
        var tabs = $("#div_tabs");
        
        if (type === "close") {
            tabs.tabs("close", curTabTitle);
            return;
        }
        
        var allTabs = tabs.tabs("div_tabs");
        var closeTabsTitle = [];
        
        $.each(allTabs, function () {
            var opt = $(this).panel("options");
            if (opt.closable && opt.title != curTabTitle && type === "Other") {
                closeTabsTitle.push(opt.title);
            } else if (opt.closable && type === "All") {
                closeTabsTitle.push(opt.title);
            }
        });
        
        for (var i = 0; i < closeTabsTitle.length; i++) {
            tabs.tabs("close", closeTabsTitle[i]);
        }
    }

    /********************************************/




    //退出功能
    $("#n_title_out").click(function() {
        //提示用户是否确定退出
        $.messager.confirm("确认对话框", "你真的要退出吗？", function(r) {
            //退出
            if (r) {
                window.location.href = "/login/login_in";
            }
        })
    });

    //修改密码
    $("#n_title_pwd").click(function() {
        //打开修改密码窗口
        $("#div_pwd").window("open");
    });

    //确认修改密码
    $("#btnCon").click(function() {
        //校验原有密码
        if ($(":password:eq(0)").val() == "") {
            $.messager.alert("原有密码", "原有密码不能为空！", "warning");
        } else if ($(":password:eq(1)").val() == "") {
            //校验新密码
            $.messager.alert("新密码", "新密码不能为空！", "warning");
        } else if ($(":password:eq(2)").val() == "") {
            //校验确认密码
            $.messager.alert("确认密码", "确认密码不能为空！", "warning");
        } else if ($(":password:eq(1)").val() != $(":password:eq(2)").val()) {
            //校验两次密码
            $.messager.alert("密码校验", "两次密码不一致！", "error");
        } else {
            //关闭密码窗口
            $("#div_pwd").window("close");
            //$.messager.alert("密码修改","密码修改成功！","info");
            $.messager.show({
                title: '密码修改',
                msg: '密码修改成功，新密码为:'+$(":password:eq(2)").val(),
                timeout: 3000,
                showType: 'slide'
            });
        }
    })

    //取消密码修改
    $("#btnCan").click(function(){
        $("#div_pwd").window("close");
    })

})
