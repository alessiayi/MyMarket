
var productoscarrito
var currentboleta

function begin(){
  $.getJSON("/compras", function(data){
      productoscarrito = data["json_productos"]
  })

  $.getJSON("/numboleta", function(data){
    currentboleta = parseInt(data)
    $("#numboleta").text(data)
  })

  rest()
}


function update(){
  begin()
  //window.location.reload(false)
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
function rest(){
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

}

$(document).ready(begin());
