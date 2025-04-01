/** === DATA TABLE === */
$(document).ready(function() {
    $('#views-products-datatable').DataTable({
        "lengthMenu": [[10, 20, 30, 40, -1], [10, 20, 30, 40, "All"]],
       
        "columnDefs": [{
            "targets": [1, 2, ], // The columns to disable sorting (0-index based)
            "orderable": false
        }],
        "columns": [
            { "width": "15%" },
            { "width": "15%" },
            { "width": "20%" },
            { "width": "15%" },
            { "width": "15%" },
            { "width": "8%" },
            { "width": "12%" },               
        ],
        language: {
            "zeroRecords":    "Не найдено подходящих записей!",
            "search":         "Поиск:",
            "infoPostFix":    "",
            "info":      "",
            lengthMenu: '_MENU_ Количество записей',
            "paginate": {
                "first": "Первая",
                "last": "Последняя",
                "next": "Следующая",
                "previous": "Предыдущая"
            },
        },
        "order": [[5, 'asc'], [3, 'asc']],
        // buttons: [ 'copy', 'excel', 'pdf', 'print'],
    });
  });