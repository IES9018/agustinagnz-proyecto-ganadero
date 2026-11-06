
"use strict";

const AUTH_TOKEN_KEY = "ganadapp_access_token";

const fetchOriginal = window.fetch.bind(window);

window.fetch = async function (input, options = {}) {
    const url = new URL(
        typeof input === "string" ? input : input.url,
        window.location.origin
    );

    const headers = new Headers(
        options.headers ||
        (input instanceof Request ? input.headers : undefined)
    );

    const token = sessionStorage.getItem(AUTH_TOKEN_KEY);

    const esLogin = url.pathname === "/auth/login";
    const esRegistro = url.pathname === "/auth/registro";

    if (
        token &&
        url.origin === window.location.origin &&
        !esLogin &&
        !esRegistro
    ) {
        headers.set("Authorization", `Bearer ${token}`);
    }

    const respuesta = await fetchOriginal(input, {
        ...options,
        headers
    });

    if (
        respuesta.status === 401 &&
        token &&
        !esLogin &&
        !esRegistro
    ) {
        sessionStorage.removeItem(AUTH_TOKEN_KEY);

        if (window.location.pathname !== "/login") {
            const destino =
                window.location.pathname + window.location.search;

            window.location.href =
                `/login?next=${encodeURIComponent(destino)}`;
        }
    }

    return respuesta;
};


document.addEventListener("DOMContentLoaded", async () => {
    const token = sessionStorage.getItem(AUTH_TOKEN_KEY);

    const formulariosLogout = document.querySelectorAll(
        'form[action="/auth/logout"]'
    );

    formulariosLogout.forEach(formulario => {
        formulario.hidden = !token;

        formulario.addEventListener("submit", evento => {
            evento.preventDefault();

            sessionStorage.removeItem(AUTH_TOKEN_KEY);
            window.location.href = "/login";
        });
    });

    const formularioLogin = document.querySelector(
        'form[action="/auth/login"]'
    );

    if (formularioLogin) {
        formularioLogin.addEventListener("submit", async evento => {
            evento.preventDefault();

            const boton = formularioLogin.querySelector(
                'button[type="submit"]'
            );

            const mensaje = document.getElementById("login-error");

            boton.disabled = true;
            mensaje.style.display = "none";

            try {
                const respuesta = await fetch("/auth/login", {
                    method: "POST",
                    headers: {
                        "Content-Type":
                            "application/x-www-form-urlencoded"
                    },
                    body: new URLSearchParams(
                        new FormData(formularioLogin)
                    )
                });

                const datos = await respuesta.json();

                if (!respuesta.ok) {
                    throw new Error(
                        datos.detail || "No se pudo iniciar sesión."
                    );
                }

                if (
                    !datos.access_token ||
                    datos.token_type !== "bearer"
                ) {
                    throw new Error(
                        "La respuesta de autenticación no es válida."
                    );
                }

                sessionStorage.setItem(
                    AUTH_TOKEN_KEY,
                    datos.access_token
                );

                const parametros = new URLSearchParams(
                    window.location.search
                );

                const destino = parametros.get("next");

                window.location.href =
                    destino && destino.startsWith("/")
                        ? destino
                        : "/";

            } catch (error) {
                mensaje.textContent = error.message;
                mensaje.style.display = "block";
            } finally {
                boton.disabled = false;
            }
        });
    }

    const rutasProtegidas = [
        "/animales",
        "/sanidad",
        "/stock",
        "/trazabilidad"
    ];

    const requiereAutenticacion =
        rutasProtegidas.includes(window.location.pathname);

    if (requiereAutenticacion && !token) {
        const destino =
            window.location.pathname + window.location.search;

        window.location.href =
            `/login?next=${encodeURIComponent(destino)}`;

        return;
    }

    if (token) {
        try {
            const respuesta = await fetchOriginal("/auth/perfil", {
                headers: {
                    "Authorization": `Bearer ${token}`
                },
                cache: "no-store"
            });

            if (!respuesta.ok) {
                sessionStorage.removeItem(AUTH_TOKEN_KEY);

                if (requiereAutenticacion) {
                    window.location.href = "/login";
                }

                return;
            }

            const perfil = await respuesta.json();

            const nombre = document.getElementById("perfil-nombre");
            const rol = document.getElementById("perfil-rol");

            if (nombre) {
                nombre.textContent = perfil.nombre;
            }

            if (rol && perfil.rol) {
                rol.textContent = perfil.rol;
            }

            if (window.location.pathname === "/login") {
                const destino = new URLSearchParams(
                    window.location.search
                ).get("next");

                window.location.href =
                    destino && destino.startsWith("/")
                        ? destino
                        : "/";
            }

        } catch (error) {
            console.error(
                "No se pudo verificar la autenticación:",
                error
            );
        }
    }
});
