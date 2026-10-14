const form = document.querySelector("#stock-form");
const lista = document.querySelector("#stock-list");
const selectorEstablecimiento = document.querySelector(
    "#stock-establecimiento"
);
const mensaje = document.querySelector("#stock-message");

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
        throw new Error(datos.detail || "No se pudo completar la operación.");
    }

    return datos;
}

async function cargarEstablecimientos() {
    establecimientos = await respuestaApi("/api/establecimientos");
    selectorEstablecimiento.replaceChildren();

    const opcionInicial = document.createElement("option");
    opcionInicial.value = "";
    opcionInicial.textContent = establecimientos.length
        ? "Seleccione un establecimiento"
        : "No hay establecimientos registrados";
    selectorEstablecimiento.append(opcionInicial);

    for (const establecimiento of establecimientos) {
        const opcion = document.createElement("option");
        opcion.value = establecimiento.id_establecimiento;
        opcion.textContent = `${establecimiento.nombre} — ${establecimiento.ubicacion}`;
        selectorEstablecimiento.append(opcion);
    }

    selectorEstablecimiento.disabled = establecimientos.length === 0;
}

function agregarCelda(fila, texto) {
    const celda = document.createElement("td");
    celda.textContent = texto ?? "";
    fila.append(celda);
    return celda;
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
        registrarMovimiento(item.id_stock, "ingreso", cantidad.value);
    });

    const salida = document.createElement("button");
    salida.type = "button";
    salida.textContent = "Salida";
    salida.addEventListener("click", () => {
        registrarMovimiento(item.id_stock, "salida", cantidad.value);
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
    agregarCelda(filaCarga, "Cargando inventario...");
    filaCarga.firstElementChild.colSpan = 6;
    lista.append(filaCarga);

    try {
        const items = await respuestaApi("/api/stock");
        lista.replaceChildren();

        if (!items.length) {
            const fila = document.createElement("tr");
            const celda = agregarCelda(
                fila,
                "Todavía no hay insumos registrados."
            );
            celda.colSpan = 6;
            lista.append(fila);
            return;
        }

        for (const item of items) {
            const fila = document.createElement("tr");
            agregarCelda(fila, item.tipo_insumo);
            agregarCelda(fila, String(item.cantidad));
            agregarCelda(fila, item.unidad);
            agregarCelda(fila, item.ubicacion);

            const establecimiento = establecimientos.find(
                (e) => e.id_establecimiento === item.id_establecimiento
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
        const celda = agregarCelda(fila, error.message);
        celda.colSpan = 6;
        lista.append(fila);
    }
}

async function registrarMovimiento(stockId, tipoOperacion, valor) {
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
        await cargarStock();
    } catch (error) {
        mostrarMensaje(error.message, true);
    }
}

form.addEventListener("submit", async (evento) => {
    evento.preventDefault();

    const datos = Object.fromEntries(new FormData(form).entries());
    datos.cantidad = Number(datos.cantidad);
    datos.id_establecimiento = Number(datos.id_establecimiento);

    try {
        const creado = await respuestaApi("/api/stock", {
            method: "POST",
            body: JSON.stringify(datos)
        });

        mostrarMensaje(`Insumo "${creado.tipo_insumo}" registrado.`);
        form.reset();
        await cargarStock();
    } catch (error) {
        mostrarMensaje(error.message, true);
    }
});

document.querySelector("#stock-refresh").addEventListener(
    "click",
    cargarStock
);

async function iniciarStock() {
    try {
        await cargarEstablecimientos();
        await cargarStock();
    } catch (error) {
        mostrarMensaje(
            `No se pudo iniciar el módulo de stock: ${error.message}`,
            true
        );
    }
}

iniciarStock();
