const API_PRODUCTORES = "/api/productores";

const formularioProductor = document.getElementById("productor-form");
const listaProductores = document.getElementById("lista-productores");
const mensajeProductor = document.getElementById("productor-mensaje");
const mensajeLista = document.getElementById("productores-mensaje");

const panelEstablecimientos = document.getElementById(
    "panel-establecimientos"
);
const listaEstablecimientos = document.getElementById(
    "lista-establecimientos"
);
const formularioEstablecimiento = document.getElementById(
    "establecimiento-form"
);
const panelFormularioEstablecimiento = document.getElementById(
    "form-establecimiento-panel"
);

let productorSeleccionado = null;

async function api(url, opciones = {}) {
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

function mostrarMensaje(elemento, texto, error = false) {
    elemento.textContent = texto;
    elemento.classList.toggle("is-error", error);
}

function limpiarFormularioProductor() {
    formularioProductor.reset();
    document.getElementById("productor-id").value = "";
    document.getElementById("titulo-form-productor").textContent =
        "Registrar productor";
}

function limpiarFormularioEstablecimiento() {
    formularioEstablecimiento.reset();
    document.getElementById("establecimiento-id").value = "";
    document.getElementById("establecimiento-estado").value = "activo";
    document.getElementById("titulo-form-establecimiento").textContent =
        "Nuevo establecimiento";
}

function datosProductor() {
    return {
        nombre: document.getElementById("productor-nombre").value,
        documento: document.getElementById("productor-documento").value,
        telefono: document.getElementById("productor-telefono").value,
        email: document.getElementById("productor-email").value,
        localidad: document.getElementById("productor-localidad").value,
        domicilio: document.getElementById("productor-domicilio").value,
        observaciones: document.getElementById(
            "productor-observaciones"
        ).value
    };
}

function crearCelda(fila, valor) {
    const celda = document.createElement("td");
    celda.textContent = valor ?? "—";
    fila.append(celda);
    return celda;
}

function crearBoton(texto, accion) {
    const boton = document.createElement("button");
    boton.type = "button";
    boton.textContent = texto;
    boton.addEventListener("click", accion);
    return boton;
}

async function cargarProductores() {
    listaProductores.replaceChildren();

    try {
        const productores = await api(API_PRODUCTORES);

        if (!productores.length) {
            const fila = document.createElement("tr");
            crearCelda(fila, "No hay productores registrados.").colSpan = 6;
            listaProductores.append(fila);
            return;
        }

        for (const productor of productores) {
            const fila = document.createElement("tr");

            crearCelda(fila, productor.nombre);
            crearCelda(fila, productor.documento);
            crearCelda(fila, productor.telefono);
            crearCelda(fila, productor.localidad);
            crearCelda(fila, productor.estado);

            const acciones = document.createElement("td");
            const grupoAcciones = document.createElement("div");
            grupoAcciones.className = "action-buttons";

            const botonEstablecimientos = crearBoton(
                "Ver establecimientos",
                () => seleccionarProductor(productor.id_productor)
            );
            botonEstablecimientos.classList.add("action-health");

            const botonEditar = crearBoton(
                "Editar",
                () => editarProductor(productor)
            );
            botonEditar.classList.add("action-edit");

            const botonEstado = crearBoton(
                productor.estado === "activo" ? "Desactivar" : "Activar",
                () => cambiarEstadoProductor(productor)
            );
            botonEstado.classList.add(
                productor.estado === "activo" ? "action-delete" : "action-health"
            );

            grupoAcciones.append(
                botonEstablecimientos,
                botonEditar,
                botonEstado
            );

            acciones.append(grupoAcciones);
            fila.append(acciones);

            listaProductores.append(fila);
        }
    } catch (error) {
        mostrarMensaje(mensajeLista, error.message, true);
    }
}

function editarProductor(productor) {
    document.getElementById("productor-id").value =
        productor.id_productor;

    document.getElementById("productor-nombre").value =
        productor.nombre || "";

    document.getElementById("productor-documento").value =
        productor.documento || "";

    document.getElementById("productor-telefono").value =
        productor.telefono || "";

    document.getElementById("productor-email").value =
        productor.email || "";

    document.getElementById("productor-localidad").value =
        productor.localidad || "";

    document.getElementById("productor-domicilio").value =
        productor.domicilio || "";

    document.getElementById("productor-observaciones").value =
        productor.observaciones || "";

    document.getElementById("titulo-form-productor").textContent =
        "Editar productor";

    formularioProductor.scrollIntoView({ behavior: "smooth" });
}

async function cambiarEstadoProductor(productor) {
    const nuevoEstado =
        productor.estado === "activo" ? "inactivo" : "activo";

    if (!confirm(
        `¿Desea cambiar el estado de ${productor.nombre} a ${nuevoEstado}?`
    )) {
        return;
    }

    try {
        await api(
            `${API_PRODUCTORES}/${productor.id_productor}/estado`,
            {
                method: "PATCH",
                body: JSON.stringify({ estado: nuevoEstado })
            }
        );

        await cargarProductores();
    } catch (error) {
        mostrarMensaje(mensajeLista, error.message, true);
    }
}

async function seleccionarProductor(productorId) {
    try {
        const productor = await api(
            `${API_PRODUCTORES}/${productorId}`
        );

        productorSeleccionado = productor;

        panelEstablecimientos.hidden = false;
        document.getElementById("titulo-establecimientos").textContent =
            productor.nombre;

        panelFormularioEstablecimiento.hidden = true;

        await cargarEstablecimientos();
        panelEstablecimientos.scrollIntoView({ behavior: "smooth" });
    } catch (error) {
        mostrarMensaje(mensajeLista, error.message, true);
    }
}

async function cargarEstablecimientos() {
    if (!productorSeleccionado) return;

    listaEstablecimientos.replaceChildren();

    try {
        const establecimientos = await api(
            `${API_PRODUCTORES}/${productorSeleccionado.id_productor}/establecimientos`
        );

        if (!establecimientos.length) {
            const fila = document.createElement("tr");
            crearCelda(
                fila,
                "Este productor todavía no tiene establecimientos."
            ).colSpan = 5;

            listaEstablecimientos.append(fila);
            return;
        }

        for (const establecimiento of establecimientos) {
            const fila = document.createElement("tr");

            crearCelda(fila, establecimiento.nombre);
            crearCelda(fila, establecimiento.ubicacion);
            crearCelda(fila, establecimiento.capacidad);
            crearCelda(fila, establecimiento.estado);

            const acciones = document.createElement("td");
            const grupoAcciones = document.createElement("div");
            grupoAcciones.className = "action-buttons";

            const botonEditar = crearBoton(
                "Editar",
                () => editarEstablecimiento(establecimiento)
            );
            botonEditar.classList.add("action-edit");

            const botonEstado = crearBoton(
                establecimiento.estado === "activo" ? "Desactivar" : "Activar",
                () => cambiarEstadoEstablecimiento(establecimiento)
            );
            botonEstado.classList.add(
                establecimiento.estado === "activo" ? "action-delete" : "action-health"
            );

            grupoAcciones.append(botonEditar, botonEstado);

            acciones.append(grupoAcciones);
            fila.append(acciones);
            listaEstablecimientos.append(fila);
        }
    } catch (error) {
        mostrarMensaje(
            document.getElementById("establecimientos-mensaje"),
            error.message,
            true
        );
    }
}

function editarEstablecimiento(establecimiento) {
    document.getElementById("establecimiento-id").value =
        establecimiento.id_establecimiento;

    document.getElementById("establecimiento-nombre").value =
        establecimiento.nombre;

    document.getElementById("establecimiento-ubicacion").value =
        establecimiento.ubicacion;

    document.getElementById("establecimiento-capacidad").value =
        establecimiento.capacidad ?? "";

    document.getElementById("establecimiento-estado").value =
        establecimiento.estado;

    document.getElementById("titulo-form-establecimiento").textContent =
        "Editar establecimiento";

    panelFormularioEstablecimiento.hidden = false;
    panelFormularioEstablecimiento.scrollIntoView({
        behavior: "smooth"
    });
}

async function cambiarEstadoEstablecimiento(establecimiento) {
    const nuevoEstado =
        establecimiento.estado === "activo" ? "inactivo" : "activo";

    if (!confirm(
        `¿Desea cambiar el estado de ${establecimiento.nombre} a ${nuevoEstado}?`
    )) {
        return;
    }

    try {
        await api(
            `/api/establecimientos/${establecimiento.id_establecimiento}/estado`,
            {
                method: "PATCH",
                body: JSON.stringify({ estado: nuevoEstado })
            }
        );

        await cargarEstablecimientos();
    } catch (error) {
        mostrarMensaje(
            document.getElementById("establecimientos-mensaje"),
            error.message,
            true
        );
    }
}

formularioProductor.addEventListener("submit", async evento => {
    evento.preventDefault();

    const id = document.getElementById("productor-id").value;
    const url = id ? `${API_PRODUCTORES}/${id}` : API_PRODUCTORES;
    const method = id ? "PUT" : "POST";

    try {
        await api(url, {
            method,
            body: JSON.stringify(datosProductor())
        });

        mostrarMensaje(
            mensajeProductor,
            id ? "Productor actualizado." : "Productor registrado."
        );

        limpiarFormularioProductor();
        await cargarProductores();

        if (productorSeleccionado) {
            await seleccionarProductor(
                productorSeleccionado.id_productor
            );
        }
    } catch (error) {
        mostrarMensaje(mensajeProductor, error.message, true);
    }
});

formularioEstablecimiento.addEventListener(
    "submit",
    async evento => {
        evento.preventDefault();

        if (!productorSeleccionado) return;

        const id = document.getElementById(
            "establecimiento-id"
        ).value;

        const datos = {
            nombre: document.getElementById(
                "establecimiento-nombre"
            ).value,
            ubicacion: document.getElementById(
                "establecimiento-ubicacion"
            ).value,
            capacidad: document.getElementById(
                "establecimiento-capacidad"
            ).value || null,
            estado: document.getElementById(
                "establecimiento-estado"
            ).value
        };

        const url = id
            ? `/api/establecimientos/${id}`
            : `${API_PRODUCTORES}/${productorSeleccionado.id_productor}/establecimientos`;

        try {
            await api(url, {
                method: id ? "PUT" : "POST",
                body: JSON.stringify(datos)
            });

            limpiarFormularioEstablecimiento();
            panelFormularioEstablecimiento.hidden = true;
            await cargarEstablecimientos();
        } catch (error) {
            mostrarMensaje(
                document.getElementById("establecimientos-mensaje"),
                error.message,
                true
            );
        }
    }
);

document.getElementById("nuevo-establecimiento").addEventListener(
    "click",
    () => {
        limpiarFormularioEstablecimiento();
        panelFormularioEstablecimiento.hidden = false;
        panelFormularioEstablecimiento.scrollIntoView({
            behavior: "smooth"
        });
    }
);

document.getElementById("cancelar-establecimiento").addEventListener(
    "click",
    () => {
        limpiarFormularioEstablecimiento();
        panelFormularioEstablecimiento.hidden = true;
    }
);

document.getElementById("cancelar-productor").addEventListener(
    "click",
    limpiarFormularioProductor
);

document.getElementById("actualizar-productores").addEventListener(
    "click",
    cargarProductores
);

document.addEventListener("DOMContentLoaded", async () => {
    try {
        const respuesta = await fetch("/auth/perfil", {
            credentials: "same-origin"
        });

        if (respuesta.ok) {
            const perfil = await respuesta.json();
            document.getElementById("perfil-nombre").textContent =
                perfil.nombre;
        }
    } catch (error) {
        console.error("No se pudo cargar el perfil:", error);
    }

    await cargarProductores();
});