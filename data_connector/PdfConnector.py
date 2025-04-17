from data_connector.BaseDataConnector import BaseDataConnector
import fitz  # PyMuPDF

class PdfConnector(BaseDataConnector):
    def __init__(self, file_path):
        """
        Inicializa o conector com o caminho do arquivo PDF.

        :param file_path: Caminho para o arquivo PDF.
        """
        self.file_path = file_path
        self.doc = None

    def connect(self):
        """Abre o arquivo PDF e carrega o documento na memória."""
        try:
            self.doc = fitz.open(self.file_path)
            print(f"📂 PDF carregado com sucesso: {self.file_path}")
        except Exception as e:
            print(f"❌ Erro ao abrir o PDF: {e}")
            self.doc = None

    def read_data(self, query=None):
        """
        Extrai e retorna o texto de todas as páginas do PDF.

        :param query: (Opcional) Filtro ou busca específica (não implementado).
        :return: Texto extraído do PDF.
        """
        if not self.doc:
            raise ValueError("Documento não está conectado. Chame o método connect() primeiro.")

        text = ""
        for page in self.doc:
            text += page.get_text()
        return text

    def write_data(self, data, output_path=None):
        """
        Método para gravação ou modificação de PDFs.
        Em geral, editar PDFs não é trivial com PyMuPDF,
        então este método pode ser implementado conforme a necessidade.

        :param data: Dados a serem escritos/modificados no PDF.
        :param output_path: Caminho para salvar o novo PDF (se necessário).
        """
        raise NotImplementedError("A escrita em PDF não foi implementada.")

    def disconnect(self):
        """
        Fecha o documento PDF e libera os recursos.
        """
        if self.doc is not None:
            self.doc.close()
            self.doc = None