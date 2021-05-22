from shared import app, db, client, loop, get_client
from flask import  render_template, send_from_directory, request, send_file
from nftoken import create_nf_token
from werkzeug.utils import secure_filename
import os
import models
from datetime import datetime
import pandas as pd
import asyncio

from logging import getLogger


log = getLogger("main")


from threading import Thread

def start_worker(loop):
    asyncio.set_event_loop(loop)
    try:
        loop.run_forever()
    finally:
        loop.close()

@app.route('/')
def index():
    return render_template('index.html', user = models.User.current() )


@app.route('/create', methods=['GET', 'POST'])
def nftcreate():
    user = models.User.current()
    pubkey = request.form.get('pubkey')
    url = request.form.get('url')
    
    if request.method == 'POST':
        r = create_nf_token(pubkey)
        if (r):
            tokenId, tokenAddress = r
            log.info('create_nf_token success')
            nft = models.Files( token_id = tokenId, token_address = tokenAddress, user = user)
            db.session.add(nft)
            db.session.commit()

            return render_template('success.html', user = user, tokenId = tokenId,tokenAddress = tokenAddress )

    return render_template('create.html', user = user)


@app.route('/files')
def files():
    #mypath = app.config['UPLOAD_FOLDER']
    #onlyfiles = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
    user = models.User.current()
    fl = models.Files.query.filter_by(user_id = user.id).all()
    return render_template('files.html', files = fl, user = user)

@app.route('/download/<int:idx>', methods=['GET', 'POST'])
def download(idx):
    user = models.User.current()
    fl = models.Files.query.get(idx)
    fname, fext = os.path.splitext(fl.filename)
    filename = fname + '_norm.csv'
    return send_file(filename, as_attachment=True)



@app.route('/file/<int:idx>', methods=['GET', 'POST'])
def file(idx):
    user = models.User.current()
    fl = models.Files.query.get(idx)
    if request.method == 'POST':
        if fl.status == 'upload':
            fl.status = 'prepare'
            db.session.add(fl)
            db.session.commit()
            #response = client.procceed_file(fl.id)
            #asyncio.ensure_future(response.wait(), loop=worker_loop)
    fname, fext = os.path.splitext(fl.filename)

    return render_template('file.html', file = fname,)




@app.route('/fonts/<path:path>')
def send_js(path):
    return send_from_directory('static/fonts', path)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            #flash('No file part')
            #return redirect(request.url)
            return {'msg': 'fail'}
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return {'msg': 'fail filename'}
            #flash('No selected file')
            #return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            filename, file_extension = os.path.splitext(filename)

            if file_extension not in ['.xlsx','.csv']:
                return {'msg': 'fail fileext'}

            filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            filename = filename + datetime.now().strftime('%Y-%m-%d-%H.%M.%S') + file_extension
            file.save(filename)
            user = models.User.current()
            nf = models.Files(
                **{
                    'user_id': user.id,
                    'filename': filename,
                    'name': file.filename,
                    'status': 'upload'

                }
            )

            db.session.add(nf)
            db.session.commit()


            return {'msg': 'done', 'url': f'/file/{nf.id}'}






if __name__ == '__main__':
    # Wait for results
    worker_loop = asyncio.new_event_loop()
    #worker = Thread(target=start_worker, args=(worker_loop,))
    #client = get_client(worker_loop)
    app.run(host="0.0.0.0", port=80, debug=True)