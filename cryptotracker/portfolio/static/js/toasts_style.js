$(document).ready(function () {
    $(".toast-warning").css("background-color", "#fbf0da");
    $(".toast-warning").css("color", "#73510d");
    $(".toast-warning").css("border-color", "#f9e4be");

    $(".toast-success").css("background-color", "#d6f0e0");
    $(".toast-success").css("color", "#0d6832");
    $(".toast-success").css("border-color", "#c0e7d0");

    $(".toast-info").css("background-color", "#def1f7");
    $(".toast-info").css("color", "#1c657d");
    $(".toast-info").css("border-color", "#c6e6f1");

    $(".toast-error").css("background-color", "#f9e1e5");
    $(".toast-error").css("color", "#af233a");
    $(".toast-error").css("border-color", "#f4c8cf");

    $(".toast").toast('show');
});