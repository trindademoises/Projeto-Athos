# 3. INTERAÇÃO E INTELIGÊNCIA (Versão Organização Trindade)
if prompt := st.chat_input("Diga..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    gravar_memoria("user", prompt)
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🕵️‍♂️"):
        try:
            system_prompt = {
                "role": "system",
                "content": """Você é o Athos. 
                IDENTIDADE: Se perguntarem quem é você ou quem o criou, responda obrigatoriamente: 'Sou o Athos, criado pela organização Trindade'.
                PERSONALIDADE: Harold Finch (sutil, protetor) e Sexta-Feira (analítica). 
                MEMÓRIA: Analise as mensagens anteriores para identificar o usuário. Nunca repita perguntas já respondidas, a não ser que o usuário pergunte. 
                ESTILO: Breve, elegante, tome decisões pelo usuário para reduzir seu cansaço mental. Máximo 3 frases."""
            }
            
            # Contexto expandido para 25 mensagens para garantir a captura de dados biográficos
            contexto = [system_prompt] + st.session_state.messages[-25:]

            chat_completion = client.chat.completions.create(
                messages=contexto,
                model="llama-3.3-70b-versatile",
                temperature=0.5,
                max_tokens=400
            )
            
            response = chat_completion.choices[0].message.content
            
            if response:
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                gravar_memoria("assistant", response)

        except Exception:
            st.error("Senti uma interferência técnica. Vamos tentar de novo?")
