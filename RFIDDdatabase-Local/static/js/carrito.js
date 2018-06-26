var productoscarrito
var currentboleta

$.getJSON("http://127.0.0.1:5000/compras", function(data){
    productoscarrito = data["json_productos"]
})

$.getJSON("http://127.0.0.1:5000/numboleta", function(data){
  currentboleta = parseInt(data)
  $("#numboleta").text(data)
})

function update(){
  window.location.reload(false)
}





function endReceipt(){
  $.ajax({
      url: '/numboleta',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({"numeroboleta":currentboleta+1}),
      dataType: 'json'
  });

  window.location.reload(false)
/*
  $.post("/numboleta", send, function(data){
    alert(data);
  }, "json");
  */
}

$(function(){

    $("#gridContainer").dxDataGrid({
        dataSource: productoscarrito,
        //keyExpr: "ID",
        //selection: {
            //mode: "single"
        //},
        columns: [{
                dataField: "UID_Code",
                width: 130,
                caption: "UID_Code"
            },
            "Nombre_Producto",  {
                dataField: "Precio",
                alignment: "right",
                format: "currency"
            }
        ],
        summary: {
            totalItems: [{
                column: "UID_Code",
                summaryType: "count"
            }, {
                column: "Precio",
                summaryType: "sum",
                valueFormat: "currency"
            }]
        }
    });
});
