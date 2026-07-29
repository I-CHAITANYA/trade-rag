import os
import re



def clean_text(text):
    """
    Clean extracted PDF text
    """

    # Remove extra spaces
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    # Remove unwanted characters
    text = text.strip()


    return text





def get_pdf_files(folder_path):
    """
    Return all PDF files inside a folder
    """

    pdf_files = []


    for root, dirs, files in os.walk(folder_path):

        for file in files:

            if file.lower().endswith(".pdf"):

                pdf_files.append(
                    os.path.join(
                        root,
                        file
                    )
                )


    return pdf_files





def create_directory(path):
    """
    Create directory if it does not exist
    """

    if not os.path.exists(path):

        os.makedirs(path)





def get_filename(path):
    """
    Extract filename from path
    """

    return os.path.basename(path)





def print_separator():
    """
    Display separator in terminal
    """

    print(
        "\n" + "=" * 50 + "\n"
    )