
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
