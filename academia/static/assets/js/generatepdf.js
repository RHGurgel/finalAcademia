document.addEventListener('DOMContentLoaded', function() {
            document.getElementById('generatePDF').addEventListener('click', function() {

                const element = document.getElementById('content-to-print');


                const opt = {
                    margin: 1,
                    filename: 'meu-documento.pdf',
                    image: { type: 'jpeg', quality: 0.98 },
                    html2canvas: { scale: 2 },
                    jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
                };

                html2pdf().set(opt).from(element).save();
            });
        });