jQuery(document).ready(function($){
    $('body').prepend('<h1>hello Jquery</h1>');
});

function rollback(){
    jQuery(document).ready(function($){
        $('li').css('color','black');
    })
};
function class_red(){
    jQuery(document).ready(function($){
        $('.aa').css('color','red');
    })
};
function id_blue(){
    jQuery(document).ready(function($){
        $('#bb').css('color','blue');
    })
};
function load_email(){
    alert('aaa' + this.value)
}

