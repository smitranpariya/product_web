$(document).ready(function() {
    $("#customer").validate();
 });

 
 jQuery(document).ready(function() {
    jQuery("#customer").validate({
       rules: {
          doc_number: 'required',
          first_name: 'required',
          last_name:'required',
          sim_card:'required',
          offer_id:'required',
          last_name:'required',
          last_name:'required',
          u_email: {
             required: true,
             email: true,//add an email rule that will ensure the value entered is valid email id.
             maxlength: 255,
          },

       }
    });
 });