
function begin(){
  var boletas
  $.getJSON("/boletas", function(data){
    boletas = data["todo"]
  })
  rest()
}


function rest(){
  $(function(){
      var dataGrid = $("#gridContainer").dxDataGrid({
          dataSource: boletas,
          allowColumnReordering: true,
          grouping: {
              autoExpandAll: true,
          },
          searchPanel: {
              visible: true
          },
          paging: {
              pageSize: 10
          },
          groupPanel: {
              visible: true
          },
          columns: [
              "UID_Code",
              "Nombre_Producto",
              //"Precio",
              {
                dataField: "Precio",
                alignment: "right",

              },
              {
                  dataField: "Numero_Boleta",
                  groupIndex: 0
              }
          ]
      }).dxDataGrid("instance");

      $("#autoExpand").dxCheckBox({
          value: true,
          text: "Expand All Groups",
          onValueChanged: function(data) {
              dataGrid.option("grouping.autoExpandAll", data.value);
          }
      });
  });
}

$(document).ready(begin());
