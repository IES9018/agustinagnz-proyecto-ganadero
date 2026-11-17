const form = document.querySelector("#stock-form");
const lista = document.querySelector("#stock-list");
const selectorEstablecimiento = document.querySelector(
    "#stock-establecimiento"
);
const mensaje = document.querySelector("#stock-message");

const mensajeAlertas = document.querySelector(
    "#mensaje-alertas-stock"
);
const listaAlertas = document.querySelector(
    "#lista-alertas-stock"
);

let establecimientos = [];

function mostrarMensaje(texto, error = false) {
    mensaje.textContent = texto;
    mensaje.classList.toggle("is-error", error);
    mensaje.classList.toggle("is-success", !error);
}

async function respuestaApi(url, opciones = {}) {
    const respuesta = await fetch(url, {
        ...opciones,
        headers: {
            "Content-Type": "application/json",
            ...(opciones.headers || {})
        }
    });

    const datos = await respuesta.json().catch(() => ({}));

    if (!respuesta.ok) {
        throw new Error(
            datos.detail || "No se pudo completar la operación."
        );
    }

    return datos;
}

function obtenerEstadoStock(item) {
    if (Number(item.cantidad) <= Number(item.stock_minimo)) {
        return {
            texto: "Crítico",
            clase: "stock-estado-critico"
        };
    }

    return {
        texto: "Normal",
        clase: "stock-estado-normal"
    };
}

async function cargarEstablecimientos() {
    establecimientos = await respuestaApi(
        "/api/establecimientos"
    );

    selectorEstablecimiento.replaceChildren();

    const activos = establecimientos.filter(
        item => item.estado === "activo"
    );

    const opcionInicial = document.createElement("option");
    opcionInicial.value = "";
    opcionInicial.textContent = activos.length
        ? "Seleccione un establecimiento"
        : "No hay establecimientos activos";

    selectorEstablecimiento.append(opcionInicial);

    for (const establecimiento of activos) {
        const opcion = document.createElement("option");
        opcion.value = establecimiento.id_establecimiento;
        opcion.textContent =
            `${establecimiento.nombre} — ${establecimiento.ubicacion}`;

        selectorEstablecimiento.append(opcion);
    }

    selectorEstablecimiento.disabled = activos.length === 0;
}

function agregarCelda(fila, texto) {
    const celda = document.createElement("td");
    celda.textContent = texto ?? "";
    fila.append(celda);
    return celda;
}

function agregarEstadoStock(fila, item) {
    const estado = obtenerEstadoStock(item);
    const celda = document.createElement("td");
    const indicador = document.createElement("span");

    indicador.className = estado.clase;
    indicador.textContent = estado.texto;

    celda.append(indicador);
    fila.append(celda);
}

function crearControlMovimiento(item) {
    const celda = document.createElement("td");

    const cantidad = document.createElement("input");
    cantidad.type = "number";
    cantidad.min = "0.001";
    cantidad.step = "any";
    cantidad.placeholder = "Cantidad";
    cantidad.setAttribute(
        "aria-label",
        `Cantidad del movimiento para ${item.tipo_insumo}`
    );

    const ingreso = document.createElement("button");
    ingreso.type = "button";
    ingreso.textContent = "Ingreso";
    ingreso.addEventListener("click", () => {
        registrarMovimiento(
            item.id_stock,
            "ingreso",
            cantidad.value
        );
    });

    const salida = document.createElement("button");
    salida.type = "button";
    salida.textContent = "Salida";
    salida.addEventListener("click", () => {
        registrarMovimiento(
            item.id_stock,
            "salida",
            cantidad.value
        );
    });

    const controles = document.createElement("div");
    controles.className = "stock-movement-controls";
    controles.append(cantidad, ingreso, salida);
    celda.append(controles);

    return celda;
}

async function cargarStock() {
    lista.replaceChildren();

    const filaCarga = document.createElement("tr");
    agregarCelda(filaCarga, "Cargando inventario...").colSpan = 8;
    lista.append(filaCarga);

    try {
        const items = await respuestaApi("/api/stock");
        lista.replaceChildren();

        if (!items.length) {
            const fila = document.createElement("tr");
            agregarCelda(
                fila,
                "Todavía no hay insumos registrados."
            ).colSpan = 8;

            lista.append(fila);
            return;
        }

        for (const item of items) {
            const fila = document.createElement("tr");

            agregarCelda(fila, item.tipo_insumo);
            agregarCelda(fila, item.categoria);
            agregarCelda(fila, String(item.cantidad));
            agregarEstadoStock(fila, item);
            agregarCelda(fila, item.unidad);
            agregarCelda(fila, item.ubicacion);

            const establecimiento = establecimientos.find(
                e => Number(e.id_establecimiento)
                    === Number(item.id_establecimiento)
            );

            agregarCelda(
                fila,
                establecimiento
                    ? establecimiento.nombre
                    : `ID ${item.id_establecimiento}`
            );

            fila.append(crearControlMovimiento(item));
            lista.append(fila);
        }
    } catch (error) {
        lista.replaceChildren();

        const fila = document.createElement("tr");
        agregarCelda(fila, error.message).colSpan = 8;
        lista.append(fila);
    }
}

async function cargarAlertasStock() {
    listaAlertas.replaceChildren();

    try {
        const alertas = await respuestaApi("/api/stock/alertas");

        if (!alertas.length) {
            mensajeAlertas.textContent =
                "No hay insumos en estado crítico.";
            return;
        }

        mensajeAlertas.textContent =
            `Se encontraron ${alertas.length} alertas críticas.`;

        for (const alerta of alertas) {
            const tarjeta = document.createElement("article");
            tarjeta.className =
                "sanidad-alerta status-danger";

            const titulo = document.createElement("strong");
            titulo.textContent = alerta.tipo_insumo;

            const establecimiento = document.createElement("p");
            establecimiento.textContent =
                `Establecimiento: ${alerta.establecimiento}`;

            const existencia = document.createElement("p");
            existencia.textContent =
                `Existencia: ${alerta.cantidad} ${alerta.unidad}`;

            const umbral = document.createElement("p");
            umbral.textContent =
                `Umbral crítico: ${alerta.stock_minimo} ${alerta.unidad}`;

            tarjeta.append(
                titulo,
                establecimiento,
                existencia,
                umbral
            );

            listaAlertas.append(tarjeta);
        }
    } catch (error) {
        mensajeAlertas.textContent =
            `No se pudieron cargar las alertas: ${error.message}`;
    }
}

async function registrarMovimiento(
    stockId,
    tipoOperacion,
    valor
) {
    const cantidad = Number(valor);

    if (!Number.isFinite(cantidad) || cantidad <= 0) {
        mostrarMensaje(
            "Ingresá una cantidad mayor que cero para el movimiento.",
            true
        );
        return;
    }

    try {
        const actualizado = await respuestaApi(
            `/api/stock/${stockId}/movimientos`,
            {
                method: "POST",
                body: JSON.stringify({
                    tipo_operacion: tipoOperacion,
                    cantidad
                })
            }
        );

        mostrarMensaje(
            `Stock actualizado. Nueva existencia: ${actualizado.cantidad} ${actualizado.unidad}.`
        );

        await Promise.all([
            cargarStock(),
            cargarAlertasStock()
        ]);
    } catch (error) {
        mostrarMensaje(error.message, true);
    }
}

form.addEventListener("submit", async evento => {
    evento.preventDefault();

    const datos = Object.fromEntries(
        new FormData(form).entries()
    );

    datos.categoria =
        document.getElementById("stock-categoria").value;

    datos.stock_minimo =
        Number(document.getElementById("stock-minimo").value);

    datos.cantidad = Number(datos.cantidad);
    datos.id_establecimiento =
        Number(datos.id_establecimiento);

    try {
        const creado = await respuestaApi("/api/stock", {
            method: "POST",
            body: JSON.stringify(datos)
        });

        mostrarMensaje(
            `Insumo "${creado.tipo_insumo}" registrado.`
        );

        form.reset();

        await Promise.all([
            cargarStock(),
            cargarAlertasStock()
        ]);
    } catch (error) {
        mostrarMensaje(error.message, true);
    }
});

document.querySelector("#stock-refresh").addEventListener(
    "click",
    async () => {
        await Promise.all([
            cargarStock(),
            cargarAlertasStock()
        ]);
    }
);

async function iniciarStock() {
    try {
        await cargarEstablecimientos();

        await Promise.all([
            cargarStock(),
            cargarAlertasStock()
        ]);
    } catch (error) {
        mostrarMensaje(
            `No se pudo iniciar el módulo de stock: ${error.message}`,
            true
        );
    }
}

iniciarStock();