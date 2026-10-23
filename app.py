import streamlit as st
import ezdxf
from ezdxf.addons.drawing import matplotlib as dxf_plt
import matplotlib.pyplot as plt
import aspose.cad as cad
import os
import tempfile

# Configuração da página para ocupar a tela toda
st.set_page_config(page_title="Visualizador CAD", page_icon="📐", layout="wide")

st.title("📐 Visualizador CAD Online (DWG ➡️ DXF)")
st.markdown("Envie um arquivo `.dwg`. O aplicativo fará a conversão automática nos bastidores e renderizará a planta 2D na tela.")

# 1. UPLOAD DO DWG
arquivo_dwg = st.file_uploader("Arraste ou selecione seu arquivo DWG", type=["dwg"])

if arquivo_dwg:
    st.divider()
    
    # Cria arquivos temporários seguros para não dar conflito no servidor
    with tempfile.NamedTemporaryFile(delete=False, suffix=".dwg") as tmp_dwg:
        tmp_dwg.write(arquivo_dwg.getvalue())
        caminho_dwg = tmp_dwg.name
        
    caminho_dxf = caminho_dwg.replace(".dwg", ".dxf")
    sucesso = False
    
    # ==========================================
    # PASSO 1: CONVERSÃO (DWG para DXF)
    # ==========================================
    # Usando st.status para um painel de carregamento bonito e profissional
    with st.status("🔄 **Passo 1: Lendo o DWG e convertendo para DXF...**", expanded=True) as status:
        try:
            # O Aspose.CAD faz a mágica de ler o formato fechado DWG
            imagem_cad = cad.Image.load(caminho_dwg)
            # E salva como DXF para podermos desenhar
            imagem_cad.save(caminho_dxf)
            status.update(label="✅ Conversão concluída com sucesso!", state="complete", expanded=False)
            sucesso = True
        except Exception as e:
            status.update(label=f"❌ Erro na conversão: {e}", state="error", expanded=True)

    # ==========================================
    # PASSO 2: VISUALIZAÇÃO DO DESENHO
    # ==========================================
    if sucesso and os.path.exists(caminho_dxf):
        with st.spinner("🎨 **Passo 2: Processando as linhas e desenhando a planta na tela...**"):
            try:
                # O ezdxf lê as linhas e blocos do arquivo convertido
                doc = ezdxf.readfile(caminho_dxf)
                msp = doc.modelspace()
                
                # Criação da figura com fundo PRETO (Estilo AutoCAD)
                fig = plt.figure(figsize=(15, 10))
                ax = fig.add_axes([0, 0, 1, 1])
                ax.set_facecolor("black")
                fig.patch.set_facecolor('black')
                
                # Motor gráfico processa os vetores para a tela
                ctx = dxf_plt.RenderContext(doc)
                out = dxf_plt.MatplotlibBackend(ax)
                dxf_plt.Frontend(ctx, out).draw_layout(msp, finalize=True)
                
                # Exibe o resultado!
                st.pyplot(fig)
                
                # BÔNUS: Botão para a pessoa baixar o DXF limpo caso queira
                st.markdown("<br>", unsafe_allow_html=True)
                with open(caminho_dxf, "rb") as file:
                    st.download_button(
                        label="📥 Baixar arquivo em formato .DXF",
                        data=file,
                        file_name=arquivo_dwg.name.replace(".dwg", ".dxf"),
                        mime="application/dxf",
                        type="primary"
                    )
                    
                st.caption("⚠️ **Nota:** Como o motor usa a licença de desenvolvedor gratuita, uma pequena marca d'água em formato de texto pode aparecer no centro do desenho.")
                
            except Exception as e:
                st.error(f"❌ Falha ao desenhar a geometria: {e}")
                
    # ==========================================
    # PASSO 3: LIMPEZA
    # ==========================================
    # Apaga os arquivos do servidor depois de desenhar para não travar a memória do Streamlit
    try:
        os.remove(caminho_dwg)
        if os.path.exists(caminho_dxf):
            os.remove(caminho_dxf)
    except:
        pass
