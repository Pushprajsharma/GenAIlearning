function showSection(sectionId) {
    document.querySelectorAll('.section').forEach(section => {
        section.style.display = 'none';
    });
    document.getElementById(sectionId).style.display = 'block';
}

async function uploadFile() {
    let btn = document.getElementById('extract')
    btn.disabled = true;
    document.getElementById('result').innerHTML = "<p>Loading...</p>";
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    if (!file) {
        alert("Please select a file");
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('http://127.0.0.1:5000/upload', {
        method: 'POST',
        body: formData
    });

    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = "";
    resultDiv.innerHTML += "<h3>Extracted Performance Requirements</h3>";

    if (response.ok) {
        const result = await response.json();
        if (!result || result.trim().length == 0) {
            resultDiv.innerHTML += "<p>No performance requirements found</p>";
            btn.disabled = false;
            return;
        }

        // const ul = document.createElement('ul');
        // result.split('\n').forEach(text => {
        //     if (text.trim().length > 0) {
        //         const li = document.createElement('li');
        //         li.innerHTML = text;
        //         ul.appendChild(li);
        //     }
        // });
        // resultDiv.appendChild(ul);

        resultDiv.innerHTML += result;

    } else {
        const result = await response.json();
        resultDiv.innerHTML = `<p style="color: red;">${result.error}</p>`;
    }
    
    btn.disabled = false;
}

// function exportToWord() {
   
// }

document.getElementById('Export').addEventListener('click', ()=>{
    console.log("Export to word called")
    const resultDiv = document.getElementById('result');
    const content = resultDiv.innerHTML;

    const header = "<html xmlns:o='urn:schemas-microsoft-com:office:office' " +
                   "xmlns:w='urn:schemas-microsoft-com:office:word' " +
                   "xmlns='http://www.w3.org/TR/REC-html40'>" +
                   "<head><meta charset='utf-8'><title>Export HTML to Word Document</title></head><body>";
    const footer = "</body></html>";
    const sourceHTML = header + content + footer;

    const source = 'data:application/vnd.ms-word;charset=utf-8,' + encodeURIComponent(sourceHTML);
    const fileDownload = document.createElement("a");
    document.body.appendChild(fileDownload);
    fileDownload.href = source;
    fileDownload.download = 'test_cases.doc';
    fileDownload.click();
    document.body.removeChild(fileDownload);
});


