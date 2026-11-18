import pandas as pd
import streamlit as st

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="StreamStore - Cuentas y Servicios Digitales",
    page_icon="🎬",
    layout="wide",
)

# --- ESTILOS CSS ---
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #05050f 0%, #100c2a 40%, #1e133d 70%, #0c081e 100%);
        color: #ffffff;
    }
    .product-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.12);
        text-align: center;
        margin-bottom: 15px;
        backdrop-filter: blur(10px);
        transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
    }
    .product-card:hover {
        transform: translateY(-5px);
        border-color: #00f2fe;
        box-shadow: 0 10px 25px rgba(0, 242, 254, 0.2);
    }
    .badge-stock {
        background-color: #198754;
        color: white;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.8em;
        font-weight: bold;
    }
    .badge-agotado {
        background-color: #dc3545;
        color: white;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.8em;
        font-weight: bold;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- LOGOS OFICIALES Y DESCRIPCIONES ---
LOGOS = {
    "Netflix": "https://cdn-icons-png.flaticon.com/512/5977/5977590.png",
    "Disney+": "https://cdn-icons-png.flaticon.com/512/5977/5977585.png",
    "HBO Max": "https://cdn-icons-png.flaticon.com/512/5977/5977579.png",
    "Amazon Prime Video": "https://cdn-icons-png.flaticon.com/512/5977/5977575.png",
    "Spotify": "https://cdn-icons-png.flaticon.com/512/2111/2111624.png",
    "YouTube Premium": "https://cdn-icons-png.flaticon.com/512/1384/1384060.png",
    "Canva Pro": "https://cdn-icons-png.flaticon.com/512/4494/4494748.png",
    "Crunchyroll": "https://cdn-icons-png.flaticon.com/512/5977/5977565.png",
    "Paramount+": "https://cdn-icons-png.flaticon.com/512/5977/5977595.png",
    "Otra App": "https://cdn-icons-png.flaticon.com/512/3163/3163478.png",
}

# --- INICIALIZACIÓN DE st.session_state ---
if "productos" not in st.session_state:
    st.session_state.productos = [
        {
            "id": 1,
            "plataforma": "Netflix",
            "plan": "4K Ultra HD (1 Perfil - 30 días)",
            "descripcion": "Películas y series en máxima calidad 4K, con perfil propio.",
            "precio": 15000.0,
            "stock": 8,
            "logo": LOGOS["Netflix"],
        },
        {
            "id": 2,
            "plataforma": "Amazon Prime Video",
            "plan": "Cuenta Completa 30 días",
            "descripcion": "Series Originals, películas y hasta 3 pantallas simultáneas.",
            "precio": 10000.0,
            "stock": 5,
            "logo": LOGOS["Amazon Prime Video"],
        },
        {
            "id": 3,
            "plataforma": "HBO Max",
            "plan": "Plan Platino 4K (1 Perfil)",
            "descripcion": (
                "Estrenos de cine, HBO, Warner y DC en calidad Ultra HD."
            ),
            "precio": 11000.0,
            "stock": 0,
            "logo": LOGOS["HBO Max"],
        },
        {
            "id": 4,
            "plataforma": "Disney+",
            "plan": "Estándar + ESPN (30 días)",
            "descripcion": (
                "Disney, Pixar, Marvel, Star Wars y deportes en vivo con"
                " ESPN."
            ),
            "precio": 12500.0,
            "stock": 6,
            "logo": LOGOS["Disney+"],
        },
        {
            "id": 5,
            "plataforma": "Spotify",
            "plan": "Premium Individual (1 Mes)",
            "descripcion": (
                "Música sin anuncios, saltos ilimitados y modo offline."
            ),
            "precio": 9000.0,
            "stock": 10,
            "logo": LOGOS["Spotify"],
        },
        {
            "id": 6,
            "plataforma": "YouTube Premium",
            "plan": "Sin Anuncios + Music (1 Mes)",
            "descripcion": (
                "Videos sin publicidad y acceso a YouTube Music incluido."
            ),
            "precio": 9500.0,
            "stock": 7,
            "logo": LOGOS["YouTube Premium"],
        },
        {
            "id": 7,
            "plataforma": "Canva Pro",
            "plan": "Cuenta Educativa / Equipo (1 Año)",
            "descripcion": (
                "Elementos gráficos premium, plantillas y herramientas con IA."
            ),
            "precio": 14000.0,
            "stock": 12,
            "logo": LOGOS["Canva Pro"],
        },
        {
            "id": 8,
            "plataforma": "Crunchyroll",
            "plan": "Mega Fan Sin Anuncios",
            "descripcion": (
                "Anime en alta definición sin publicidad y estrenos en simulcast."
            ),
            "precio": 8500.0,
            "stock": 0,
            "logo": LOGOS["Crunchyroll"],
        },
    ]

if "next_id" not in st.session_state:
    st.session_state.next_id = 9

if "carrito" not in st.session_state:
    st.session_state.carrito = []

if "usuario_registrado" not in st.session_state:
    st.session_state.usuario_registrado = {
        "correo": "",
        "tarjeta": "",
        "registrado": False,
    }


# --- FUNCIONES CRUD ---
def crear_producto(plataforma, plan, descripcion, precio, stock):
    nuevo = {
        "id": st.session_state.next_id,
        "plataforma": plataforma,
        "plan": plan,
        "descripcion": descripcion,
        "precio": float(precio),
        "stock": int(stock),
        "logo": LOGOS.get(plataforma, LOGOS["Otra App"]),
    }
    st.session_state.productos.append(nuevo)
    st.session_state.next_id += 1


def actualizar_producto(
    id_prod, nueva_plataforma, nuevo_plan, nueva_desc, nuevo_precio, nuevo_stock
):
    for prod in st.session_state.productos:
        if prod["id"] == id_prod:
            prod["plataforma"] = nueva_plataforma
            prod["plan"] = nuevo_plan
            prod["descripcion"] = nueva_desc
            prod["precio"] = float(nuevo_precio)
            prod["stock"] = int(nuevo_stock)
            prod["logo"] = LOGOS.get(nueva_plataforma, LOGOS["Otra App"])
            break


def eliminar_producto(id_prod):
    st.session_state.productos = [
        p for p in st.session_state.productos if p["id"] != id_prod
    ]
    st.session_state.carrito = [
        item for item in st.session_state.carrito if item["id"] != id_prod
    ]


def procesar_compra():
    for item_carrito in st.session_state.carrito:
        for prod in st.session_state.productos:
            if prod["id"] == item_carrito["id"]:
                prod["stock"] = max(0, prod["stock"] - item_carrito["cantidad"])
                break
    st.session_state.carrito = []


# --- BARRA LATERAL ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3163/3163478.png", width=50)
    st.markdown("### 👤 Portal de Cliente")

    if not st.session_state.usuario_registrado["registrado"]:
        st.write("Registra tu correo y tarjeta para compras rápidas.")
        with st.form("form_registro"):
            correo_input = st.text_input(
                "Correo Electrónico", placeholder="tu_correo@gmail.com"
            )
            tarjeta_input = st.text_input(
                "Número de Tarjeta (Simulado)",
                placeholder="4532 •••• •••• 8910",
                type="password",
            )
            btn_reg = st.form_submit_button(
                "Registrar y Guardar Tarjeta", use_container_width=True
            )

            if btn_reg:
                if "@" in correo_input and len(tarjeta_input) >= 4:
                    st.session_state.usuario_registrado["correo"] = correo_input
                    st.session_state.usuario_registrado["tarjeta"] = (
                        "•••• " + tarjeta_input[-4:]
                    )
                    st.session_state.usuario_registrado["registrado"] = True
                    st.success("¡Registro exitoso!")
                    st.rerun()
                else:
                    st.error("Ingresa un correo válido y una tarjeta correcta.")
    else:
        st.success("✅ ¡Cliente Autenticado!")
        st.markdown(
            f"**Correo:** {st.session_state.usuario_registrado['correo']}"
        )
        st.markdown(
            f"**Método de Pago:** Tarjeta asociada"
            f" ({st.session_state.usuario_registrado['tarjeta']})"
        )

        if st.button("Cerrar Sesión / Cambiar Datos", use_container_width=True):
            st.session_state.usuario_registrado = {
                "correo": "",
                "tarjeta": "",
                "registrado": False,
            }
            st.rerun()

    st.divider()
    st.markdown("### 🎬 StreamStore V2.2")


# --- ENCABEZADO ---
st.title("🎬 StreamStore | Cuentas y Servicios Digitales")
st.markdown("Tienda de streaming con control de inventario en tiempo real.")

# --- PESTAÑAS ---
tab_tienda, tab_stock, tab_crud = st.tabs(
    [
        "🛒 Catálogo y Carrito",
        "📊 Inventario (En Stock vs. Agotados)",
        "⚙️ Administrar Productos (CRUD)",
    ]
)

# ==========================================
# PESTAÑA 1: TIENDA Y CARRITO
# ==========================================
with tab_tienda:
    col_catalogo, col_carrito = st.columns([2.2, 1])

    with col_catalogo:
        st.subheader("Catálogo de Aplicaciones Disponibles")

        if not st.session_state.productos:
            st.warning("No hay productos registrados en el CRUD.")
        else:
            cols = st.columns(2)
            for idx, prod in enumerate(st.session_state.productos):
                with cols[idx % 2]:
                    badge = (
                        f'<span class="badge-stock">En Stock:'
                        f' {prod["stock"]}</span>'
                        if prod["stock"] > 0
                        else '<span class="badge-agotado">AGOTADO</span>'
                    )

                    st.markdown(
                        f"""
                        <div class="product-card">
                            <img src="{prod['logo']}" width="45" style="margin-bottom: 8px; object-fit: contain;"><br>
                            <h4 style="margin: 4px 0;">{prod['plataforma']}</h4>
                            <p style="color: #00f2fe; font-size: 0.9em; font-weight: bold; margin-bottom: 4px;">{prod['plan']}</p>
                            <p style="color: #d1d1d1; font-size: 0.82em; min-height: 38px; margin-bottom: 8px;">{prod['descripcion']}</p>
                            <h3 style="color: #ffffff; margin: 6px 0;">${prod['precio']:,.0f}</h3>
                            {badge}
                        </div>
                    """,
                        unsafe_allow_html=True,
                    )

                    if prod["stock"] > 0:
                        if st.button(
                            f"➕ Agregar al carrito",
                            key=f"btn_add_{prod['id']}",
                            use_container_width=True,
                        ):
                            en_carrito = next(
                                (
                                    item
                                    for item in st.session_state.carrito
                                    if item["id"] == prod["id"]
                                ),
                                None,
                            )
                            if en_carrito:
                                if en_carrito["cantidad"] < prod["stock"]:
                                    en_carrito["cantidad"] += 1
                                    st.toast(
                                        f"Se sumó +1 cuenta de"
                                        f" {prod['plataforma']}"
                                    )
                                else:
                                    st.warning("Stock máximo alcanzado.")
                            else:
                                st.session_state.carrito.append({
                                    "id": prod["id"],
                                    "plataforma": prod["plataforma"],
                                    "plan": prod["plan"],
                                    "precio": prod["precio"],
                                    "cantidad": 1,
                                })
                                st.toast(
                                    f"✅ {prod['plataforma']} agregado al"
                                    " carrito"
                                )
                    else:
                        st.button(
                            "🚫 Agotado",
                            key=f"btn_out_{prod['id']}",
                            disabled=True,
                            use_container_width=True,
                        )

    with col_carrito:
        st.subheader("🛍️ Carrito de Compra")
        with st.container(border=True):
            if not st.session_state.carrito:
                st.info("El carrito está vacío.")
            else:
                valor_total = 0.0
                total_articulos = 0

                for i, item in enumerate(st.session_state.carrito):
                    subtotal = item["precio"] * item["cantidad"]
                    valor_total += subtotal
                    total_articulos += item["cantidad"]

                    c_info, c_del = st.columns([4, 1])
                    with c_info:
                        st.markdown(f"**{item['plataforma']}**")
                        st.caption(f"{item['plan']}")
                        st.write(
                            f"{item['cantidad']} x ${item['precio']:,.0f} ="
                            f" **${subtotal:,.0f}**"
                        )
                    with c_del:
                        if st.button("🗑️", key=f"del_item_{i}"):
                            st.session_state.carrito.pop(i)
                            st.rerun()
                    st.divider()

                st.write(f"**Total de cuentas:** {total_articulos}")
                st.markdown(f"### Valor Total: `${valor_total:,.0f}`")

                b1, b2 = st.columns(2)
                with b1:
                    if st.button("🧹 Vaciar", use_container_width=True):
                        st.session_state.carrito = []
                        st.rerun()
                with b2:
                    if st.button(
                        "✅ Pagar", type="primary", use_container_width=True
                    ):
                        if not st.session_state.usuario_registrado["registrado"]:
                            st.warning(
                                "⚠️ Registra tu correo y tarjeta en la barra"
                                " lateral."
                            )
                        else:
                            procesar_compra()
                            st.success("🎉 ¡Compra exitosa!")
                            st.rerun()

# ==========================================
# PESTAÑA 2: CONTROL DE STOCK
# ==========================================
with tab_stock:
    st.subheader("Control de Inventario en Tiempo Real")
    df_productos = pd.DataFrame(st.session_state.productos)

    if df_productos.empty:
        st.info("No hay datos en el inventario.")
    else:
        df_en_stock = df_productos[df_productos["stock"] > 0]
        df_agotados = df_productos[df_productos["stock"] == 0]

        m1, m2, m3 = st.columns(3)
        m1.metric("Total de Productos", len(df_productos))
        m2.metric("En Stock", len(df_en_stock))
        m3.metric("Agotados", len(df_agotados))

        st.divider()

        col_disp, col_ago = st.columns(2)
        with col_disp:
            st.success("✅ Cuentas en Stock")
            if not df_en_stock.empty:
                st.dataframe(
                    df_en_stock[
                        [
                            "id",
                            "plataforma",
                            "plan",
                            "descripcion",
                            "precio",
                            "stock",
                        ]
                    ],
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                st.write("No hay cuentas con stock.")

        with col_ago:
            st.error("❌ Cuentas Agotadas")
            if not df_agotados.empty:
                st.dataframe(
                    df_agotados[
                        [
                            "id",
                            "plataforma",
                            "plan",
                            "descripcion",
                            "precio",
                            "stock",
                        ]
                    ],
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                st.write("¡Excelente! No hay productos agotados.")

# ==========================================
# PESTAÑA 3: CRUD
# ==========================================
with tab_crud:
    st.subheader("Gestión de Productos (CRUD)")

    operacion = st.radio(
        "Elige una acción:",
        [
            "➕ Agregar Producto (Create)",
            "📋 Ver Contenido (Read)",
            "✏️ Actualizar Producto (Update)",
            "🗑️ Borrar Producto (Delete)",
        ],
        horizontal=True,
    )

    if operacion == "➕ Agregar Producto (Create)":
        with st.form("form_crear", clear_on_submit=True):
            st.write("Registrar nueva cuenta o servicio")
            plat = st.selectbox("Aplicación / Plataforma", list(LOGOS.keys()))
            plan = st.text_input("Detalles del Plan")
            desc = st.text_area("Breve Descripción / Beneficios")
            precio = st.number_input("Precio ($)", min_value=0.0, step=1000.0)
            stock = st.number_input("Cantidad en Stock", min_value=0, step=1)

            if st.form_submit_button("Guardar"):
                if not plan.strip() or not desc.strip():
                    st.error("Completa el plan y la descripción.")
                else:
                    crear_producto(plat, plan, desc, precio, stock)
                    st.success(f"¡{plat} agregado correctamente!")
                    st.rerun()

    elif operacion == "📋 Ver Contenido (Read)":
        st.write("Tabla completa de productos:")
        if st.session_state.productos:
            df_ver = pd.DataFrame(st.session_state.productos)
            st.dataframe(
                df_ver[
                    ["id", "plataforma", "plan", "descripcion", "precio", "stock"]
                ],
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("La lista está vacía.")

    elif operacion == "✏️ Actualizar Producto (Update)":
        if not st.session_state.productos:
            st.warning("No hay productos para actualizar.")
        else:
            mapa_opciones = {
                f"ID {p['id']} | {p['plataforma']} - {p['plan']}": p
                for p in st.session_state.productos
            }
            seleccion = st.selectbox(
                "Selecciona el producto:", list(mapa_opciones.keys())
            )
            prod_sel = mapa_opciones[seleccion]

            with st.form("form_actualizar"):
                lista_plats = list(LOGOS.keys())
                indice_plat = (
                    lista_plats.index(prod_sel["plataforma"])
                    if prod_sel["plataforma"] in lista_plats
                    else 0
                )

                nueva_plat = st.selectbox(
                    "Plataforma", lista_plats, index=indice_plat
                )
                nuevo_plan = st.text_input("Plan", value=prod_sel["plan"])
                nueva_desc = st.text_area(
                    "Descripción", value=prod_sel["descripcion"]
                )
                nuevo_precio = st.number_input(
                    "Precio ($)", value=float(prod_sel["precio"]), step=1000.0
                )
                nuevo_stock = st.number_input(
                    "Stock",
                    value=int(prod_sel["stock"]),
                    min_value=0,
                    step=1,
                )

                if st.form_submit_button("Guardar Cambios"):
                    actualizar_producto(
                        prod_sel["id"],
                        nueva_plat,
                        nuevo_plan,
                        nueva_desc,
                        nuevo_precio,
                        nuevo_stock,
                    )
                    st.success("¡Actualizado con éxito!")
                    st.rerun()

    elif operacion == "🗑️ Borrar Producto (Delete)":
        if not st.session_state.productos:
            st.warning("No hay productos para eliminar.")
        else:
            mapa_borrar = {
                f"ID {p['id']} | {p['plataforma']} - {p['plan']}": p["id"]
                for p in st.session_state.productos
            }
            seleccion_del = st.selectbox(
                "Selecciona el producto a eliminar:", list(mapa_borrar.keys())
            )
            id_a_borrar = mapa_borrar[seleccion_del]

            if st.button("🗑️ Confirmar Eliminación", type="primary"):
                eliminar_producto(id_a_borrar)
                st.warning("Producto eliminado.")
                st.rerun()