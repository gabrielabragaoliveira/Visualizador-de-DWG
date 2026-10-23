import streamlit as st
import ezdxf
from ezdxf.addons.drawing import matplotlib as dxf_plt
import matplotlib.pyplot as plt
import aspose.cad as cad
import os
import tempfile

# Configuração da página para tela cheia
st.set_page_config(page_title="Conversor CAD", page_icon="📐", layout="wide")

st.title("📐 Visualizador e Conversor CAD (DWG ➡️ DXF)")
st.markdown("Faça o upload do seu arquivo **.dwg**. O sistema converterá para DXF, renderizará a planta e disponibilizará o download automático.")

# 1. Upload do Arquivo
arquivo_dwg = st.file_uploader("Selecione ou arraste seu arquivo DWG", type=["dwg"])

if arquivo_dwg:
    st.divider()
    
    # Cria arquivos temporários com segurança
    with tempfile.NamedTemporaryFile(delete=False, suffix=".dwg") as tmp_dwg:
        tmp_dwg.write(arquivo_dwg.getvalue())
        caminho_dwg = tmp_dwg.name
        
    caminho_dxf = caminho_dwg.replace(".dwg", ".dxf")
    sucesso_conversao = False
    
    # 2. Conversão INTERNA via Aspose
    with st.status("🔄 **Passo 1: Convertendo formato proprietário DWG para DXF...**", expanded=True) as status:
        try:
            imagem_cad = cad.Image.load(caminho_dwg)
            imagem_cad.save(caminho_dxf)
            status.update(label="✅ Conversão concluída com sucesso!", state="complete", expanded=False)
            sucesso_conversao = True
        except Exception as e:
            status.update(label=f"❌ Erro na conversão: {e}", state="error", expanded=True)

    # 3. Leitura e Renderização
    if sucesso_conversao and os.path.exists(caminho_dxf):
        with st.spinner("🎨 **Passo 2: Renderizando a planta na tela (fundo estilo AutoCAD)...**"):
            try:
                doc = ezdxf.readfile(caminho_dxf)
                msp = doc.modelspace()
                
                # Configuração do gráfico (Fundo Preto)
                fig = plt.figure(figsize=(15, 10))
                ax = fig.add_axes([0, 0, 1, 1])
                ax.set_facecolor("black")
                fig.patch.set_facecolor('black')
                
                # Processamento de vetores
                ctx = dxf_plt.RenderContext(doc)
                out = dxf_plt.MatplotlibBackend(ax)
                dxf_plt.Frontend(ctx, out).draw_layout(msp, finalize=True)
                
                # Exibe a imagem no Streamlit
                st.pyplot(fig)
                
                st.caption("💡 **Nota:** A conversão gratuita adiciona uma pequena marca d'água em texto no centro do DXF.")
                
                # 4. Download Automático do DXF
                st.markdown("<br>", unsafe_allow_html=True)
                with open(caminho_dxf, "rb") as file:
                    st.download_button(
                        label="📥 Baixar arquivo .DXF convertido",
                        data=file,
                        file_name=arquivo_dwg.name.replace(".dwg", ".dxf"),
                        mime="application/dxf",
                        type="primary"
                    )
                    
            except Exception as e:
                st.error(f"❌ Erro ao desenhar a geometria: {e}")
                
    # 5. Limpeza de Memória do Servidor
    try:
        os.remove(caminho_dwg)
        if os.path.exists(caminho_dxf):
            os.remove(caminho_dxf)
    except:
        pass
