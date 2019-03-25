// 函数参数必须是字符串，因为二代身份证号码是十八位，而在javascript中，十八位的数值会超出计算范围，造成不精确的结果，导致最后两位和计算的值不一致，从而该函数出现错误。
//身份证号验证
function checkIDCard(idcode){
    // 加权因子
    var weight_factor = [7,9,10,5,8,4,2,1,6,3,7,9,10,5,8,4,2];
    // 校验码
    var check_code = ['1', '0', 'X' , '9', '8', '7', '6', '5', '4', '3', '2'];
    var code = idcode + "";
    var last = idcode[17];//最后一个
    var seventeen = code.substring(0,17);
    // ISO 7064:1983.MOD 11-2
    // 判断最后一位校验码是否正确
    var arr = seventeen.split("");
    var len = arr.length;
    var num = 0;
    for(var i = 0; i < len; i++){
        num = num + arr[i] * weight_factor[i];
    }
    // 获取余数
    var resisue = num%11;
    var last_no = check_code[resisue];
    // 格式的正则
    // 正则思路
    /*
     第一位不可能是0
     第二位到第六位可以是0-9
     第七位到第十位是年份，所以七八位为19或者20
     十一位和十二位是月份，这两位是01-12之间的数值
     十三位和十四位是日期，是从01-31之间的数值
     十五，十六，十七都是数字0-9
     十八位可能是数字0-9，也可能是X
     */
    var idcard_patter = /^[1-9][0-9]{5}([1][9][0-9]{2}|[2][0][0|1][0-9])([0][1-9]|[1][0|1|2])([0][1-9]|[1|2][0-9]|[3][0|1])[0-9]{3}([0-9]|[X])$/;
    // 判断格式是否正确
    var format = idcard_patter.test(idcode);
    // 返回验证结果，校验码和格式同时正确才算是合法的身份证号码
    return last === last_no && format ? true : false;
}

//加载方法
$(function(){
    //失去焦点事件
    $("input",$("#certificate_number").next("span")).blur(function(){ 
        var snumber = $("#certificate_number").textbox('getValue');
        console.log(snumber);
        if(checkIDCard(snumber)){
            $.messager.show({title:"提示",msg:"证件号码验证正确",showType:"show",timeout:1000});
            $('#certificate_number').validatebox({required:false});
        }else{
            $("#certificate_number").textbox('clear')
            //$('#certificate_number').textbox({required:true});
            $.messager.alert("提示","证件号码验证失败，请重新检查证件号码","error");
        };
    }); 


    $('#gender').combobox('setValue', ['']);


    $('#issue_date').datebox({
        formatter:function (date) {
            return date.getFullYear() + '-' + date.getMonth() + '-' + date.getDate();
        },
        onSelect: function(date){
            //$('#issue_date').datebox('setValue',date.getFullYear()+"-"+(date.getMonth()+1)+"-"+date.getDate());
            console.log(date.getFullYear()+"-"+(date.getMonth()+1)+"-"+date.getDate());
        }
    });

    $.fn.datebox.defaults.formatter = function(date){
        var y = date.getFullYear();
        var m = date.getMonth()+1;
        var d = date.getDate();
        return m+'-'+d+'-'+y;
    }

    //console.log($('#issue_date').text(date));

    //form提交
    $('#add').click(function(){
        $.messager.progress();
        console.log($('#customer_form').serializeArray());
        var v = $('#customer_form').serializeArray();//获取表单数据,并进行转化
        $.ajax({
            type: "post",
            url:"customer_form_add",
            data: JSON.stringify(v),
            //data:$('#customer_form').serialize(),
            success: function(data){
                console.log(data);
                $.messager.progress('close');
                $.messager.alert("提示","客户信息新增成功","info");
            }
        });
    });




});

   