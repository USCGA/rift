// Call the dataTables jQuery plugin
$(document).ready(function() {
  $('#dataTable').DataTable(
    {
      "order": [[ 3, "desc" ]]
    }
  );
});
