import streamlit as st
import ezdxf
from ezdxf.addons.drawing import matplotlib as dxf_plt
import matplotlib.pyplot as plt
import aspose.cad as cad
import os

st.set_page_config(page_title="Visualizador CAD Integrado", page_icon="📐", layout="wide")

st.title("📐 Visualizador CAD Web")
st.markdown("Envie seu arquivo **.dwg**. O sistema converterá para DXF e renderizará a planta na mesma tela.")

arquivo_dwg = st.file_uploader("Selecione seu arquivo DWG", type=["dwg"])

if arquivo_dwg:
    # Salva o arquivo temporariamente no servidor
    with open("temp.dwg", "wb") as f:
        f.write(arquivo_dwg.getbuffer())
        
    sucesso_conversao = False
    
    # ETAPA 1: Conversão (DWG para DXF)
    with st.spinner("🔄 Passo 1: Convertendo arquivo DWG para DXF..."):
        try:
            imagem_cad = cad.Image.load("temp.dwg")
            imagem_cad.save("temp.dxf")
            sucesso_conversao = True
        except Exception as e:
            st.error(f"❌ Erro durante a conversão: {e}")
            
    # ETAPA 2: Leitura e Renderização (DXF para Tela)
    if sucesso_conversao and os.path.exists("temp.dxf"):
        with st.spinner("🎨 Passo 2: Renderizando a geometria 2D do projeto..."):
            try:
                doc = ezdxf.readfile("temp.dxf")
                msp = doc.modelspace()
                
                # Configuração do gráfico
                fig = plt.figure(figsize=(12, 10))
                ax = fig.add_axes([0, 0, 1, 1])
                
                # Motor gráfico
                ctx = dxf_plt.RenderContext(doc)
                out = dxf_plt.MatplotlibBackend(ax)
                dxf_plt.Frontend(ctx, out).draw_layout(msp, finalize=True)
                
                # Exibe na tela
                st.pyplot(fig)
                st.info("💡 Nota: A conversão gratuita adiciona uma marca d'água da Aspose no desenho.")
                
            except Exception as e:
                st.error(f"❌ Falha na renderização da geometria: {e}")
