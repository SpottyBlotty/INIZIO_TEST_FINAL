document.addEventListener('DOMContentLoaded', () => {
    const searchForm = document.getElementById('searchForm');
    const queryInput = document.getElementById('queryInput');
    const statusDiv = document.getElementById('status');
    const resultsTableBody = document.querySelector('#resultsTable tbody');
    const downloadCsvBtn = document.getElementById('downloadCsvBtn');

    let lastData = null;

    searchForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        statusDiv.textContent = "Status: Loading...";
        
        try {
            const response = await fetch(`/api/search?q=${encodeURIComponent(queryInput.value)}`);
            const data = await response.json();
            lastData = data;

            resultsTableBody.innerHTML = data.results.map(res => `
                <tr>
                    <td>${res.position}</td>
                    <td><b>${res.title}</b></td>
                    <td><a href="${res.link}" target="_blank">Link</a></td>
                    <td>${res.snippet}</td>
                </tr>
            `).join('');

            statusDiv.textContent = `Status: Found ${data.results.length} results`;
            downloadCsvBtn.disabled = false;
            downloadCsvBtn.disabled = false;
downloadJsonBtn.disabled = false; // Добавь вот это!
        } catch (err) {
            statusDiv.textContent = "Status: Error";
        }
    });

    downloadCsvBtn.addEventListener('click', async () => {
        const response = await fetch('/api/export/csv', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(lastData)
        });

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = "results.csv";
        a.click();
    });

});
