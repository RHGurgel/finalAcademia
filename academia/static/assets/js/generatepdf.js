document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('generatePDF').addEventListener('click', function() {

        // --- INÍCIO DA CORREÇÃO ---

        // 1. Encontra todos os elementos com a classe .no-print
        const elementosParaEsconder = document.querySelectorAll('.no-print');

        // 2. Esconde cada um deles antes de gerar o PDF
        elementosParaEsconder.forEach(el => {
            el.style.display = 'none';
        });

        // --- FIM DA CORREÇÃO ---

        // Elemento que será convertido em PDF
        const element = document.getElementById('content-to-print');

        // Suas opções de configuração do PDF
        const opt = {
            margin: 10, // Aumentei a margem para um visual melhor
            filename: 'meu-documento.pdf',
            image: { type: 'jpeg', quality: 0.98 },
            html2canvas: { scale: 2 },
            jsPDF: { unit: 'mm', format: 'a4', orientation: 'landscape' } // Paisagem é melhor para tabelas
        };

        // Gera o PDF e garante que os elementos reapareçam no final
        html2pdf().set(opt).from(element).save().finally(function () {

            // --- INÍCIO DA CORREÇÃO ---

            // 3. Mostra os elementos novamente na tela após a geração do PDF
            elementosParaEsconder.forEach(el => {
                el.style.display = ''; // Remove o estilo 'display: none'
            });

            // --- FIM DA CORREÇÃO ---
        });
    });
});