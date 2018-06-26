
var var_table
function getdata(){
  $.getJSON("http://127.0.0.1:5000/table", function(data){
      var_table = data
  })
  setTimeout(function(){
  reload()
   }, 10);
}
