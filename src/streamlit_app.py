import streamlit as st
import requests

# Título del chatbot
st.markdown("<h1 style='text-align: center;'>Asistente Virtual - Interbank</h1>", unsafe_allow_html=True)

# Crear contenedor para la conversación
if "messages" not in st.session_state:
    st.session_state["messages"] = []  # Inicializamos la sesión para guardar los mensajes

# Mostrar los mensajes previos en forma de chat
for msg in st.session_state["messages"]:
    style = "text-align: right; color: blue;" if msg["role"] == "user" else "text-align: left; color: black;"
    st.markdown(f"<p style='{style}'>{msg['content']}</p>", unsafe_allow_html=True)

# Definir función para enviar el mensaje
def send_message():
    user_message = st.session_state["user_input"]
    if user_message:
        # Guardar el mensaje del usuario en la sesión
        st.session_state["messages"].append({"role": "user", "content": user_message})

        # Realizar la solicitud al backend Flask
        try:
            response = requests.post(
                "http://localhost:8080/chat",
                json={"sessionID": "555156", "query": user_message}  # Simulamos una sesión fija
            )
            data = response.json()

            # Guardar la respuesta del asistente
            st.session_state["messages"].append({"role": "assistant", "content": data["response"]})
        except Exception as e:
            st.session_state["messages"].append({"role": "assistant", "content": f"Error: {str(e)}"})

        # Limpiar el input después de enviar el mensaje
        st.session_state["user_input"] = ""  # Limpiamos la entrada

# Entrada de texto para el usuario con on_change para enviar automáticamente
st.text_input(
    "Escribe tu mensaje...",
    key="user_input",  # Guardamos el input en session_state
    on_change=send_message  # Llama a la función cuando cambia el texto
)
