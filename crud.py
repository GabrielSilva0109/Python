import streamlit as st
import sqlite3

# Conexão com o banco de dados SQLite
conn = sqlite3.connect('usuarios.db')
c = conn.cursor()

# Criação da tabela se não existir
c.execute('''
    CREATE TABLE IF NOT EXISTS usuario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        idade INTEGER,
        profissao TEXT
    )
''')
conn.commit()

# Funções CRUD
def inserir_usuario(nome, idade, profissao):
    c.execute('INSERT INTO usuario (nome, idade, profissao) VALUES (?, ?, ?)', (nome, idade, profissao))
    conn.commit()

def listar_usuarios():
    c.execute('SELECT * FROM usuario')
    return c.fetchall()

def atualizar_usuario(id, nome, idade, profissao):
    c.execute('UPDATE usuario SET nome=?, idade=?, profissao=? WHERE id=?', (nome, idade, profissao, id))
    conn.commit()

def deletar_usuario(id):
    c.execute('DELETE FROM usuario WHERE id=?', (id,))
    conn.commit()

# Interface Streamlit
st.title("CRUD de Usuários")

menu = st.sidebar.selectbox("Menu", ["Criar", "Ler", "Atualizar", "Deletar"])

if menu == "Criar":
    st.subheader("Adicionar Usuário")
    with st.form(key="form_criar"):
        nome = st.text_input("Nome")
        idade = st.number_input("Idade", min_value=0, max_value=120, step=1)
        profissao = st.selectbox("Profissão", ["Desenvolvedor", "Músico", "Designer", "Professor"])
        submit = st.form_submit_button("Adicionar")
        if submit:
            inserir_usuario(nome, idade, profissao)
            st.success("Usuário adicionado com sucesso!")

elif menu == "Ler":
    st.subheader("Lista de Usuários")
    usuarios = listar_usuarios()
    for u in usuarios:
        st.write(f"ID: {u[0]}, Nome: {u[1]}, Idade: {u[2]}, Profissão: {u[3]}")

elif menu == "Atualizar":
    st.subheader("Atualizar Usuário")
    usuarios = listar_usuarios()
    ids = [u[0] for u in usuarios]
    id_escolhido = st.selectbox("Selecione o ID do usuário", ids)
    usuario = next((u for u in usuarios if u[0] == id_escolhido), None)
    if usuario:
        with st.form(key="form_atualizar"):
            nome = st.text_input("Nome", value=usuario[1])
            idade = st.number_input("Idade", min_value=0, max_value=120, value=usuario[2], step=1)
            profissao = st.selectbox("Profissão", ["Desenvolvedor", "Músico", "Designer", "Professor"], index=["Desenvolvedor", "Músico", "Designer", "Professor"].index(usuario[3]))
            submit = st.form_submit_button("Atualizar")
            if submit:
                atualizar_usuario(id_escolhido, nome, idade, profissao)
                st.success("Usuário atualizado com sucesso!")

elif menu == "Deletar":
    st.subheader("Deletar Usuário")
    usuarios = listar_usuarios()
    ids = [u[0] for u in usuarios]
    id_escolhido = st.selectbox("Selecione o ID do usuário para deletar", ids)
    if st.button("Deletar"):
        deletar_usuario(id_escolhido)
        st.success("Usuário deletado com sucesso!")


        # Funções adicionais para transações financeiras

        def registrar_emprestimo(usuario_id, valor, taxa_juros, parcelas):
            c.execute('''
                CREATE TABLE IF NOT EXISTS emprestimo (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario_id INTEGER,
                    valor REAL,
                    taxa_juros REAL,
                    parcelas INTEGER,
                    FOREIGN KEY(usuario_id) REFERENCES usuario(id)
                )
            ''')
            c.execute('INSERT INTO emprestimo (usuario_id, valor, taxa_juros, parcelas) VALUES (?, ?, ?, ?)',
                      (usuario_id, valor, taxa_juros, parcelas))
            conn.commit()

        def listar_emprestimos():
            c.execute('SELECT * FROM emprestimo')
            return c.fetchall()

        def registrar_consorcio(usuario_id, valor_cota, meses):
            c.execute('''
                CREATE TABLE IF NOT EXISTS consorcio (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario_id INTEGER,
                    valor_cota REAL,
                    meses INTEGER,
                    FOREIGN KEY(usuario_id) REFERENCES usuario(id)
                )
            ''')
            c.execute('INSERT INTO consorcio (usuario_id, valor_cota, meses) VALUES (?, ?, ?)',
                      (usuario_id, valor_cota, meses))
            conn.commit()

        def listar_consorcios():
            c.execute('SELECT * FROM consorcio')
            return c.fetchall()

        # Interface para transações financeiras
        st.sidebar.markdown("---")
        transacao = st.sidebar.selectbox("Transações Financeiras", ["Nenhuma", "Empréstimo", "Consórcio"])

        if transacao == "Empréstimo":
            st.subheader("Registrar Empréstimo")
            usuarios = listar_usuarios()
            ids = [u[0] for u in usuarios]
            usuario_id = st.selectbox("Usuário", ids)
            valor = st.number_input("Valor do Empréstimo", min_value=0.0, step=100.0)
            taxa_juros = st.number_input("Taxa de Juros (%)", min_value=0.0, step=0.1)
            parcelas = st.number_input("Parcelas", min_value=1, step=1)
            if st.button("Registrar Empréstimo"):
                registrar_emprestimo(usuario_id, valor, taxa_juros, parcelas)
                st.success("Empréstimo registrado com sucesso!")
            st.subheader("Empréstimos Registrados")
            for e in listar_emprestimos():
                st.write(f"ID: {e[0]}, Usuário: {e[1]}, Valor: {e[2]}, Juros: {e[3]}%, Parcelas: {e[4]}")

        elif transacao == "Consórcio":
            st.subheader("Registrar Consórcio")
            usuarios = listar_usuarios()
            ids = [u[0] for u in usuarios]
            usuario_id = st.selectbox("Usuário", ids)
            valor_cota = st.number_input("Valor da Cota", min_value=0.0, step=100.0)
            meses = st.number_input("Meses", min_value=1, step=1)
            if st.button("Registrar Consórcio"):
                registrar_consorcio(usuario_id, valor_cota, meses)
                st.success("Consórcio registrado com sucesso!")
            st.subheader("Consórcios Registrados")
            for c_ in listar_consorcios():
                st.write(f"ID: {c_[0]}, Usuário: {c_[1]}, Valor da Cota: {c_[2]}, Meses: {c_[3]}")


                # Funções para operações adicionais

                def buscar_usuario_por_nome(nome):
                    c.execute('SELECT * FROM usuario WHERE nome LIKE ?', ('%' + nome + '%',))
                    return c.fetchall()

                def buscar_emprestimos_por_usuario(usuario_id):
                    c.execute('SELECT * FROM emprestimo WHERE usuario_id=?', (usuario_id,))
                    return c.fetchall()

                def buscar_consorcios_por_usuario(usuario_id):
                    c.execute('SELECT * FROM consorcio WHERE usuario_id=?', (usuario_id,))
                    return c.fetchall()

                def deletar_emprestimo(emprestimo_id):
                    c.execute('DELETE FROM emprestimo WHERE id=?', (emprestimo_id,))
                    conn.commit()

                def deletar_consorcio(consorcio_id):
                    c.execute('DELETE FROM consorcio WHERE id=?', (consorcio_id,))
                    conn.commit()

                # Interface adicional no Streamlit
                st.sidebar.markdown("---")
                st.sidebar.subheader("Operações Avançadas")

                op_avancada = st.sidebar.selectbox("Operação Avançada", ["Nenhuma", "Buscar Usuário", "Buscar Empréstimos", "Buscar Consórcios", "Deletar Empréstimo", "Deletar Consórcio"])

                if op_avancada == "Buscar Usuário":
                    st.subheader("Buscar Usuário por Nome")
                    nome_busca = st.text_input("Digite o nome para buscar")
                    if st.button("Buscar"):
                        resultados = buscar_usuario_por_nome(nome_busca)
                        if resultados:
                            for u in resultados:
                                st.write(f"ID: {u[0]}, Nome: {u[1]}, Idade: {u[2]}, Profissão: {u[3]}")
                        else:
                            st.info("Nenhum usuário encontrado.")

                elif op_avancada == "Buscar Empréstimos":
                    st.subheader("Buscar Empréstimos por Usuário")
                    usuarios = listar_usuarios()
                    ids = [u[0] for u in usuarios]
                    usuario_id = st.selectbox("Selecione o usuário", ids)
                    if st.button("Buscar Empréstimos"):
                        emprestimos = buscar_emprestimos_por_usuario(usuario_id)
                        if emprestimos:
                            for e in emprestimos:
                                st.write(f"ID: {e[0]}, Valor: {e[2]}, Juros: {e[3]}%, Parcelas: {e[4]}")
                        else:
                            st.info("Nenhum empréstimo encontrado para este usuário.")

                elif op_avancada == "Buscar Consórcios":
                    st.subheader("Buscar Consórcios por Usuário")
                    usuarios = listar_usuarios()
                    ids = [u[0] for u in usuarios]
                    usuario_id = st.selectbox("Selecione o usuário", ids)
                    if st.button("Buscar Consórcios"):
                        consorcios = buscar_consorcios_por_usuario(usuario_id)
                        if consorcios:
                            for c_ in consorcios:
                                st.write(f"ID: {c_[0]}, Valor da Cota: {c_[2]}, Meses: {c_[3]}")
                        else:
                            st.info("Nenhum consórcio encontrado para este usuário.")

                elif op_avancada == "Deletar Empréstimo":
                    st.subheader("Deletar Empréstimo")
                    emprestimos = listar_emprestimos()
                    emprestimo_ids = [e[0] for e in emprestimos]
                    if emprestimo_ids:
                        emprestimo_id = st.selectbox("Selecione o ID do empréstimo", emprestimo_ids)
                        if st.button("Deletar Empréstimo"):
                            deletar_emprestimo(emprestimo_id)
                            st.success("Empréstimo deletado com sucesso!")
                    else:
                        st.info("Nenhum empréstimo cadastrado.")

                elif op_avancada == "Deletar Consórcio":
                    st.subheader("Deletar Consórcio")
                    consorcios = listar_consorcios()
                    consorcio_ids = [c_[0] for c_ in consorcios]
                    if consorcio_ids:
                        consorcio_id = st.selectbox("Selecione o ID do consórcio", consorcio_ids)
                        if st.button("Deletar Consórcio"):
                            deletar_consorcio(consorcio_id)
                            st.success("Consórcio deletado com sucesso!")
                    else:
                        st.info("Nenhum consórcio cadastrado.")


                        # Fechar conexão ao final da execução
                        conn.close()