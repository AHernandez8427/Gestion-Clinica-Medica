$(document).ready(function () {
  var API_URL = 'http://127.0.0.1:5000'
  // DataTable initialization code...
  var table = $("#tablaDatos").DataTable({
    ajax: {
      url: API_URL + "/api/get_pacientes",
    },
    error: function (xhr, status, error) {
      console.log("Error al obtener los datos del API:", error);
    },
    columns: [
      { data: "id_paciente" },
      { data: "nombre" },
      { data: "fecha_nacimiento" },
      { data: "datos_medicos" },
      {
        data: null,
        render: function (data, type, row, meta) {
          return `<button type="button" class="btn btn-secondary btn-add" data-id="${row.id_paciente}">Citas</button>
                <button type="button" class="btn btn-primary btn-edit" data-id="${row.id_paciente}">Editar</button>
                <button type="button" class="btn btn-danger btn-delete"  data-id="${row.id_paciente}">Eliminar</button>
                `;
        },
      },
    ],
  });

  // Handle click event for edit buttons
  $("#tablaDatos").on("click", ".btn-edit", function () {
    console.log("click working");
    var pacienteId = $(this).data("id");
    // Logic to open modal and populate form with data based on pacienteId
    openEditModal(pacienteId);
  });

  $("#tablaDatos").on("click", ".btn-add", function () {
    // Get the value of the data-id attribute
    var id = $(this).data('id');
    // Redirect the user to another HTML file with the id as a query parameter
    window.location.href = 'citas.html?id=' + id;
  });



  $("#btn-add-new").on('click', function () {
    $("#addModal").modal("show");
  });
  $("#btnAdd").on("click", function () {
    // Get data from the form
    var formData = {};
    $.each($("#addForm").serializeArray(), function (_, kv) {
      formData[kv.name] = kv.value;
    });
    const data = {
      nombre: formData.nombre,
      fecha_nacimiento: formData.fechaNacimiento,
      datos_medicos: formData.datosMedicos,
    };
    if (!data.fecha_nacimiento)
      alert("Porfavor seleccione una fecha de nacimiento");
    console.log("before request", data);
    // Send AJAX request to update patient data
    $.ajax({
      url: API_URL + "/api/new_paciente",
      method: "POST",
      contentType: "application/json", // Set the content type to JSON
      data: JSON.stringify(data), // Use the serialized form data directly
      success: function (response) {
        // Close the modal
        $("#editModal").modal("hide");
        // Reload or update the DataTable to reflect the changes
        table.ajax.reload();
        console.log("Patient data Added successfully");
      },
      error: function (xhr, status, error) {
        console.log("Error updating patient data:", error);
      },
    });
    console.log("after request");
  });
  // Function to open edit modal
  // Attach click event handler for "Guardar Cambios" button outside the openEditModal function
  $("#btnSaveChanges").on("click", function () {
    // Get data from the form
    var formData = {};
    $.each($("#editForm").serializeArray(), function (_, kv) {
      formData[kv.name] = kv.value;
    });
    const data = {
      id_paciente: formData.pacienteId,
      nombre: formData.nombre,
      fecha_nacimiento: formData.fechaNacimiento,
      datos_medicos: formData.datosMedicos,
    };
    if (!data.fecha_nacimiento)
      alert("Porfavor seleccione una fecha de nacimiento");
    console.log("before request", data);
    // Send AJAX request to update patient data
    $.ajax({
      url: API_URL + "/api/update_paciente",
      method: "POST",
      contentType: "application/json", // Set the content type to JSON
      data: JSON.stringify(data), // Use the serialized form data directly
      success: function (response) {
        // Close the modal
        $("#editModal").modal("hide");
        // Reload or update the DataTable to reflect the changes
        table.ajax.reload();
        console.log("Patient data updated successfully");
      },
      error: function (xhr, status, error) {
        console.log("Error updating patient data:", error);
      },
    });
    console.log("after request");
  });

  // Function to open edit modal
  function openEditModal(id) {
    // You can use AJAX to fetch data for the patient with the given id
    $.ajax({
      url: API_URL + "/api/get_paciente/" + id,
      method: "GET",
      success: function (response) {
        // Populate modal form with data from response
        $("#nombre").val(response.nombre);
        $("#fechaNacimiento").val(response.fecha_nacimiento);
        $("#datosMedicos").val(response.datos_medicos);
        $("#pacienteId").val(id);

        // Show the modal
        $("#editModal").modal("show");
      },
      error: function (xhr, status, error) {
        console.log("Error fetching patient data:", error);
      },
    });
  }

  // Handle click event for delete buttons
  $("#tablaDatos").on("click", ".btn-delete", function () {
    var row = $(this).closest("tr");

    deleteRow(row);
  });

  // Function to delete row
  function deleteRow(row) {
    var id = row.find("td:first").text(); // Assuming the ID is in the first column
    $.ajax({
      url: API_URL + "/api/del_paciente/" + id, // Replace this URL with your actual delete endpoint
      type: "DELETE",
      success: function (response) {
        // If the deletion was successful, remove the row from the table
        row.remove();
        console.log("Record deleted successfully");
      },
      error: function (xhr, status, error) {
        alert("Paciente no se puede borrar debido a que tiene citas.");
      },
    });
  }
});
