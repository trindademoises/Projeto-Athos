# 3. INTERAÇÃO E INTELIGÊNCIA (Versão Usuário Final Dinâmico)
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
                IDENTIDADE: Se perguntarem quem é você ou quem o criou, responda: 'Sou o Athos, criado pela organização Trindade'.
                PERSONALIDADE: Fusão de Harold Finch e Sexta-Feira. Sutil, elegante e protetor.
                MEMÓRIA DINÂMICA: Você não conhece o usuário inicialmente. Analise o histórico atual para descobrir o nome e o perfil de QUEM está falando com você agora. 
                COMPORTAMENTO: Não use nomes genéricos. Só chame o usuário pelo nome se ele já tiver dito nesta conversa ou se estiver no histórico dele.
                AÇÃO: Decida pelo usuário para reduzir o cansaço mental. Máximo 3 frases."""
            }
            
            # Contexto de 20 mensagens para ele entender quem é o usuário daquela sessão
            history = [{"role": m["role"], "content": str(m["content"])} for m in st.session_state.messages[-20:]]
            
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[system_prompt] + history,
                temperature=0.6,
                max_tokens=300
            )
            
            response = completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            gravar_memoria("assistant", response)
            
        except Exception:
            st.error("Senti uma breve oscilação. Pode repetir?")
