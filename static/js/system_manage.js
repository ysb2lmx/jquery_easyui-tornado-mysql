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
    console.log("系统信息管理");

})
