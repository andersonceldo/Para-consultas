import streamlit as st
import pandas as pd
from datetime import datetime

# Cargar datos limpios
@st.cache_data
def cargar_datos():
    try:
        df = pd.read_csv("datos_limpios.csv", dtype={"CEDULA": str})
        df["FECHA SIMPLE"] = pd.to_datetime(df["FECHA SIMPLE"], errors="coerce")
        return df
    except Exception as e:
        st.error(f"❌ Error al cargar los datos: {str(e)}")
        return None

df = cargar_datos()

# Función para consultar por cédula
def consultar_por_cedula(cedula):
    if df is None:
        return None, "Datos no disponibles."

    try:
        resultado = df[df["CEDULA"].str.strip() == cedula.strip()]
        if resultado.empty:
            return None, "No se encontró ningún estudiante con esa cédula."

        info = resultado.iloc[0]
        hoy = datetime.now().date()
        fecha_defensa = info["FECHA SIMPLE"].date() if pd.notna(info["FECHA SIMPLE"]) else None

        datos = {
            "nombre": info.get("APELLIDOS Y NOMBRES ", "No disponible"),
            "opcion": info.filter(like="OPCION DE TITULACIÓN", axis=0).values[0] if info.filter(like="OPCION DE TITULACIÓN", axis=0).values.size > 0 else "No especificada",
            "fecha": info["FECHA SIMPLE"].strftime("%d/%m/%Y") if fecha_defensa else "No programado",
            "hora": info.get("HORA", "No especificada"),
            "enlace": info.get("ENLACES", "#"),
            "hoy": fecha_defensa == hoy if fecha_defensa else False
        }

        return datos, None

    except Exception as e:
        return None, f"Error al procesar la consulta: {str(e)}"

# Interfaz de usuario
def main():
    st.title("🎓 Consulta de Defensas UTPL")
    st.markdown("Ingrese su número de cédula para conocer sus detalles de defensa:")

    cedula = st.text_input("Cédula:", placeholder="Ejemplo: 0987654321")

    if st.button("Consultar", type="primary"):
        if not cedula or not cedula.isdigit():
            st.warning("Por favor ingrese una cédula válida (solo números).")
        else:
            with st.spinner("Buscando información..."):
                datos, error = consultar_por_cedula(cedula)

                if error:
                    st.error(error)
                else:
                    st.success(f"Información encontrada para: **{datos['nombre']}**")
                    st.write(f"**Opción de titulación:** {datos['opcion']}")

                    if datos["hoy"]:
                        st.balloons()
                        st.warning("⚠️ ¡Tienes defensa HOY!")
                        st.write(f"**Fecha:** {datos['fecha']}")
                        st.write(f"**Hora:** {datos['hora']}")
                        st.markdown(f"[🔗 Unirse a la reunión]({datos['enlace']})")
                    else:
                        st.info(f"📅 Próximo evento: {datos['fecha']} - {datos['hora']}")

    st.markdown("---")
    st.caption("© 2025 | Sistema de Consulta de Defensas | UTPL")

if __name__ == "__main__":
    main()
