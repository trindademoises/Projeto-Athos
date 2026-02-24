# 3. INTERAÇÃO E INTELIGÊNCIA (Versão Anti-Amnésia)
if prompt := st.chat_input("Diga..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    gravar_memoria("user", prompt)
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🕵️‍♂️"):
        try:
            # PROMPT SYSTEM TURBO: Força ele a olhar o histórico com atenção
            system_prompt = {
                "role": "system",
                "content": """Você é o Athos. 
                Sua tarefa principal agora é: ANTES DE RESPONDER, verifique no histórico abaixo se o usuário já disse o nome dele ou detalhes como (TDAH, São-paulino, turno da noite).
                Se o nome dele (Moisés/Batera) estiver nas mensagens anteriores, use-o naturalmente.
                DIRETRIZES:
                1. Nunca pergunte algo que já foi respondido no histórico.
                2. Seja o Harold Finch: protetor, sutil e analítico.
                3. Se ele parecer cansado, tome decisões por ele com ordens diretas.
                4. Estilo: Curto, elegante, no máximo 3 frases."""
            }
            
            # Enviamos um bloco maior de histórico (20 mensagens) para garantir que ele ache o nome
            contexto = [system_prompt] + st.session_state.messages[-20:]

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
