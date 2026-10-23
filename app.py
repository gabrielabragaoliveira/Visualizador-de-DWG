# Supondo que 'df' é o seu DataFrame gerado após ler o KML/KMZ
# Exibindo a visão prévia da tabela para o usuário
print("\n👁️ VISÃO PRÉVIA DOS PONTOS ENCONTRADOS:")
display(df)

print("-" * 60)
print("🎯 PASSO 2: SELEÇÃO DA LINHA DESEJADA")

# Cria uma lista de opções numéricas baseada na quantidade de linhas da tabela (Ex: 1, 2, 3...)
opcoes_linhas = [f"Linha {i+1}" for i in range(len(df))]

# Widget de Caixa de Seleção (Dropdown)
seletor_linha = widgets.Dropdown(
    options=opcoes_linhas,
    description='Escolha:',
    disabled=False,
)

botao_confirmar = widgets.Button(
    description='Confirmar Seleção',
    button_style='success',
    icon='check'
)

output_selecao = widgets.Output()

def on_confirmar_clicked(b):
    with output_selecao:
        clear_output()
        # Pega o índice real (0, 1, 2...) baseado na escolha (Linha 1, Linha 2...)
        indice_escolhido = opcoes_linhas.index(seletor_linha.value)
        linha_selecionada = df.iloc[indice_escolhido]
        
        print(f"\n✅ Você selecionou a {seletor_linha.value}:")
        display(pd.DataFrame(linha_selecionada).T) # Exibe a linha isolada como tabela
        
        # A partir daqui, você pode usar as variáveis da linha selecionada
        # Ex: lat = linha_selecionada['Latitude']

botao_confirmar.on_click(on_confirmar_clicked)

# Mostra o painel na tela
painel_selecao = widgets.VBox([seletor_linha, botao_confirmar, output_selecao])
display(painel_selecao)
