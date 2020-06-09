import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse, HTMLResponse
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from scripts.sentiment import sentiment_text, sentiment_text_sentences
from starlette.templating import Jinja2Templates
import logging
import os

# Log transport
logging.basicConfig(level=logging.INFO)

templates = Jinja2Templates(directory='templates')

app = Starlette(debug=True)
app.mount('/static', StaticFiles(directory='static'), name='Static')

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


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    uvicorn.run('app:app', host='0.0.0.0', port=port, log_level='info')
