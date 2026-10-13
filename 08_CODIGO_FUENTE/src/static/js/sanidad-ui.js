"use strict";

const API_ANIMALES = "/api/animales";
const selectAnimal = document.getElementById("animal-id");
const selectHistorial = document.getElementById("animal-historial");
const formulario = document.getElementById("sanidad-form");
const tablaSanidad = document.getElementById("lista-sanidad");
const mensajeSanidad = document.getElementById("sanidad-mensaje");
const cantidadEventos = document.getElementById("cantidad-eventos");
const mensajeVacio = document.getElementById("mensaje-vacio");

function escapeHtml(value) {
    return String(value ?? "")
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function mostrarMensaje(texto, error = false) {
    mensajeSanidad.textContent = texto;
    mensajeSanidad.className = error ? "error-row" : "";
}

async function solicitar(url, opciones = {}) {
    const respuesta = await fetch(url, {
        ...opciones,
        headers: {
            "Content-Type": "application/json",
            ...(opciones.headers || {})
        }
    });

    const datos = await respuesta.json().catch(() => ({}));

    if (!respuesta.ok) {
        throw new Error(datos.detail || `Error HTTP ${respuesta.status}`);
    }

    return datos;
}

function obtenerLista(datos) {
    if (Array.isArray(datos)) return datos;
    return datos.animales || datos.eventos || datos.historial || datos.items || [];
}

async function cargarAnimales() {
    try {
        const animales = obtenerLista(await solicitar(API_ANIMALES));

        const opciones = animales.map(animal => {
            const id = animal.id_animal ?? animal.id;
            const identificador = animal.identificador || `Animal ${id}`;

            return `<option value="${escapeHtml(id)}">${escapeHtml(identificador)} — ${escapeHtml(animal.especie || "")}</option>`;
        }).join("");

        selectAnimal.insertAdjacentHTML("beforeend", opciones);
        selectHistorial.insertAdjacentHTML("beforeend", opciones);

        const idUrl = new URLSearchParams(window.location.search).get("id");

        if (idUrl && animales.some(a => String(a.id_animal ?? a.id) === idUrl)) {
            selectAnimal.value = idUrl;
            selectHistorial.value = idUrl;
            await cargarHistorial();
        }
    } catch (error) {
        mostrarMensaje(`No fue posible cargar los animales: ${error.message}`, true);
    }
}

async function cargarHistorial() {
    const idAnimal = selectHistorial.value;
    tablaSanidad.innerHTML = "";
    mensajeVacio.style.display = "none";

    if (!idAnimal) {
        cantidadEventos.textContent = "Seleccione un animal para consultar su historial";
        tablaSanidad.innerHTML =
            '<tr><td colspan="5">Seleccione un animal para consultar su historial.</td></tr>';
        return;
    }

    tablaSanidad.innerHTML =
        '<tr><td colspan="5">Cargando historial...</td></tr>';

    try {
        const eventos = obtenerLista(
            await solicitar(`${API_ANIMALES}/${encodeURIComponent(idAnimal)}/sanidad`)
        );

        cantidadEventos.textContent = eventos.length === 1
            ? "1 evento registrado"
            : `${eventos.length} eventos registrados`;

        if (!eventos.length) {
            tablaSanidad.innerHTML = "";
            mensajeVacio.style.display = "flex";
            return;
        }

        tablaSanidad.innerHTML = eventos.map(evento => {
            const idEvento = evento.id_evento ?? evento.id;
            const anulado = String(evento.estado || "").toLowerCase() === "anulado";
            const estadoClase = anulado ? "status-danger" : "status-ok";

            const acciones = anulado
                ? "—"
                : `<button type="button" class="action-edit" data-anular="${escapeHtml(idEvento)}">Anular</button>`;

            const motivo = evento.motivo_anulacion
                ? `<br><small>Motivo de anulación: ${escapeHtml(evento.motivo_anulacion)}</small>`
                : "";

            return `
                <tr>
                    <td>${escapeHtml(evento.fecha || "—")}</td>
                    <td>${escapeHtml(evento.tipo_evento || "—")}</td>
                    <td>${escapeHtml(evento.descripcion || "—")}${motivo}</td>
                    <td><span class="status ${estadoClase}">${anulado ? "Anulado" : "Vigente"}</span></td>
                    <td><div class="action-buttons">${acciones}</div></td>
                </tr>
            `;
        }).join("");
    } catch (error) {
        cantidadEventos.textContent = "No se pudo cargar el historial";
        tablaSanidad.innerHTML =
            `<tr><td colspan="5" class="error-row">${escapeHtml(error.message)}</td></tr>`;
    }
}

formulario.addEventListener("submit", async event => {
    event.preventDefault();

    const idAnimal = selectAnimal.value;

    const payload = {
        tipo_evento: document.getElementById("tipo-evento").value,
        descripcion: document.getElementById("descripcion-evento").value.trim(),
        fecha: document.getElementById("fecha-evento").value,
        estado: "Registrado"
    };

    if (!idAnimal || !payload.tipo_evento || !payload.descripcion || !payload.fecha) {
        mostrarMensaje("Complete todos los campos obligatorios.", true);
        return;
    }

    try {
        await solicitar(
            `${API_ANIMALES}/${encodeURIComponent(idAnimal)}/sanidad`,
            {
                method: "POST",
                body: JSON.stringify(payload)
            }
        );

        mostrarMensaje("Evento sanitario registrado correctamente.");
        formulario.reset();
        document.getElementById("fecha-evento").value =
            new Date().toISOString().slice(0, 10);

        selectHistorial.value = idAnimal;
        await cargarHistorial();
    } catch (error) {
        mostrarMensaje(`No fue posible registrar el evento: ${error.message}`, true);
    }
});

tablaSanidad.addEventListener("click", async event => {
    const boton = event.target.closest("[data-anular]");
    if (!boton) return;

    const motivo = window.prompt("Indique el motivo de anulación del evento:");
    if (!motivo || !motivo.trim()) return;

    try {
        await solicitar(
            `/api/sanidad/${encodeURIComponent(boton.dataset.anular)}?motivo=${encodeURIComponent(motivo.trim())}`,
            { method: "DELETE" }
        );

        mostrarMensaje("Evento anulado. El registro se conserva en el historial.");
        await cargarHistorial();
    } catch (error) {
        mostrarMensaje(`No fue posible anular el evento: ${error.message}`, true);
    }
});

selectHistorial.addEventListener("change", cargarHistorial);

document.getElementById("actualizar-historial")
    .addEventListener("click", cargarHistorial);

document.getElementById("limpiar-formulario").addEventListener("click", () => {
    formulario.reset();
    document.getElementById("fecha-evento").value =
        new Date().toISOString().slice(0, 10);
    mostrarMensaje("");
});

document.getElementById("fecha-evento").value =
    new Date().toISOString().slice(0, 10);

cargarAnimales();
