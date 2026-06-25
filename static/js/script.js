document.addEventListener("DOMContentLoaded", () => {
    const pago = document.getElementById("pago");
    const statusTexto = document.getElementById("status-texto");

    const dataInput = document.getElementById("data");
    const btnHoje = document.getElementById("btn-hoje");
    const btnOntem = document.getElementById("btn-ontem");
    const btnOutros = document.getElementById("btn-outros");

    const valorCard = document.getElementById("valor-card");
    const valorInput = document.getElementById("valor");

    const atualizarStatus = () => {
        if (!pago || !statusTexto) return;
        
        const textoAtivo = pago.dataset.textoAtivo || "Pago";
        const textoInativo = pago.dataset.textoInativo || "Não foi pago";
        
        statusTexto.textContent = pago.checked ? textoAtivo : textoInativo;
    };

    const formatarData = (data) => {
        const ano = data.getFullYear();
        const mes = String(data.getMonth() + 1).padStart(2, "0");
        const dia = String(data.getDate()).padStart(2, "0");

        return `${ano}-${mes}-${dia}`;
    };

    const ativarBotao = (botao) => {
        if (!btnHoje || !btnOntem || !btnOutros) return;

        btnHoje.classList.remove("active");
        btnOntem.classList.remove("active");
        btnOutros.classList.remove("active");

        botao.classList.add("active");
    };

    if (pago && statusTexto) {
        atualizarStatus();
        pago.addEventListener("change", atualizarStatus);
    }

    if (dataInput && btnHoje && btnOntem && btnOutros) {
        if (!dataInput.value) {
            dataInput.value = formatarData(new Date());
        }

        btnHoje.addEventListener("click", () => {
            const hoje = new Date();

            dataInput.value = formatarData(hoje);
            ativarBotao(btnHoje);
        });

        btnOntem.addEventListener("click", () => {
            const ontem = new Date();

            ontem.setDate(ontem.getDate() - 1);

            dataInput.value = formatarData(ontem);
            ativarBotao(btnOntem);
        });

        btnOutros.addEventListener("click", () => {
            ativarBotao(btnOutros);

            if (dataInput.showPicker) {
                dataInput.showPicker();
            } else {
                dataInput.focus();
                dataInput.click();
            }
        });

        dataInput.addEventListener("change", () => {
            ativarBotao(btnOutros);
        });
    }

    if (valorInput) {
       valorInput.addEventListener("input", () => {
           let valor = valorInput.value.replace(/\D/g, "");

           valor = (Number(valor) / 100).toLocaleString("pt-BR", {
               minimumFractionDigits: 2,
               maximumFractionDigits: 2
           });

           valorInput.value = valor;
       });
    }   

    if (valorCard && valorInput) {
        valorCard.addEventListener("click", () => {
            valorInput.focus();
        });
    }

    const btnExcluir = document.getElementById("btn-excluir");
    const overlayExcluir = document.getElementById("overlay-excluir");
    const btnCancelar = document.getElementById("btn-cancelar");

    if (overlayExcluir) {

        overlayExcluir.addEventListener("click", (e) => {

            if (e.target === overlayExcluir) {
                overlayExcluir.classList.remove("show");
            }

        });

    }
    
    if (btnExcluir && overlayExcluir && btnCancelar) {

        btnExcluir.addEventListener("click", (e) => {
            e.preventDefault();
            overlayExcluir.classList.add("show");
        });

        btnCancelar.addEventListener("click", () => {
            overlayExcluir.classList.remove("show");
        });

    }

    const formProtegido = document.querySelector("form[data-proteger-saida='true']");
    let formularioAlterado = false;
    let formularioEnviado = false;

    if (formProtegido) {
        const campos = formProtegido.querySelectorAll("input, select, textarea");

        campos.forEach((campo) => {
            campo.addEventListener("change", () => {
                formularioAlterado = true;
            });

            campo.addEventListener("input", () => {
                formularioAlterado = true;
            });
        });

        formProtegido.addEventListener("submit", () => {
            formularioEnviado = true;
        });

        window.addEventListener("beforeunload", (e) => {
            if (formularioAlterado && !formularioEnviado) {
                e.preventDefault();
                e.returnValue = "";
            }
        });
    }

    document.querySelectorAll(".menu-acoes").forEach(botao => {
        botao.addEventListener("click", (e) => {
            e.stopPropagation();

            const menu = botao.nextElementSibling;

            if (!menu || !menu.classList.contains("acoes-menu")) return;

            const aberto = menu.classList.contains("show");

            document.querySelectorAll(".acoes-menu").forEach((m) => {
                m.classList.remove("show");
            });

            if (!aberto) {
                menu.classList.add("show");
            }

        });

    });

    document.addEventListener("click", () => {
        document.querySelectorAll(".acoes-menu").forEach(menu => {
            menu.classList.remove("show");
        });

    });

    // Menu add
    const menuButton = document.getElementById("menu-add-button");
    const menuOptions = document.getElementById("menu-add-options");

    if (menuButton && menuOptions) {

        menuButton.addEventListener("click", function(e){
            e.stopPropagation();
            menuOptions.classList.toggle("show");
        });

        document.addEventListener("click", function(e){

            if(!menuOptions.contains(e.target) && e.target !== menuButton){
                menuOptions.classList.remove("show");
            }

        });

    }

    // Animação de saldo
    const saldo = document.querySelector(".money-counter");
    if (saldo) {
        const valorFinal = Number(saldo.dataset.valor);
        
        let valorInicial = Number(
            localStorage.getItem("ultimoSaldo")
        );

        if (isNaN(valorInicial)) {
            valorInicial = 0;
        }

        const duracao = 900;
        const inicio = performance.now();

        const formatarMoeda = (valor) => {
            return valor.toLocaleString("pt-BR", {
                style: "currency",
                currency: "BRL"
            });
        };

        const animar = (tempoAtual) => {

            const progresso = Math.min(
                (tempoAtual - inicio) / duracao,
                1
            );

            const valorAtual =
                valorInicial +
                (valorFinal - valorInicial) * progresso;

            saldo.textContent = formatarMoeda(valorAtual);

            if (progresso < 1) {
                requestAnimationFrame(animar);
            } else {
                saldo.textContent = formatarMoeda(valorFinal);

                localStorage.setItem(
                    "ultimoSaldo",
                    valorFinal
                );
            }
        };

        requestAnimationFrame(animar);
    }

    // Gráficos
    // Despesas
    const dadosGraficoDespesas = document.getElementById("dados-grafico-despesas");
    const canvasDespesas = document.getElementById("grafico-despesas-categoria");

    if (dadosGraficoDespesas && canvasDespesas) {
        const labels = JSON.parse(dadosGraficoDespesas.dataset.labels);
        const valores = JSON.parse(dadosGraficoDespesas.dataset.valores);
        const cores = JSON.parse(dadosGraficoDespesas.dataset.cores);

        new Chart(canvasDespesas, {
            type: "doughnut",
            data: {
                labels: labels,
                datasets: [{
                    data: valores,
                    backgroundColor: cores,
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                cutout: "65%",
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    }

    // Receitas
    const dadosGraficoReceitas = document.getElementById("dados-grafico-receitas");
    const canvasReceitas = document.getElementById("grafico-receitas-categoria");

    if (dadosGraficoReceitas && canvasReceitas) {
        const labels = JSON.parse(dadosGraficoReceitas.dataset.labels);
        const valores = JSON.parse(dadosGraficoReceitas.dataset.valores);
        const cores = JSON.parse(dadosGraficoReceitas.dataset.cores);

        new Chart(canvasReceitas, {
            type: "doughnut",
            data: {
                labels: labels,
                datasets: [{
                    data: valores,
                    backgroundColor: cores,
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                cutout: "65%",
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    }

    // Comparativo
    const dadosComparativo = document.getElementById("dados-grafico-comparativo");
    const canvasComparativo = document.getElementById("grafico-comparativo");

    if (dadosComparativo && canvasComparativo) {
        const labels = JSON.parse(dadosComparativo.dataset.labels);
        const receitas = JSON.parse(dadosComparativo.dataset.receitas);
        const despesas = JSON.parse(dadosComparativo.dataset.despesas);
        const saldo = JSON.parse(dadosComparativo.dataset.saldo);

        new Chart(canvasComparativo, {
            type: "line",
            data: {
                labels: labels,
                datasets: [
                    {
                        label: "Receitas",
                        data: receitas,
                        borderColor: "#16a34a",
                        backgroundColor: "rgba(22,163,74,.12)",
                        tension: .35
                    },
                    {
                        label: "Despesas",
                        data: despesas,
                        borderColor: "#ef4444",
                        backgroundColor: "rgba(239,68,68,.12)",
                        tension: .35
                    },
                    {
                        label: "Saldo",
                        data: saldo,
                        borderColor: "#2563eb",
                        backgroundColor: "rgba(37,99,235,.12)",
                        tension: .35
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: "bottom"
                    }
                }
            }
        });
    }
        
});