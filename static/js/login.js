$(function(){
    //登录校验
    $("#bt_login_in").click(function(){
        //校验用户信息
        if($("#username").val()==""){
            //使用EasyUI的信息框进行提示
            $.messager.alert('登录提示',"用户名不能为空！","warning");
        }else if($("#password").val()==""){
            //使用EasyUI的信息框进行提示
            $.messager.alert('登录提示',"密码不能为空！","warning");
        }

        var message={
            "username":$("#username").val(),
            "password":$("#password").val(),
        }

        console.log(message);

        /*休眠方法*/
        var t = Date.now();
        function sleep(d){
            while(Date.now - t <= d);
            console.log(111);
        }

        var return_data;

        $.ajax({
            type:"post",
            url:"/login/login_in",
            data:{"Message":JSON.stringify(message)},
            //data:{"Message":message},
            success:function(return_data){
                console.log(return_data);
                if(return_data.code<0){
                    //$.messager.progress(10); 
                    $.messager.alert("登录提示",return_data.status,"error");
                    console.log("失败");
                    //window.location.href ="./login/login_in";
                } else {
                    //$.messager.progress(10); 
                    $.messager.alert("登录提示",return_data.status,"info");
                    console.log("成功");
                    window.location.href ="/index?Message="+JSON.stringify(message);
                }
          }
        });

    });

    //重置
    $("#bt_reset").click(function(){
        $("form").get(0).reset();
    })
});
