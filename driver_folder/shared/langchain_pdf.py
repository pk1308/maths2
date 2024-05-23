from langchain_google_genai import ChatGoogleGenerativeAI
from shared.functions import  load_pdf_from_file

def summarize(file_path , context_base = "summarize the following text not less that 1000" ):
    """_summary_

    Args:
        file_path (_type_): _description_

    Returns:
        _type_: _description_
    """
    pages = load_pdf_from_file(file_path=file_path)

    # Setup the Google Generative AI model and invoke it using a human-friendly prompt
    llm = ChatGoogleGenerativeAI(model="gemini-pro")
    result = llm.invoke(f"{context_base}: \n {pages}:")

    return result.content
