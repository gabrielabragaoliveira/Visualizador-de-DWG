import streamlit as st
import ezdxf
from ezdxf.addons.drawing import matplotlib as dxf_plt
import matplotlib.pyplot as plt
import subprocess
import os

# Configuração da página para ter mais espaço na tela
st.set_page_config(page_title="Visualizador CAD", page_icon="📐", layout="wide")

st.title("📐 Visualizador CAD Web")
st.markdown("Faça o upload do seu arquivo **.dwg** para visualizar a planta diretamente no navegador.")

# 1. Upload do Arquivo
arquivo_dwg = st.file_uploader("Envie seu arquivo DWG", type=["dwg"])

if arquivo_dwg:
    # Salva o arquivo temporariamente no servidor
    with open("temp.dwg", "wb") as f:
        f.write(arquivo_dwg.getbuffer())
        
    # 2. Conversão via ODA File Converter (requer instalação no servidor)
    with st.spinner("🔄 Convertendo formato proprietário DWG para DXF (isso pode levar alguns segundos)..."):
        # O ODAFileConverter lê o diretório atual (".") e converte para o próprio diretório (".")
        processo = subprocess.run(["ODAFileConverter", ".", ".", "ACAD2018", "DXF", "0", "1"], capture_output=True)
    
    # Verifica se a conversão gerou o arquivo DXF com sucesso
    if os.path.exists("temp.dxf"):
        # 3. Leitura e Renderização
        with st.spinner("🎨 Renderizando a geometria 2D do projeto..."):
            try:
                doc = ezdxf.readfile("temp.dxf")
                msp = doc.modelspace()
                
                # Configuração da área de plotagem (fundo escuro estilo AutoCAD fica melhor visualmente)
                fig = plt.figure(figsize=(12, 10))
                ax = fig.add_axes([0, 0, 1, 1])
                
                # Motor gráfico do ezdxf
                ctx = dxf_plt.RenderContext(doc)
                out = dxf_plt.MatplotlibBackend(ax)
                dxf_plt.Frontend(ctx, out).draw_layout(msp, finalize=True)
                
                # 4. Exibição na aplicação online
                st.pyplot(fig)
                
            except Exception as e:
                st.error(f"❌ Falha na renderização geométrica: {e}")
    else:
        st.error("❌ **Falha na Conversão!**")
        st.info("O sistema não conseguiu converter o arquivo. Verifique se o **ODA File Converter** está instalado no seu computador e adicionado às Variáveis de Ambiente (PATH).")
