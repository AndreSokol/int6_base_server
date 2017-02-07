import DB_emulator as DB

def main(page_path):

    if (page_path == "/music"):
        return showBands()
    if (page_path == "/error"):
        return showWhatHappensIfErrorInPageRendering()

    answer = "<html><body><h1>Hello, World!</h1>"
    answer += "<p><b>Your path:</b> " + page_path + "</b>"
    answer += "<br><img width=256 src=\"/st/sticker-rock-stas.png\">"
    answer += "</body></html>"

    return answer


def showBands():
    answer = """<html>
    <head>
        <title>Some bands</title>
        <link rel="stylesheet" href="/st/css/sample.css">
    </head>
    <body>
        <h1>Some cool bands</h1>"""
    for band in DB.bands:
        answer += "<p><b>Band name: </b>" + band[0] + "</p>"
        answer += "<p><b>Founder: </b>" + band[1] + "</p>"
        answer += "<hr>"
    answer += "<br><img width=256 src=\"/st/sticker-rock-stas.png\">"
    answer += """</body>
    </html>
    """

    return answer

def showWhatHappensIfErrorInPageRendering():
    return 100 / 0
