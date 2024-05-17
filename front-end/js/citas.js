$(document).ready(function () {
  var API_URL = "http://127.0.0.1:5000";
  var idPaciente = new URLSearchParams(window.location.search).get("id");



  // DataTable initialization code...
  var table = $("#tablaCitas").DataTable({
    ajax: {
      url: API_URL + "/api/get_citas_by_patient/" + parseInt(idPaciente),
    },
    error: function (xhr, status, error) {
      console.log("Error al obtener los datos del API:", error);
    },
    columns: [
      { data: "id_cita" },
      { data: "fecha_cita" },
      { data: "hora_cita" },
      {
        data: null,
        render: function (data, type, row) {
          return row.medico.nombre;
        },
      },
      {
        data: null,
        render: function (data, type, row) {
          return row.medico.especializacion;
        },
      },
      {
        data: null,
        render: function (data, type, row, meta) {
          return '<button type="button" class="btn btn-danger btn-delete">Eliminar</button>';
        }
      }
    ],
  });

  $("#btn-volver").on("click", function () {
    window.location.href = "index.html";
  });
  $("#btn-add-new").on('click', function () {
    $("#addCitaModal").modal("show");
    $.ajax({
      url: API_URL + '/api/get_medicos',
      method: "GET",
      dataType: "json",
      success: function ({data}) {
        // Populate select element with options
        $.each(data, function (index, medico) {
          $("#medicos").append(
            $("<option>", {
              value: medico.id_medico,
              text: medico.nombre,
            })
          );
        });
      },
      error: function (xhr, status, error) {
        console.error("Error cargando los medicos:", error);
      },
    });
  });
  $("#btnAdd").on("click", function () {
    // Get data from the form
    var formData = {};
    $.each($("#addForm").serializeArray(), function (_, kv) {
      formData[kv.name] = kv.value;
    });

    const data = {
      fecha_cita: formData.fechaCita,
      hora_cita: formData.horaCita,
      id_medico: +formData.medicos,
      id_paciente: +idPaciente
    };
    // Send AJAX request to update patient data
    $.ajax({
      url: API_URL + "/api/new_cita",
      method: "POST",
      contentType: "application/json", // Set the content type to JSON
      data: JSON.stringify(data), // Use the serialized form data directly
      success: function (response) {
        // Close the modal
        $("#addCitaModal").modal("hide");
        // Reload or update the DataTable to reflect the changes
        table.ajax.reload();
      },
      error: function (xhr, status, error) {
        console.log("Error updating citas data:", error);
      },
    });
    console.log("after request");
  });

  $("#tablaCitas").on("click", ".btn-delete", function () {
    var row = $(this).closest("tr");

    deleteRow(row);
  });

  function deleteRow(row) {
    var id = row.find("td:first").text(); // Assuming the ID is in the first column
    $.ajax({
      url: API_URL + "/api/del_cita/" + id, // Replace this URL with your actual delete endpoint
      type: "DELETE",
      success: function (response) {
        // If the deletion was successful, remove the row from the table
        row.remove();
        console.log("Record deleted successfully");
      },
      error: function (xhr, status, error) {
      },
    });
  }
});
