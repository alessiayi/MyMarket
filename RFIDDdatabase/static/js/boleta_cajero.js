var productoscarrito = $.getJSON("/compras")["json_productos"]
var currentboleta = parseInt($.getJSON("/numboleta"))
$("#numboleta").text(currentboleta)

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
        columns: [{
                dataField: "UID_Code",
                width: 130,
                caption: "UID_Code"
            },
            "Nombre_Producto",
            {
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
