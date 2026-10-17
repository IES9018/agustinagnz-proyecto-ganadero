"use strict";

const API_ANIMALES = "/api/animales";
const selectorAnimal = document.getElementById("animal-trazabilidad");
const tablaTrazabilidad = document.getElementById("lista-trazabilidad");
const cantidadTrazabilidad = document.getElementById("cantidad-trazabilidad");
const mensajeTrazabilidad = document.getElementById("trazabilidad-mensaje");
const trazabilidadVacia = document.getElementById("trazabilidad-vacia");
const botonActualizar = document.getElementById("actualizar-trazabilidad");

function escaparHTML(valor) {
    return String(valor ?? "").replace(/[&<>"']/g, caracter => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;"
    })[caracter]);
}

function mostrarMensaje(texto, error = false) {
    mensajeTrazabilidad.textContent = texto;
    mensajeTrazabilidad.className = error ? "error-row" : "";
}

function formatearFecha(valor) {
    if (!valor) return "Sin fecha";

    const fecha = String(valor).split("T")[0];
    const partes = fecha.split("-");

    if (partes.length !== 3) return escaparHTML(valor);

    return `${partes[2]}/${partes[1]}/${partes[0]}`;
}

function etiquetaOrigen(origen) {
    if (origen === "sanidad") return "Sanidad";
    if (origen === "animal") return "Gestión de animales";
    return origen || "General";
}

function etiquetaEstado(evento) {
    if (evento.estado === "anulado") {
        return '<span class="trace-status trace-status--cancelled">Anulado</span>';
    }

    if (evento.estado === "vigente") {
        return '<span class="trace-status trace-status--active">Vigente</span>';
    }

    if (evento.tipo === "alta") {
        return '<span class="trace-status">Alta registrada</span>';
    }

    if (evento.tipo === "modificacion") {
        return '<span class="trace-status">Cambio registrado</span>';
    }

    return '<span class="trace-status">Registrado</span>';
}

async function solicitar(url) {
    const respuesta = await fetch(url);
    const datos = await respuesta.json().catch(() => ({}));

    if (!respuesta.ok) {
        throw new Error(datos.detail || "No se pudo completar la consulta.");
    }

    return datos;
}

async function cargarAnimales() {
    selectorAnimal.innerHTML = '<option value="">Cargando animales...</option>';
    selectorAnimal.disabled = true;

    try {
        const animales = await solicitar(API_ANIMALES);

        selectorAnimal.innerHTML =
            '<option value="">Seleccione un animal</option>';

        animales.forEach(animal => {
            const opcion = document.createElement("option");
            opcion.value = animal.id_animal;
            opcion.textContent =
                `${animal.identificador} — ${animal.especie} (${animal.raza})`;
            selectorAnimal.appendChild(opcion);
        });

        selectorAnimal.disabled = animales.length === 0;

        if (animales.length === 0) {
            selectorAnimal.innerHTML =
                '<option value="">No hay animales registrados</option>';
            mostrarMensaje("Primero debe registrar un animal.", true);
            cantidadTrazabilidad.textContent = "No hay animales disponibles.";
            return;
        }

        const parametros = new URLSearchParams(window.location.search);
        const idSolicitado = parametros.get("id");

        if (
            idSolicitado &&
            animales.some(animal => String(animal.id_animal) === idSolicitado)
        ) {
            selectorAnimal.value = idSolicitado;
        }

        if (selectorAnimal.value) {
            await cargarTrazabilidad();
        } else {
            mostrarMensaje("");
        }
    } catch (error) {
        selectorAnimal.innerHTML =
            '<option value="">Error al cargar los animales</option>';
        mostrarMensaje(error.message, true);
        cantidadTrazabilidad.textContent = "No se pudo cargar la lista de animales.";
    } finally {
        if (selectorAnimal.options.length > 0 &&
            selectorAnimal.options[0].value === "") {
            selectorAnimal.disabled = false;
        }
    }
}

async function cargarTrazabilidad() {
    const animalId = selectorAnimal.value;

    tablaTrazabilidad.innerHTML = "";
    trazabilidadVacia.style.display = "none";

    if (!animalId) {
        cantidadTrazabilidad.textContent =
            "Seleccione un animal para consultar su historial.";
        mostrarMensaje("");
        return;
    }

    botonActualizar.disabled = true;
    mostrarMensaje("Consultando historial...");
    cantidadTrazabilidad.textContent = "Cargando registros...";

    try {
        const datos = await solicitar(
            `${API_ANIMALES}/${encodeURIComponent(animalId)}/trazabilidad`
        );

        const eventos = Array.isArray(datos.eventos) ? datos.eventos : [];

        cantidadTrazabilidad.textContent =
            `${eventos.length} ${eventos.length === 1 ? "registro" : "registros"} ` +
            `en el historial de ${datos.identificador}.`;

        if (eventos.length === 0) {
            trazabilidadVacia.style.display = "block";
            mostrarMensaje("Consulta completada.");
            return;
        }

        tablaTrazabilidad.innerHTML = eventos.map(evento => `
            <tr>
                <td>${formatearFecha(evento.fecha)}</td>
                <td>${escaparHTML(evento.tipo)}</td>
                <td>${escaparHTML(etiquetaOrigen(evento.origen))}</td>
                <td>${escaparHTML(evento.descripcion)}</td>
                <td>${etiquetaEstado(evento)}</td>
            </tr>
        `).join("");

        mostrarMensaje("Historial actualizado correctamente.");
    } catch (error) {
        cantidadTrazabilidad.textContent = "No se pudo obtener el historial.";
        mostrarMensaje(error.message, true);
    } finally {
        botonActualizar.disabled = false;
    }
}

selectorAnimal.addEventListener("change", cargarTrazabilidad);
botonActualizar.addEventListener("click", cargarTrazabilidad);

cargarAnimales();
