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
        if(result.length == 0) {
            resultDiv.innerHTML += "<p>No performance requirements found</p>";
            btn.disabled = false;
            return;
        }

        count  = 1;
        const paragraph = document.createElement('p');
        paragraph.innerHTML = result;
        resultDiv.appendChild(paragraph);
        paragraph.innerHTML = `<span style="background-color: #ffff4c;">${result}</span>`;
        // result.forEach(text => {
        //     const paragraph = document.createElement('p');
        //     paragraph.innerHTML = `<span style="background-color: #ffff4c;">${text}</span>`;
        //     resultDiv.appendChild(paragraph);
        //     count++;
        // });

    } else {
        const result = await response.json();
        resultDiv.innerHTML = `<p style="color: red;">${result.error}</p>`;
    }
    
    btn.disabled = false;
}
