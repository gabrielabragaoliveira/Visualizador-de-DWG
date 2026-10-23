import streamlit as st
import ezdxf
from ezdxf.addons.drawing import matplotlib as dxf_plt
import matplotlib.pyplot as plt
import aspose.cad as cad
import os

# Configuração da página para ter mais espaço na tela
st.set_page_config(page_title="Visualizador CAD Integrado", page_icon="📐", layout="wide")

st.title("📐 Visualizador CAD Online")
st.markdown("Faça o upload do seu arquivo **.dwg**. O sistema converterá e renderizará o projeto automaticamente nesta mesma tela!")

# 1. Upload do Arquivo
arquivo_dwg = st.file_uploader("Selecione ou arraste seu arquivo DWG", type=["dwg"])

if arquivo_dwg:
    # Salva o arquivo temporariamente no servidor do Streamlit
    with open("temp.dwg", "wb") as f:
        f.write(arquivo_dwg.getbuffer())
        
    sucesso_conversao = False
    
    # ---------------------------------------------------------
    # ETAPA 1: CONVERSÃO (DWG -> DXF)
    # ---------------------------------------------------------
    with st.spinner("🔄 Passo 1: Convertendo formato proprietário DWG para DXF..."):
        try:
            # A biblioteca Aspose lê o DWG fechado
            imagem_cad = cad.Image.load("temp.dwg")
            # E salva como DXF aberto no mesmo local
            imagem_cad.save("temp.dxf")
            sucesso_conversao = True
            st.toast("✅ Arquivo convertido com sucesso! Iniciando renderização...")
        except Exception as e:
            st.error(f"❌ Erro durante a conversão do arquivo: {e}")
            
    # ---------------------------------------------------------
    # ETAPA 2: LEITURA E VISUALIZAÇÃO
    # ---------------------------------------------------------
    if sucesso_conversao and os.path.exists("temp.dxf"):
        with st.spinner("🎨 Passo 2: Lendo vetores e renderizando a geometria 2D do projeto..."):
            try:
                # O ezdxf lê o arquivo DXF que acabou de ser gerado
                doc = ezdxf.readfile("temp.dxf")
                msp = doc.modelspace()
                
                # Configuração da área de plotagem 
                fig = plt.figure(figsize=(12, 10))
                ax = fig.add_axes([0, 0, 1, 1])
                
                # Motor gráfico do ezdxf traduzindo as linhas para o matplotlib
                ctx = dxf_plt.RenderContext(doc)
                out = dxf_plt.MatplotlibBackend(ax)
                dxf_plt.Frontend(ctx, out).draw_layout(msp, finalize=True)
                
                # Exibição do gráfico pronto na aplicação Streamlit
                st.pyplot(fig)
                
                st.info("💡 **Nota:** Como o conversor interno opera com a licença gratuita, uma pequena marca d'água em texto é adicionada ao centro do desenho.")
                
            except Exception as e:
                st.error(f"❌ Falha na renderização da geometria: {e}")
