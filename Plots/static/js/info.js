$(document).on('click', 'a[class^="id"]', function(e) {
    e.preventDefault();
    var modal = document.getElementsByClassName("div_"+this.className)
    if(modal[0].style.display == "block"){
        modal[0].style.display = "none";
        return 0;
    }
    modal[0].style.display = "block";
});

$(document).on('click', 'a[class^="del_id"]', function(e) {
    e.preventDefault();
    //alert(e.target.className);
    var r = /\d+/;
    var str = e.target.className;
    var new_str = str.match(r);

});

