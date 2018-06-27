

var var_table
function getdata(){
  $.getJSON("/table", function(data){
      var_table = data
  })
  setTimeout(function(){
  reload()
   }, 10);
}



getdata()
function reload(){
  setTimeout(function(){
  $("#gridContainer").dxDataGrid({
      columns: ["id", "UID_Code", "Nombre_Producto", "Precio", "Stock"],
      dataSource: var_table,
  });
  }, 10);
}

//alert("Usted no está apto para realizar cambios")
$(document).ready(reload());
