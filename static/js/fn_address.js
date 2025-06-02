
 $(document).ready(function(){
    $.getJSON('/api/provinces', function (data) {
        data.forEach(function (prov) {
          $('#province').append(`<option value="${prov.id}">${prov.name}</option>`);
        });
      });
    $('#input_province').on('change', function () {
        const provinceId = $(this).val();
        $('#input_district').empty().append('<option value="">-- เลือกอำเภอ --</option>').prop('disabled', !provinceId);
        $('#input_subdistrict').empty().append('<option value="">-- เลือกตำบล --</option>').prop('disabled', true);

        if (provinceId) {
          $.getJSON(`/api/districts?province_id=${provinceId}`, function (data) {
            data.forEach(function (dist) {
              $('#district').append(`<option value="${dist.id}">${dist.name}</option>`);
            });
          });
        }
      });
    $('#input_district').on('change', function () {
        const districtId = $(this).val();
        $('#input_subdistrict').empty().append('<option value="">-- เลือกตำบล --</option>').prop('disabled', !districtId);

        if (districtId) {
          $.getJSON(`/api/subdistricts?district_id=${districtId}`, function (data) {
            data.forEach(function (subdist) {
              $('#subdistrict').append(`<option value="${subdist.id}">${subdist.name}</option>`);
            });
          });
        }
      });
    $('#input_subdistrict').on('change', function () {
        const subdistrictId = $(this).val();
        $('#input_zipcode').val('');

        if (subdistrictId) {
          $.getJSON(`/api/zipcodes?subdistrict_id=${subdistrictId}`, function (data) {
            if (data.length > 0) {
              $('#zipcode').val(data[0].zipcode);
            } else {
              $('#zipcode').val('');
            }
          });
        }
      });
    $('#input_zipcode').on('change', function () {
        const zipcode = $(this).val();
        if (zipcode) {
          $.getJSON(`/api/subdistricts?zipcode=${zipcode}`, function (data) {
            if (data.length > 0) {
              $('#subdistrict').val(data[0].id);
              $('#district').val(data[0].district_id);
              $('#province').val(data[0].province_id);
            } else {
              $('#subdistrict').val('');
              $('#district').val('');
              $('#province').val('');
            }
          });
        } else {
          $('#subdistrict').val('');
          $('#district').val('');
          $('#province').val('');
        }
      });
    });
