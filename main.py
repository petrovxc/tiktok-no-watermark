from requests import get as rget
from flask    import Flask, request, render_template, send_file

app = Flask(__name__)

class Scrape:
    def __init__(self, aweme):
        self.url = f"https://api16-normal-useast5.us.tiktokv.com/tiktok/v1/videos/detail/?aweme_ids=[{aweme}]"

    def video(self):
        response = rget(self.url).json()
        video = response["aweme_details"][0]["video"]["play_addr"]["url_list"][0]
        return video

def get_aweme(raw_url):
    new_url = rget(raw_url).url
    aweme = new_url.split('/')[5].split('?')[0]
    return aweme

@app.route('/', methods=['GET', 'POST'])
def start():
    if request.method == 'POST':
        raw = request.form['raw_url']
        aweme = get_aweme(raw)
        data = Scrape(aweme).video()
        mimetype = 'video/mp4'
        download_name = f"{aweme}.mp4"

        response = rget(data, stream=True)
        return send_file(response.raw, mimetype=mimetype, as_attachment=True, download_name=download_name)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=8080)