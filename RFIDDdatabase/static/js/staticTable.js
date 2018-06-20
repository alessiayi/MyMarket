$( document ).ready(function() {

    $(function(){
        $("#gridContainer").dxDataGrid({
            dataSource: var_table,
            columns: ["id", "UID_Code", "Nombre_Producto", "Precio", "Stock"]
        });
    });

});

