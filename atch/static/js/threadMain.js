function parsePostBodies() {
    /*$('.post.body').each(function(i, el) {
        if (el.text().includes(">")) {

        }
    });*/
}


function addReplyTag(tag) {
    let text = $('textarea#body')
    text.append(">>" + tag)
    text.focus()
    console.log("eeee")
}


function refreshPosts() {

}


$(document).ready(function() {
    parsePostBodies();
})