"use strict";


(($) => {


    $(() => {

        let changeZoomAjax;

        $("form").bind("submit", (event) => {
            if (!event.currentTarget[0].value) event.currentTarget[0].disabled = true;
            if (!event.currentTarget[1].value) event.currentTarget[1].disabled = true;
            // if (event.currentTarget[2].value === "__all__") event.currentTarget[2].disabled = true;
            // if (event.currentTarget[3].value === "__all__") event.currentTarget[3].disabled = true;
            // if (event.currentTarget[4].value === "__all__") event.currentTarget[4].disabled = true;
        });

        // $(".controllable").bind("change", (event) => {
        //     let target = event.currentTarget,
        //         field = $(target),
        //         tr = field.closest("tr"),
        //         date = new Date(tr.data("date")),
        //         data = {};
        //     if (field.data("name") === "expected_payment_date") {
        //         let expected_payment_date = new Date(field.val());
        //         data[field.data("name")] = `${expected_payment_date.getDate()}.${expected_payment_date.getMonth() + 1}.${expected_payment_date.getFullYear()}`;
        //     } else if (field.data("name") === "on_control") {
        //         data[field.data("name")] = target.checked ? 1 : 0;
        //     } else {
        //         data[field.data("name")] = field.val();
        //     }
        //     $(".controllable").attr("disabled", "disabled");
        //     if (changeZoomAjax) {
        //         if (target !== changeZoomAjax.field[0]) {
        //             if (changeZoomAjax.field.data("name") === "on_control") {
        //                 changeZoomAjax.field[0].checked = `${changeZoomAjax.field.data("value")}` === "1";
        //             } else {
        //                 changeZoomAjax.field.val(changeZoomAjax.field.data("value"));
        //             }
        //         }
        //         changeZoomAjax.abort();
        //     }
        //     changeZoomAjax = $.ajax({
        //         url: `/api/change-zoom/${tr.data("manager_id")}/${tr.data("lead")}/${date.getDate()}.${date.getMonth()+1}.${date.getFullYear()}`,
        //         type: "POST",
        //         data: data,
        //         success: (data, status) => {
        //             if (status === "success") {
        //                 field.closest("tr").find(".estimate").text(data.estimate);
        //                 field.data("value", field.val());
        //                 field.closest("td").addClass("success");
        //                 if (target.changeZoomTimeout) clearTimeout(target.changeZoomTimeout);
        //                 target.changeZoomTimeout = setTimeout(() => {
        //                     field.closest("td").removeClass("success");
        //                 }, 1000);
        //             }
        //         },
        //         error: () => {
        //             field.val(field.data("value"));
        //             field.closest("td").addClass("error");
        //             if (target.changeZoomTimeout) clearTimeout(target.changeZoomTimeout);
        //             target.changeZoomTimeout = setTimeout(() => {
        //                 field.closest("td").removeClass("error");
        //             }, 1000);
        //         },
        //         complete: () => {
        //             $(".controllable").attr("disabled", null);
        //             changeZoomAjax = undefined;
        //         }
        //     });
        //     changeZoomAjax.field = field;
        // });

    });


})(jQuery);
