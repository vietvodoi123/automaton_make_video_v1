from bs4 import BeautifulSoup, NavigableString, Tag

def extract_text_with_linebreaks(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    lines = []

    def traverse(node):
        for elem in node.children:
            if isinstance(elem, NavigableString):
                lines.append(str(elem))
            elif isinstance(elem, Tag):
                if elem.name in ["br", "p", "div"]:
                    # Duyệt con rồi thêm xuống dòng
                    traverse(elem)
                    lines.append("\n")
                else:
                    traverse(elem)

    traverse(soup)
    # Ghép lại, thay thế nhiều dấu xuống dòng liên tiếp bằng 1
    return "".join(lines).strip()


