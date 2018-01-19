/**
 * Created by Administrator on 2017/11/10.
 */

$(function () {
	$('#registerForm').bootstrapValidator({
		message: 'This value is not valid',
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
            },
        fields: {
        	username: {
        		message: '用户名验证失败',
        		validators: {
        			notEmpty: {
        				message: '用户名不能为空'
        			},
        			stringLegnth: {
        				min: 	6,
        				max: 18,
        				message: '用户名长度必须在6到30之间'
        			},
        			regexp: {
        				regexp: /^[a-zA-Z0-9_\.]+$/,
        				message: '用户名由数字字母下划线和.组成'
        			}
        		}
        	},
        	password: {
        		message: '密码无效',
        		validators: {
        			notEmpty: {
        				message: '密码不能为空'
        			},
        			stringLegnth: {
        				min: 6,
        				max: 18,
        				message: '密码长度必须在6到18之间'	
        			},
        			different: {
        				field: 'username',
        				message: '不能和用户名相同'
        			},
        			regexp: {
                        regexp: /^[a-zA-Z0-9_\.]+$/,
                        message: 'The username can only consist of alphabetical, number, dot and underscore'
                    }
                }
        	},
        	repeatpassword: {
                message: '密码无效',
                validators: {
                    notEmpty: {
                        message: '用户名不能为空'
                    },
                    stringLength: {
                        min: 6,
                        max: 30,
                        message: '用户名长度必须在6到30之间'
                    },
                    // identical: {//相同
                    //     field: 'password',
                    //     message: '两次密码不一致'
                    // },
                    different: {//不能和用户名相同
                        field: 'username',
                        message: '不能和用户名相同'
                    },
                    regexp: {//匹配规则
                        regexp: /^[a-zA-Z0-9_\.]+$/,
                        message: 'The username can only consist of alphabetical, number, dot and underscore'
                    }
                }
            }
        }
	})
});