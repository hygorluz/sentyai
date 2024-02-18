var previous_answer = null;

var default_qa_question = 'Please explain what is the SentyAI project and create a table with the top five benefits of using it.';


function update_answer_html(current_answer){
    $('#first-answer .question').html(current_answer.question);


    if (current_answer.refined_answer_html){
        $('#first-answer .answer').html(current_answer.refined_answer_html);
        $('#refine-answer').hide();
        $('#support').show();
    } else {
        $('#first-answer .answer').html(current_answer.answer_html);
    }


    let sources_html = "";

    for (let index = 0; index < previous_answer.sources.length; ++index) {
        let source_url = previous_answer.sources[index];
        let icon = "globe";
        if (source_url.toLowerCase().includes(".mp4")){
            icon = "video"
        }
        if (source_url.toLowerCase().includes(".doc") || source_url.toLowerCase().includes(".pdf")){
            icon = "file-text"
        }
        if (source_url.toLowerCase().includes(".mp3")){
            icon = "headphones"
        }
        sources_html = sources_html + '<div class="source-row"><a href="'+source_url+'" target="_blank" data-toggle="tooltip" data-placement="top" title="'+source_url+'"><div class="internalicon bg-dark"><i data-feather="'+icon+'"></i></div> '+source_url+'</a></div>';
    }
    sources_html = sources_html + ""
    $('#first-answer .sources').html("<b>Sources:</b><br/> " + sources_html);

    if (sources_html.length > 5) {
       $('#first-answer .sources').show();
    } else {
       $('#first-answer .sources').hide();
    }
    $('#first-answer').scrollTop(0);
    hljs.highlightAll();
}

function hide_everything(){
    $('#ask-a-question-form').prop('disabled', false);
    $('.ask-btn').prop('disabled', false);
    $('#question-input').prop('disabled', false);
    $('.ask-btn .loading-spinner').hide();

    $('#ask-a-question').hide();
    $('#loading-message-1').hide();
    $('#first-answer').hide();
    $('#loading-message-2').hide();
    $('#second-answer').hide();
    $('#failure-message').hide();
    $('#refine-answer').hide();
    $('#ask-a-question-btn').hide();
    $('#restart').hide();
    $('#support').hide();
    hljs.highlightAll();
}

function reset_qa(){
    $('#first-answer').scrollTop(0);
    hide_everything();
    $('#question-input').val(default_qa_question)
    $('#ask-a-question').show();
    $('#ask-a-question-btn').show();
    $('#first-answer').scrollTop(0);
    hljs.highlightAll();
}


function process_qa_response(response, result){

    hide_everything();

    if (result == "success") {
        previous_answer = response.responseJSON
        $('#refine-answer').hide(); // hide this
        $('#restart').show();
        update_answer_html(previous_answer)
        $('#first-answer').show();
        $('#first-answer').scrollTop(0);

        if (previous_answer.source_documents.length > 0) {
            $('#refine-answer').hide(); // hide this
            $('#support').hide();
        } else {
            $('#refine-answer').hide();
            $('#support').show();
        }
        $('#support').show(); // Show
        $('#first-answer .sources').hide();



    } else {
        $('#failure-message').show();
        $('#restart').show();
    }

    $('[data-toggle="tooltip"]').tooltip();
    feather.replace();
    hljs.highlightAll();
}


$(document).ready(function() {


    //FIRST
    $('#ask-a-question-btn').click(function(e) {
        e.preventDefault();

        if ($('#question-input').val().length < 10){
            $('#question-input').focus();
            return false;
        }

        $.ajax({
            type: "POST",
            url: "/ask",
            data: JSON.stringify({"question": $('#question-input').val(), "refine": false, "previous_answer": previous_answer}),
            complete: process_qa_response,
            contentType: "application/json; charset=utf-8",
            dataType: "json"
        });

        hide_everything();

        $('#loading-message-1').show();
        $('#ask-a-question-form').prop('disabled', true);
        $('.ask-btn').prop('disabled', true);
        $('#question-input').prop('disabled', true);
        $('.ask-btn .loading-spinner').show();


    });

    //REFINE
    $('#refine-answer').click(function(e) {
        e.preventDefault();

        if (!previous_answer){
            reset_qa();
            return false;
        }

        $.ajax({
            type: "POST",
            url: "/ask",
            data: JSON.stringify({"question": previous_answer.question, "refine": true, "previous_answer": previous_answer}),
            complete: process_qa_response,
            contentType: "application/json; charset=utf-8",
            dataType: "json"
        });

        hide_everything();

        $('#loading-message-2').show();
        $('#ask-a-question-form').prop('disabled', true);
        $('.ask-btn').prop('disabled', true);
        $('#question-input').prop('disabled', true);
        $('.ask-btn .loading-spinner').show();


    });

    //CHAT
    $('.bt-chat').click(function(e) {
        e.preventDefault();
        reset_qa();
    });

    //RESTART
    $('#restart').click(function(e) {
        e.preventDefault();
        reset_qa();
    });

    //INIT
    $('[data-toggle="tooltip"]').tooltip();
    feather.replace();
    hljs.highlightAll();

});


