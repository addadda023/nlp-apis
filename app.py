import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse, HTMLResponse
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from scripts.sentiment import sentiment_text, sentiment_text_sentences
from scripts.ocr import get_text_from_pdf, get_text_from_pdf_blob
from scripts.summarize import generate_summary
from starlette.templating import Jinja2Templates
import logging
import os

ALLOWED_EXTENSIONS = set(['pdf'])


# Log transport
logging.basicConfig(level=logging.INFO)

templates = Jinja2Templates(directory='templates')

app = Starlette(debug=True)
app.mount(r'/static', StaticFiles(directory='static'), name='Static')
# app.mount('/uploads', StaticFiles(directory='uploads'), name='Upload')


def allowed_file(filename):
    return filename[-3:].lower() in ALLOWED_EXTENSIONS


# Needed to avoid cross-domain issues
response_header = {
    'Access-Control-Allow-Origin': '*'
}


@app.route('/')
async def homepage(request):
    template = 'index.html'
    context = {'request': request}
    return templates.TemplateResponse(template, context)


@app.route('/contact')
async def contact(request):
    template = 'contact.html'
    context = {'request': request}
    return templates.TemplateResponse(template, context)


@app.route('/sentiment')
async def sentiment_home(request):
    template = 'sentiment.html'
    context = {'request': request}
    return templates.TemplateResponse(template, context)


@app.route('/sentiment', methods=['POST'])
async def sentiment_request(request: Request):
    if request.method == 'POST':
        inp_text = await request.form()
        inp_text = inp_text.get('input_text')

    logging.info('Received input: {}'.format(inp_text))

    # Sentiment of whole text
    text_sentiment = sentiment_text(inp_text)
    sentiment = 'Text Sentiment: ' + '{:.2f}'.format(text_sentiment)

    template = 'sentiment.html'
    context = {'request': request, 'inp_text': 'Input: ' + inp_text, 'sentiment': sentiment,
               'contact_us': 'Want sentiment analysis by sentence?'}

    # return JSONResponse({'sentiment': text_sentiment}, headers=response_header)
    return templates.TemplateResponse(template, context)


@app.route('/ocr')
async def ocr_home(request):
    template = 'ocr.html'
    context = {'request': request}
    return templates.TemplateResponse(template, context)


@app.route('/ocr', methods=['POST'])
async def ocr_request(request):
    context = {'request': request}
    form = await request.form()
    filename = form['upload_pdf'].filename
    contents = await form['upload_pdf'].read()

    if not contents:
        context['text'] = ['Oops empty file, try again.']

    if not allowed_file(filename):
        context['text'] = ['Format not allowed.']

    elif len(contents)//1024 >= 300:
        context['text'] = ['File size too large.']

    elif contents and allowed_file(filename) and len(contents)//1024 < 300:
        # https://github.com/encode/starlette/issues/775
        # Limit file size to 300kB
        with open(r'uploads/{}'.format(filename), 'wb') as f:
            f.write(contents)
            logging.info('Successfully wrote {} to uploads.'.format(filename))

        # Call OCR function
        extracted_text = get_text_from_pdf_blob(r'uploads/' + filename)
        context['text'] = extracted_text

        # Clean-up
        os.remove(r'uploads/{}'.format(filename))
        logging.info('Deleted {} from uploads after processing'.format(filename))

    template = 'ocr.html'
    return templates.TemplateResponse(template, context)


@app.route('/summarize')
async def summarize_home(request):
    template = 'summarize.html'
    context = {'request': request}
    return templates.TemplateResponse(template, context)


@app.route('/summarize', methods=['POST'])
async def summarize_request(request):
    if request.method == 'POST':
        text = await request.form()
        text = text.get('input_text')

        logging.info('Received input: {}'.format(text))
        summary = generate_summary(text, k=4)

    template = 'summarize.html'
    context = {'request': request, 'summary': summary,
               'contact_us': 'Request API'}

    # return JSONResponse({'sentiment': text_sentiment}, headers=response_header)
    return templates.TemplateResponse(template, context)


@app.exception_handler(404)
async def not_found(request, exc):
    """
    Return an HTTP 404 page.
    """
    template = "404.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context, status_code=404)


@app.exception_handler(405)
async def server_error(request, exc):
    """
    Return an HTTP 405 page.
    """
    template = "405.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context, status_code=405)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    uvicorn.run('app:app', host='0.0.0.0', port=port, log_level='info')
