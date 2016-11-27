function byId(document, idname) {
    try {
        return document.getElementById(idname).textContent;
    } catch(err) {
        return '';
    }
}

function getFields() {

}

function PostIt(doc_root) {
    var fields = getFields();
    var html = byId(doc_root, 'missiontitle');
    return html;
}

chrome.runtime.sendMessage({
    action: "postIt",
    source: PostIt(document)
});

