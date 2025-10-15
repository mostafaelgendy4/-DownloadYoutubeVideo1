from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__, static_folder='.', static_url_path='')

# ✅ يعرض صفحة واجهة التحميل
@app.route('/')
def index():
    return app.send_static_file('ytdawnload.html')

# ✅ يستخرج بيانات الفيديو فقط بدون تحميل
@app.route('/info', methods=['POST'])
def video_info():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({"error": "لم يتم إرسال رابط الفيديو"}), 400

    ydl_opts = {'quiet': True, 'skip_download': True}

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        # اختيار أعلى جودة فيديو متاحة
        formats = info.get("formats", [])
        best_format = max(formats, key=lambda f: f.get("height", 0))

        return jsonify({
            "title": info.get("title"),
            "thumbnail": info.get("thumbnail"),
            "duration": info.get("duration"),
            "channel": info.get("uploader"),
            "views": info.get("view_count"),
            "url": best_format.get("url")
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
